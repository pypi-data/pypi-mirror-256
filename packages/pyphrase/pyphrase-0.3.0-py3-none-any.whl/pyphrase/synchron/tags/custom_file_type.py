from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    CreateCustomFileTypeDto,
    CustomFileTypeDto,
    DeleteCustomFileTypeDto,
    PageDtoCustomFileTypeDto,
    UpdateCustomFileTypeDto,
)


class CustomFileTypeOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def getAllCustomFileType(
        self,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoCustomFileTypeDto:
        """
        Get All Custom file type

        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoCustomFileTypeDto
        """
        endpoint = "/api2/v1/customFileTypes"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoCustomFileTypeDto(**r)

    def createCustomFileTypes(
        self,
        body: CreateCustomFileTypeDto,
        phrase_token: Optional[str] = None,
    ) -> CustomFileTypeDto:
        """
        Create custom file type

        :param body: CreateCustomFileTypeDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: CustomFileTypeDto
        """
        endpoint = "/api2/v1/customFileTypes"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return CustomFileTypeDto(**r)

    def deleteBatchCustomFileType(
        self,
        body: DeleteCustomFileTypeDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete multiple Custom file type

        :param body: DeleteCustomFileTypeDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = "/api2/v1/customFileTypes"
        params = {}

        files = None
        payload = body

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def getCustomFileType(
        self,
        customFileTypeUid: str,
        phrase_token: Optional[str] = None,
    ) -> CustomFileTypeDto:
        """
        Get Custom file type

        :param customFileTypeUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: CustomFileTypeDto
        """
        endpoint = f"/api2/v1/customFileTypes/{customFileTypeUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )
        return CustomFileTypeDto(**r)

    def updateCustomFileType(
        self,
        customFileTypeUid: str,
        body: UpdateCustomFileTypeDto,
        phrase_token: Optional[str] = None,
    ) -> CustomFileTypeDto:
        """
        Update Custom file type

        :param customFileTypeUid: string (required), path.
        :param body: UpdateCustomFileTypeDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: CustomFileTypeDto
        """
        endpoint = f"/api2/v1/customFileTypes/{customFileTypeUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return CustomFileTypeDto(**r)

    def deleteCustomFileType(
        self,
        customFileTypeUid: str,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete Custom file type

        :param customFileTypeUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/customFileTypes/{customFileTypeUid}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def findCustomFileType(
        self,
        fileName: str = None,
        phrase_token: Optional[str] = None,
    ) -> Optional[CustomFileTypeDto]:
        """
        Find custom file type
        If no matching custom file type is found it returns status 200 and empty body.
        :param fileName: string (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: CustomFileTypeDto
        """
        endpoint = "/api2/v1/customFileTypes/find"
        params = {"fileName": fileName}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )
        if r is not None:
            return CustomFileTypeDto(**r)
        else:
            return
