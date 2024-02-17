from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    CreateWebHookDto,
    PageDtoWebhookCallDto,
    PageDtoWebHookDtoV2,
    ReplayRequestDto,
    WebHookDtoV2,
    WebhookPreviewsDto,
)


class WebhookOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getWebhookCallsList(
        self,
        parentUid: str = None,
        webhookUid: str = None,
        status: str = None,
        events: List[str] = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoWebhookCallDto:
        """
        Lists webhook calls

        :param parentUid: string (optional), query. UID of parent webhook call to filter by.
        :param webhookUid: string (optional), query. UID of Webhook to filter by.
        :param status: string (optional), query. Status of Webhook calls to filter by.
        :param events: array (optional), query. List of Webhook events to filter by.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoWebhookCallDto
        """
        endpoint = "/api2/v1/webhooksCalls"
        params = {
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "events": events,
            "status": status,
            "webhookUid": webhookUid,
            "parentUid": parentUid,
        }

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoWebhookCallDto(**r)

    async def replayWebhookCalls(
        self, body: ReplayRequestDto, phrase_token: Optional[str] = None
    ) -> None:
        """
        Replay webhook calls
        Replays given list of Webhook Calls in specified order in the request
        :param body: ReplayRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = "/api2/v1/webhooksCalls/replay"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def replayLast(
        self,
        status: str = None,
        events: List[str] = None,
        numberOfCalls: int = "5",
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Replay last webhook calls
        Replays specified number of last Webhook calls from oldest to the newest one
        :param status: string (optional), query. Status of Webhook calls to filter by.
        :param events: array (optional), query. List of Webhook events to filter by.
        :param numberOfCalls: integer (optional), query. Number of calls to be replayed.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = "/api2/v1/webhooksCalls/replay/latest"
        params = {"numberOfCalls": numberOfCalls, "events": events, "status": status}

        files = None
        payload = None

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def getWebHookList_1(
        self,
        sortField: str = None,
        modifiedBy: List[str] = None,
        createdBy: List[str] = None,
        events: List[str] = None,
        url: str = None,
        status: str = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        sortTrend: str = "ASC",
        phrase_token: Optional[str] = None,
    ) -> PageDtoWebHookDtoV2:
        """
        Lists webhooks

        :param sortField: string (optional), query. Sort by this field.
        :param modifiedBy: array (optional), query. Filter by webhook updaters UIDs.
        :param createdBy: array (optional), query. Filter by webhook creators UIDs.
        :param events: array (optional), query. Filter by webhook events, any match is included.
        :param url: string (optional), query. Filter by webhook URL.
        :param status: string (optional), query. Filter by enabled/disabled status.
        :param name: string (optional), query. Filter by webhook name.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.
        :param sortTrend: string (optional), query. Sort direction.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoWebHookDtoV2
        """
        endpoint = "/api2/v2/webhooks"
        params = {
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "name": name,
            "status": status,
            "url": url,
            "events": events,
            "createdBy": createdBy,
            "modifiedBy": modifiedBy,
            "sortField": sortField,
            "sortTrend": sortTrend,
        }

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoWebHookDtoV2(**r)

    async def createWebHook_1(
        self, body: CreateWebHookDto, phrase_token: Optional[str] = None
    ) -> WebHookDtoV2:
        """
        Create webhook

        :param body: CreateWebHookDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: WebHookDtoV2
        """
        endpoint = "/api2/v2/webhooks"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return WebHookDtoV2(**r)

    async def getWebHook_1(
        self, webHookUid: str, phrase_token: Optional[str] = None
    ) -> WebHookDtoV2:
        """
        Get webhook

        :param webHookUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: WebHookDtoV2
        """
        endpoint = f"/api2/v2/webhooks/{webHookUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return WebHookDtoV2(**r)

    async def updateWebHook_1(
        self,
        webHookUid: str,
        body: CreateWebHookDto,
        phrase_token: Optional[str] = None,
    ) -> WebHookDtoV2:
        """
        Edit webhook

        :param webHookUid: string (required), path.
        :param body: CreateWebHookDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: WebHookDtoV2
        """
        endpoint = f"/api2/v2/webhooks/{webHookUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return WebHookDtoV2(**r)

    async def deleteWebHook_1(
        self, webHookUid: str, phrase_token: Optional[str] = None
    ) -> None:
        """
        Delete webhook

        :param webHookUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v2/webhooks/{webHookUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def getWebhookPreviews(
        self, events: List[str] = None, phrase_token: Optional[str] = None
    ) -> WebhookPreviewsDto:
        """
        Get webhook body previews

        :param events: array (optional), query. Filter by webhook events.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: WebhookPreviewsDto
        """
        endpoint = "/api2/v2/webhooks/previews"
        params = {"events": events}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return WebhookPreviewsDto(**r)

    async def sendTestWebhook(
        self, webhookUid: str, event: str, phrase_token: Optional[str] = None
    ) -> None:
        """
        Send test webhook

        :param webhookUid: string (required), path. UID of the webhook.
        :param event: string (required), query. Event of test webhook.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v2/webhooks/{webhookUid}/test"
        params = {"event": event}

        files = None
        payload = None

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return
