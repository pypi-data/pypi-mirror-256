from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    ImportSettingsCreateDto,
    ImportSettingsDto,
    ImportSettingsEditDto,
    PageDtoImportSettingsReference,
)


class ImportSettingsOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getImportSettings(
        self, phrase_token: Optional[str] = None
    ) -> ImportSettingsDto:
        """
        Get organization's default import settings


        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ImportSettingsDto
        """
        endpoint = "/api2/v1/importSettings/default"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ImportSettingsDto(**r)

    async def getImportSettings_1(
        self, uid: str, phrase_token: Optional[str] = None
    ) -> ImportSettingsDto:
        """
        Get import settings

        :param uid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ImportSettingsDto
        """
        endpoint = f"/api2/v1/importSettings/{uid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ImportSettingsDto(**r)

    async def deleteImportSettings(
        self, uid: str, phrase_token: Optional[str] = None
    ) -> None:
        """
        Delete import settings

        :param uid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/importSettings/{uid}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def listImportSettings(
        self,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoImportSettingsReference:
        """
        List import settings

        :param name: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoImportSettingsReference
        """
        endpoint = "/api2/v1/importSettings"
        params = {"name": name, "pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoImportSettingsReference(**r)

    async def createImportSettings(
        self, body: ImportSettingsCreateDto, phrase_token: Optional[str] = None
    ) -> ImportSettingsDto:
        """
        Create import settings
        Pre-defined import settings is handy for [Create Job](#operation/createJob).
                  See [supported file types](https://wiki.memsource.com/wiki/API_File_Type_List)
        :param body: ImportSettingsCreateDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ImportSettingsDto
        """
        endpoint = "/api2/v1/importSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ImportSettingsDto(**r)

    async def editImportSettings(
        self, body: ImportSettingsEditDto, phrase_token: Optional[str] = None
    ) -> ImportSettingsDto:
        """
        Edit import settings

        :param body: ImportSettingsEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ImportSettingsDto
        """
        endpoint = "/api2/v1/importSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ImportSettingsDto(**r)
