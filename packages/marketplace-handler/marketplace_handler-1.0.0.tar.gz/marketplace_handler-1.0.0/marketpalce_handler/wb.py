from typing import List

from requests import HTTPError

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from .exceptions import InitialisationException, InvalidStatusException
from .logger import get_logger
from .config import settings
from .marketplace import Marketplace
from .schemas import MsItem, WbUpdateItem


class Wildberries(Marketplace):
    def __init__(self, token_id, bgd_token, bgd_token_url, bgd_mapping_url):
        self.bgd_mapping_url = bgd_mapping_url
        self._logger = get_logger()
        self._session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=0.5,
        )
        self._session.mount("https://", HTTPAdapter(max_retries=retries))

        try:
            bgd_token_resp = self._session.get(
                bgd_token_url,
                headers={
                    "Authorization": f"Token {bgd_token}",
                },
                timeout=5,
            )
            bgd_token_resp.raise_for_status()
            for token in bgd_token_resp.json():
                warehouse_id = token.get("warehouse_id")
                if warehouse_id and token.get("id") == token_id:
                    self.warehouse_id = warehouse_id
                    self._session.headers.update(
                        {
                            "Authorization": f"{token['common_token']}",
                        }
                    )
                    self._logger.debug("Wildberries is initialized")
                    break
        except HTTPError:
            self._logger.error("Can't connect to BGD token url")
            raise InitialisationException(
                f"Can't connect to BGD token url {bgd_token_resp.status_code}"
            )

        if not hasattr(self, "warehouse_id"):
            self._logger.error("Warehouse id is not found")
            raise InitialisationException("Warehouse id is not found")

    def get_stock(self, ms_id):
        try:
            ms_items = self._get_mapped_data([ms_id], [0])[0]
            stocks = self._session.post(
                f"{settings.wb_api_url}api/v3/stocks/{self.warehouse_id}",
                json={
                    "skus": [ms_items.barcodes],
                },
                timeout=5,
            )
            stocks.raise_for_status()
            self._logger.info(f"Wildberries: {ms_id} stock is refreshed")
            return stocks.json()
        except HTTPError as e:
            self._logger.error(
                f"Wildberries: {ms_id} stock is not refreshed. Error: {e}"
            )
            raise e

    def refresh_stock(self, ms_id: str, value: int):
        try:
            ms_items = self._get_mapped_data([ms_id], [value])[0]
            refresh_stock_resp = self._session.put(
                f"{settings.wb_api_url}api/v3/stocks/{self.warehouse_id}",
                json={
                    "stocks": [
                        {
                            "sku": ms_items.barcodes,
                            "amount": value,
                        },
                    ]
                },
                timeout=5,
            )
            refresh_stock_resp.raise_for_status()
            self._logger.info(f"Wildberries: {ms_id} stock is refreshed")
            return True
        except HTTPError as e:
            self._logger.error(
                f"Wildberries: {ms_id} stock is not refreshed. Error: {e}"
            )
            raise e

    def refresh_stocks(self, ms_ids: List[str], values: List[int]):
        try:
            json_data = []
            if len(ms_ids) != len(values):
                raise ValueError("ids and values should have the same length")
            if len(ms_ids) > settings.WB_ITEMS_REFRESH_LIMIT:
                chunks_ids, chunks_values = self.get_chunks(ms_ids, values)
                for chunk_ids, chunk_values in zip(chunks_ids, chunks_values):
                    self.refresh_stocks(chunk_ids, chunk_values)

            for item in self._get_mapped_data(ms_ids, values):
                json_data.append(
                    {
                        "sku": item.barcodes,
                        "amount": item.value,
                    }
                )
            refresh_stocks_resp = self._session.put(
                f"{settings.wb_api_url}api/v3/stocks/{self.warehouse_id}",
                json={
                    "stocks": json_data,
                },
                timeout=5,
            )
            refresh_stocks_resp.raise_for_status()
            return True
        except HTTPError as e:
            self._logger.error(
                f"Wildberries: {ms_ids} stock is not refreshed. Error: {e}"
            )
            raise e

    def get_price(self):
        prices = self._session.get(
            f"{settings.wb_api_url}public/api/v1/info", timeout=5
        )
        return {price["nmId"]: price["price"] for price in prices.json()}

    def refresh_price(self, ms_id: str, value: int):
        try:
            ms_items = self._get_mapped_data([ms_id], [value])[0]

            initial_price = self.get_price().get(ms_items.nm_id)

            self._update_prices(
                [
                    WbUpdateItem(
                        **ms_items.dict(),
                        current_value=initial_price,
                    )
                ]
            )
            return True
        except HTTPError as e:
            self._logger.error(
                f"Wildberries: {ms_id} price is not refreshed. Error: {e}"
            )
            raise e

    def refresh_prices(self, ms_ids: List[str], values: List[int]):
        if len(ms_ids) != len(values):
            raise ValueError("ids and values should have the same length")

        if len(ms_ids) > settings.WB_ITEMS_REFRESH_LIMIT:
            chunks_ids, chunks_values = self.get_chunks(ms_ids, values)
            for chunk_ids, chunk_values in zip(chunks_ids, chunks_values):
                self.refresh_price(chunk_ids, chunk_values)

        initial_prices = self.get_price()
        items_to_reprice = []
        for item in self._get_mapped_data(ms_ids, values):
            items_to_reprice.append(
                WbUpdateItem(
                    **item.dict(),
                    current_value=initial_prices.get(item.nm_id),
                )
            )

        self._update_prices(items_to_reprice)
        return True

    def _update_prices(self, items: List[WbUpdateItem]):
        items_to_reprice: List[WbUpdateItem] = []
        json_data = []
        for item in items:
            if item.current_value * 2 < item.value:
                json_data.append(
                    {
                        "nmId": item.nm_id,
                        "price": item.current_value * 2,
                    },
                )
                items_to_reprice.append(
                    WbUpdateItem(
                        ms_id=item.ms_id,
                        barcodes=item.barcodes,
                        nm_id=item.nm_id,
                        name=item.name,
                        value=item.value,
                        current_value=item.current_value * 2,
                    )
                )
            else:
                json_data.append(
                    {
                        "nmId": item.nm_id,
                        "price": item.value,
                    },
                )
        try:
            price_update_resp = self._session.post(
                f"{settings.wb_api_url}public/api/v1/prices",
                json=json_data,
                timeout=5,
            )
            price_update_resp.raise_for_status()
            self._logger.info(
                f"response: {price_update_resp.status_code} {price_update_resp.json()}"
            )
        except HTTPError as e:
            self._logger.error(f"Wildberries: prices are not refreshed. Error: {e}")
            raise e
        if items_to_reprice:
            self._update_prices(items_to_reprice)
        return True

    def refresh_status(self, wb_order_id: int, status_name: str, supply_id: int = None):
        try:
            match status_name:
                case "confirm":
                    supply_id = supply_id or self._session.post(
                        f"{settings.wb_api_url}api/v3/supplies",
                        json={"name": f"supply_order{wb_order_id}"},
                        timeout=5,
                    ).json().get("id")
                    add_order_to_supply_resp = requests.patch(
                        f"{settings.wb_api_url}api/v3/supplies{supply_id}/orders/{wb_order_id}",
                    )
                    add_order_to_supply_resp.raise_for_status()
                case "cancel":
                    cancel_order_resp = requests.patch(
                        f"{settings.wb_api_url}api/v3/supplies/{wb_order_id}/cancel"
                    )
                    cancel_order_resp.raise_for_status()
                case _:
                    raise InvalidStatusException(
                        f"{status_name} is not valid status name"
                    )
        except HTTPError as e:
            self._logger.error(
                f"Wildberries: {wb_order_id} status is not refreshed. Error: {e}"
            )
            raise e
        return True

    def refresh_statuses(self, wb_order_ids: List[int], statuses: List[str]):
        if len(wb_order_ids) != len(statuses):
            raise ValueError("ids and statuses should have the same length")

        try:
            new_supply = self._session.post(
                f"{settings.wb_api_url}api/v3/supplies",
                json={"name": "supply_orders"},
                timeout=5,
            ).json()
        except HTTPError as e:
            self._logger.error(f"Wildberries: can't create new supply. Error: {e}")
            raise e
        for wb_order_id, status in zip(wb_order_ids, statuses):
            self.refresh_status(
                wb_order_id=wb_order_id,
                status_name=status,
                supply_id=new_supply.get("id"),
            )

    def _get_mapped_data(self, ms_ids: List[str], values: List[int]) -> List[MsItem]:
        ms_items = requests.get(
            f"{self.bgd_mapping_url}", params={"ms_id": ",".join(ms_ids)}
        )

        if len(ms_ids) == 1:
            return [MsItem(**ms_items.json()[0], value=values[0])]

        id_value_map = dict(zip(ms_ids, values))

        mapped_data = []
        for item in ms_items.json():
            value = id_value_map.get(item["ms_id"])
            item["value"] = value
            mapped_data.append(MsItem(**item))
        return mapped_data

    @staticmethod
    def get_chunks(ids, values):
        chunks_ids = [
            ids[i : i + settings.WB_ITEMS_REFRESH_LIMIT]
            for i in range(0, len(ids), settings.WB_ITEMS_REFRESH_LIMIT)
        ]
        chunks_values = [
            values[i : i + settings.WB_ITEMS_REFRESH_LIMIT]
            for i in range(0, len(values), settings.WB_ITEMS_REFRESH_LIMIT)
        ]
        return chunks_ids, chunks_values
