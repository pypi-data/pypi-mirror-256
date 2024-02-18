import hmac
from base64 import b64encode
from hashlib import sha1
from types import MethodType

import requests
from requests.compat import quote, urlencode
from requests.exceptions import HTTPError, JSONDecodeError, Timeout

from ..error_helper import *
from ..retries import retry_timeouts
from .base import ApiPart, Supplier

class TME(Supplier):
    def setup(self, api_token, api_secret, currency, language, location):
        self.tme_api = TMEApi(api_token, api_secret, language, location, currency)
        return True

    def search(self, search_term):
        tme_part = self.tme_api.get_product(search_term)
        if tme_part:
            tme_stocks = self.tme_api.get_prices_and_stocks([tme_part["Symbol"]])
            tme_stock = tme_stocks[0] if tme_stocks else {}
            return [self.get_api_part(tme_part, tme_stock)], 1

        if not (results := self.tme_api.product_search(search_term)):
            return [], 0

        filtered_matches = [
            tme_part for tme_part in results["ProductList"]
            if tme_part["OriginalSymbol"].lower().startswith(search_term.lower())
            or tme_part["Symbol"].lower().startswith(search_term.lower())
        ]

        exact_matches = [
            tme_part for tme_part in filtered_matches
            if tme_part["OriginalSymbol"].lower() == search_term.lower()
            or tme_part["Symbol"].lower() == search_term.lower()
        ]
        if len(exact_matches) == 1:
            filtered_matches = exact_matches

        tme_stocks = self.tme_api.get_prices_and_stocks([m["Symbol"] for m in filtered_matches])
        return list(map(self.get_api_part, filtered_matches, tme_stocks)), len(filtered_matches)

    def get_api_part(self, tme_part, tme_stock):
        price_breaks = {
            price_break["Amount"]: price_break["PriceValue"]
            for price_break in tme_stock.get("PriceList", [])
        }

        api_part = ApiPart(
            description=tme_part.get("Description", ""),
            image_url=fix_tme_url(tme_part.get("Photo")),
            datasheet_url=None,
            supplier_link=fix_tme_url(tme_part.get("ProductInformationPage")),
            SKU=tme_part.get("Symbol", ""),
            manufacturer=tme_part.get("Producer", ""),
            manufacturer_link="",
            MPN=tme_part.get("OriginalSymbol", ""),
            quantity_available=tme_stock.get("Amount", 0),
            packaging="",
            category_path=self.tme_api.get_category_path(tme_part["CategoryId"]),
            parameters=None,
            price_breaks=price_breaks,
            currency=self.tme_api.currency,
        )

        api_part.finalize_hook = MethodType(self.finalize_hook, api_part)

        return api_part

    def finalize_hook(self, api_part: ApiPart):
        if not (parameters := self.tme_api.get_parameters(api_part.SKU)):
            return False

        api_part.parameters = {}
        for parameter in parameters:
            name = parameter["ParameterName"]
            value = parameter["ParameterValue"]
            if existing_value := api_part.parameters.get(name):
                value = ", ".join((existing_value, value))
            api_part.parameters[name] = value

        if product_files := self.tme_api.get_product_files(api_part.SKU):
            for document in product_files.get("DocumentList", []):
                if document.get("DocumentType") == "DTE":
                    api_part.datasheet_url = fix_tme_url(document.get("DocumentUrl"))
                    break

        return True

def fix_tme_url(url):
    if url and url.startswith("//"):
        return f"https:{url}"
    return url

class TMEApi:
    BASE_URL = "https://api.tme.eu/"

    def __init__(
        self, token, secret, language="EN", country="PL", currency="EUR", net_prices=True,
    ):
        self._categories = None
        self.token = token
        self.secret = secret
        self.language = language
        self.country = country
        self.currency = currency
        self.net_prices = net_prices

    def get_category_path(self, category_id):
        if self._categories is None:
            self._categories = {
                category["Id"]: (category["Name"], category["ParentId"])
                for category in self.get_categories()
            }

        parent_id = category_id
        category_path = []
        while True:
            name, parent_id = self._categories[parent_id]
            if not name:
                return category_path
            category_path.insert(0, name)

    def get_product(self, product_symbol):
        result = self._api_call("Products/GetProducts", {
            "Country": self.country,
            "Language": self.language,
            "SymbolList[0]": product_symbol,
        })
        if result:
            products = result.json()["Data"]["ProductList"]
            if products and len(products) == 1:
                return products[0]
        return []

    def product_search(self, search_term):
        result = self._api_call("Products/Search", {
            "Country": self.country,
            "Language": self.language,
            "SearchPlain": search_term,
        })
        if result:
            return result.json()["Data"]
        return []

    def get_prices_and_stocks(self, product_symbols):
        if not product_symbols:
            return []

        # this api call only supports up to 50 symbols
        product_symbols = product_symbols[:50]

        data = {
            "Country": self.country,
            "Language": self.language,
            "Currency": self.currency,
            "GrossPrices": str(not self.net_prices).lower(),
        }
        for i, symbol in enumerate(product_symbols[:10]):
            data[f"SymbolList[{i}]"] = symbol

        if result := self._api_call("Products/GetPricesAndStocks", data):
            result_data = result.json()["Data"]
            assert result_data["Currency"] == self.currency
            assert result_data["PriceType"] == ("NET" if self.net_prices else "GROSS")
            return result_data["ProductList"]
        return []

    def get_categories(self):
        result = self._api_call("Products/GetCategories", {
            "Country": self.country,
            "Language": self.language,
            "Tree": "false",
        })
        if result:
            return result.json()["Data"]["CategoryTree"]
        return []

    def get_parameters(self, product_symbol):
        result = self._api_call("Products/GetParameters", {
            "Country": self.country,
            "Language": self.language,
            "SymbolList[0]": product_symbol,
        })
        if result:
            return result.json()["Data"]["ProductList"][0]["ParameterList"]
        return []

    def get_product_files(self, product_symbol):
        result = self._api_call("Products/GetProductsFiles", {
            "Country": self.country,
            "Language": self.language,
            "SymbolList[0]": product_symbol,
        })
        if result:
            return result.json()["Data"]["ProductList"][0]["Files"]
        return []

    HEADERS = {"Content-type": "application/x-www-form-urlencoded"}

    def _api_call(self, action, data):
        url = f"{self.BASE_URL}{action}.json"
        data_sorted = dict(sorted({**data, "Token": self.token}.items()))

        signature_base = f"POST&{quote(url, '')}&{quote(urlencode(data_sorted), '')}".encode()
        signature = b64encode(hmac.new(self.secret.encode(), signature_base, sha1).digest())
        data_sorted["ApiSignature"] = signature

        try:
            for retry in retry_timeouts():
                with retry:
                    result = requests.post(url, urlencode(data_sorted), headers=self.HEADERS)
                    result.raise_for_status()
        except (HTTPError, Timeout) as e:
            try:
                status = result.json()["Status"]
                if status == "E_INPUT_PARAMS_VALIDATION_ERROR":
                    return None
                error(f"'{action}' action failed with '{status}'", prefix="TME API error: ")
            except (JSONDecodeError, KeyError):
                error(f"'{action}' action failed with '{e}'", prefix="TME API error: ")

        return result
