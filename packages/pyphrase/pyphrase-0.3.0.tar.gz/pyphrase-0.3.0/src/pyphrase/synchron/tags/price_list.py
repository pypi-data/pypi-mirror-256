from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    PageDtoTranslationPriceListDto,
    PageDtoTranslationPriceSetDto,
    TranslationPriceListCreateDto,
    TranslationPriceListDto,
    TranslationPriceSetBulkDeleteDto,
    TranslationPriceSetBulkMinimumPricesDto,
    TranslationPriceSetBulkPricesDto,
    TranslationPriceSetCreateDto,
    TranslationPriceSetListDto,
)


class PriceListOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def getPriceList(
        self,
        priceListUid: str,
        phrase_token: Optional[str] = None,
    ) -> TranslationPriceListDto:
        """
        Get price list

        :param priceListUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TranslationPriceListDto
        """
        endpoint = f"/api2/v1/priceLists/{priceListUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TranslationPriceListDto(**r)

    def updatePriceList(
        self,
        priceListUid: str,
        body: TranslationPriceListCreateDto,
        phrase_token: Optional[str] = None,
    ) -> TranslationPriceListDto:
        """
        Update price list

        :param priceListUid: string (required), path.
        :param body: TranslationPriceListCreateDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TranslationPriceListDto
        """
        endpoint = f"/api2/v1/priceLists/{priceListUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TranslationPriceListDto(**r)

    def deletePriceList(
        self,
        priceListUid: str,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete price list

        :param priceListUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/priceLists/{priceListUid}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def getListOfPriceList(
        self,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoTranslationPriceListDto:
        """
        List price lists

        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoTranslationPriceListDto
        """
        endpoint = "/api2/v1/priceLists"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoTranslationPriceListDto(**r)

    def createPriceList(
        self,
        body: TranslationPriceListCreateDto,
        phrase_token: Optional[str] = None,
    ) -> TranslationPriceListDto:
        """
        Create price list

        :param body: TranslationPriceListCreateDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TranslationPriceListDto
        """
        endpoint = "/api2/v1/priceLists"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TranslationPriceListDto(**r)

    def getPricesWithWorkflowSteps(
        self,
        priceListUid: str,
        targetLanguages: List[str] = None,
        sourceLanguages: List[str] = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoTranslationPriceSetDto:
        """
        List price sets

        :param priceListUid: string (required), path.
        :param targetLanguages: array (optional), query.
        :param sourceLanguages: array (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoTranslationPriceSetDto
        """
        endpoint = f"/api2/v1/priceLists/{priceListUid}/priceSets"
        params = {
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "sourceLanguages": sourceLanguages,
            "targetLanguages": targetLanguages,
        }

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoTranslationPriceSetDto(**r)

    def createLanguagePair(
        self,
        priceListUid: str,
        body: TranslationPriceSetCreateDto,
        phrase_token: Optional[str] = None,
    ) -> TranslationPriceSetListDto:
        """
        Add language pairs

        :param priceListUid: string (required), path.
        :param body: TranslationPriceSetCreateDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TranslationPriceSetListDto
        """
        endpoint = f"/api2/v1/priceLists/{priceListUid}/priceSets"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TranslationPriceSetListDto(**r)

    def deleteLanguagePairs(
        self,
        priceListUid: str,
        body: TranslationPriceSetBulkDeleteDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Remove language pairs

        :param priceListUid: string (required), path.
        :param body: TranslationPriceSetBulkDeleteDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/priceLists/{priceListUid}/priceSets"
        params = {}

        files = None
        payload = body

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def deleteLanguagePair(
        self,
        targetLanguage: str,
        sourceLanguage: str,
        priceListUid: str,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Remove language pair

        :param targetLanguage: string (required), path.
        :param sourceLanguage: string (required), path.
        :param priceListUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/priceLists/{priceListUid}/priceSets/{sourceLanguage}/{targetLanguage}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def setMinimumPriceForSet(
        self,
        priceListUid: str,
        body: TranslationPriceSetBulkMinimumPricesDto,
        phrase_token: Optional[str] = None,
    ) -> TranslationPriceListDto:
        """
        Edit minimum prices

        :param priceListUid: string (required), path.
        :param body: TranslationPriceSetBulkMinimumPricesDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TranslationPriceListDto
        """
        endpoint = f"/api2/v1/priceLists/{priceListUid}/priceSets/minimumPrices"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TranslationPriceListDto(**r)

    def setPrices(
        self,
        priceListUid: str,
        body: TranslationPriceSetBulkPricesDto,
        phrase_token: Optional[str] = None,
    ) -> TranslationPriceListDto:
        """
        Edit prices
        If object contains only price, all languages and workflow steps will be updated
        :param priceListUid: string (required), path.
        :param body: TranslationPriceSetBulkPricesDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TranslationPriceListDto
        """
        endpoint = f"/api2/v1/priceLists/{priceListUid}/priceSets/prices"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TranslationPriceListDto(**r)
