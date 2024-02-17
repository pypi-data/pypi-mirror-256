from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import PageDtoXmlAssistantProfileListDto


class XmlAssistantOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def listXmlAssistantProfiles(
        self,
        order: str = None,
        sort: str = None,
        search: str = None,
        updatedAt: str = None,
        createdAt: str = None,
        updatedBy: str = None,
        createdBy: str = None,
        description: str = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoXmlAssistantProfileListDto:
        """
        Get XML assistant profiles for organization

        :param order: string (optional), query.
        :param sort: string (optional), query.
        :param search: string (optional), query.
        :param updatedAt: string (optional), query.
        :param createdAt: string (optional), query.
        :param updatedBy: string (optional), query.
        :param createdBy: string (optional), query.
        :param description: string (optional), query.
        :param name: string (optional), query.
        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoXmlAssistantProfileListDto
        """
        endpoint = "/api2/v1/xmlAssistantProfiles"
        params = {
            "name": name,
            "description": description,
            "createdBy": createdBy,
            "updatedBy": updatedBy,
            "createdAt": createdAt,
            "updatedAt": updatedAt,
            "search": search,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "sort": sort,
            "order": order,
        }

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoXmlAssistantProfileListDto(**r)
