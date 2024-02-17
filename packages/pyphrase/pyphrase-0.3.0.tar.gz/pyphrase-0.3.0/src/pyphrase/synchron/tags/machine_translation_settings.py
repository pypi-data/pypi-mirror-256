from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    MachineTranslateSettingsPbmDto,
    MachineTranslateStatusDto,
    PageDtoMachineTranslateSettingsPbmDto,
    TypesDto,
)


class MachineTranslationSettingsOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def getStatus(
        self,
        mtsUid: str,
        phrase_token: Optional[str] = None,
    ) -> MachineTranslateStatusDto:
        """
        Get status of machine translate engine

        :param mtsUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: MachineTranslateStatusDto
        """
        endpoint = f"/api2/v1/machineTranslateSettings/{mtsUid}/status"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return MachineTranslateStatusDto(**r)

    def getList(
        self,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        sort: str = "NAME",
        order: str = "asc",
        phrase_token: Optional[str] = None,
    ) -> PageDtoMachineTranslateSettingsPbmDto:
        """
        List machine translate settings

        :param name: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.
        :param sort: string (optional), query. Sorting field.
        :param order: string (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoMachineTranslateSettingsPbmDto
        """
        endpoint = "/api2/v1/machineTranslateSettings"
        params = {
            "name": name,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "sort": sort,
            "order": order,
        }

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoMachineTranslateSettingsPbmDto(**r)

    def getMTSettings(
        self,
        mtsUid: str,
        phrase_token: Optional[str] = None,
    ) -> MachineTranslateSettingsPbmDto:
        """
        Get machine translate settings

        :param mtsUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: MachineTranslateSettingsPbmDto
        """
        endpoint = f"/api2/v1/machineTranslateSettings/{mtsUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return MachineTranslateSettingsPbmDto(**r)

    def getThirdPartyEnginesList(
        self,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        sort: str = "NAME",
        order: str = "asc",
        phrase_token: Optional[str] = None,
    ) -> PageDtoMachineTranslateSettingsPbmDto:
        """
        List third party machine translate settings

        :param name: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 100, default 50.
        :param sort: string (optional), query. Sorting field.
        :param order: string (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoMachineTranslateSettingsPbmDto
        """
        endpoint = "/api2/v1/machineTranslateSettings/thirdPartyEngines"
        params = {
            "name": name,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "sort": sort,
            "order": order,
        }

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoMachineTranslateSettingsPbmDto(**r)

    def getMTTypes(
        self,
        phrase_token: Optional[str] = None,
    ) -> TypesDto:
        """
        Get machine translate settings types


        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TypesDto
        """
        endpoint = "/api2/v1/machineTranslateSettings/types"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TypesDto(**r)
