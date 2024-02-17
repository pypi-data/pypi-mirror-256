from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    CreateCustomFieldDto,
    CustomFieldDto,
    PageDtoCustomFieldDto,
    PageDtoCustomFieldOptionDto,
)


class CustomFieldsOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def getCustomField(
        self,
        fieldUid: str,
        phrase_token: Optional[str] = None,
    ) -> CustomFieldDto:
        """
        Get custom field

        :param fieldUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: CustomFieldDto
        """
        endpoint = f"/api2/v1/customFields/{fieldUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return CustomFieldDto(**r)

    def getCustomFieldList(
        self,
        sortField: str = None,
        required: bool = None,
        uids: List[str] = None,
        modifiedBy: List[str] = None,
        createdBy: List[str] = None,
        types: List[str] = None,
        allowedEntities: List[str] = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        sortTrend: str = "ASC",
        phrase_token: Optional[str] = None,
    ) -> PageDtoCustomFieldDto:
        """
        Lists custom fields

        :param sortField: string (optional), query. Sort by this field.
        :param required: boolean (optional), query. Filter by custom field required parameter.
        :param uids: array (optional), query. Filter by custom field UIDs.
        :param modifiedBy: array (optional), query. Filter by custom field updaters UIDs.
        :param createdBy: array (optional), query. Filter by custom field creators UIDs.
        :param types: array (optional), query. Filter by custom field types.
        :param allowedEntities: array (optional), query. Filter by custom field allowed entities.
        :param name: string (optional), query. Filter by custom field name.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.
        :param sortTrend: string (optional), query. Sort direction.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoCustomFieldDto
        """
        endpoint = "/api2/v1/customFields"
        params = {
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "name": name,
            "allowedEntities": allowedEntities,
            "types": types,
            "createdBy": createdBy,
            "modifiedBy": modifiedBy,
            "uids": uids,
            "required": required,
            "sortField": sortField,
            "sortTrend": sortTrend,
        }

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoCustomFieldDto(**r)

    def createCustomField(
        self,
        body: CreateCustomFieldDto,
        phrase_token: Optional[str] = None,
    ) -> CustomFieldDto:
        """
        Create custom field

        :param body: CreateCustomFieldDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: CustomFieldDto
        """
        endpoint = "/api2/v1/customFields"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return CustomFieldDto(**r)

    def getCustomFieldOptionList(
        self,
        fieldUid: str,
        sortField: str = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        sortTrend: str = "ASC",
        phrase_token: Optional[str] = None,
    ) -> PageDtoCustomFieldOptionDto:
        """
        Lists options of custom field

        :param fieldUid: string (required), path.
        :param sortField: string (optional), query. Sort by this field.
        :param name: string (optional), query. Filter by option name.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.
        :param sortTrend: string (optional), query. Sort direction.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoCustomFieldOptionDto
        """
        endpoint = f"/api2/v1/customFields/{fieldUid}/options"
        params = {
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "name": name,
            "sortField": sortField,
            "sortTrend": sortTrend,
        }

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoCustomFieldOptionDto(**r)
