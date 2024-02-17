from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    AddCommentDto,
    AddLqaCommentResultDto,
    AddPlainCommentResultDto,
    ConversationListDto,
    CreateLqaConversationDto,
    CreatePlainConversationDto,
    EditLqaConversationDto,
    EditPlainConversationDto,
    FindConversationsDto,
    LQAConversationDto,
    LQAConversationsListDto,
    PlainConversationDto,
    PlainConversationsListDto,
)


class ConversationsOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def listAllConversations(
        self,
        jobUid: str,
        since: str = None,
        includeDeleted: bool = "False",
        phrase_token: Optional[str] = None,
    ) -> ConversationListDto:
        """
        List all conversations

        :param jobUid: string (required), path.
        :param since: string (optional), query.
        :param includeDeleted: boolean (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ConversationListDto
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations"
        params = {"includeDeleted": includeDeleted, "since": since}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ConversationListDto(**r)

    async def findConversations(
        self, body: FindConversationsDto, phrase_token: Optional[str] = None
    ) -> ConversationListDto:
        """
        Find all conversation

        :param body: FindConversationsDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ConversationListDto
        """
        endpoint = "/api2/v1/jobs/conversations/find"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ConversationListDto(**r)

    async def deleteLQAComment(
        self,
        commentId: str,
        conversationId: str,
        jobUid: str,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete LQA comment

        :param commentId: string (required), path.
        :param conversationId: string (required), path.
        :param jobUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/lqas/{conversationId}/comments/{commentId}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def getLQAConversation(
        self, conversationId: str, jobUid: str, phrase_token: Optional[str] = None
    ) -> LQAConversationDto:
        """
        Get LQA conversation

        :param conversationId: string (required), path.
        :param jobUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LQAConversationDto
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/lqas/{conversationId}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LQAConversationDto(**r)

    async def deleteLQAConversation(
        self, conversationId: str, jobUid: str, phrase_token: Optional[str] = None
    ) -> None:
        """
        Delete LQA conversation

        :param conversationId: string (required), path.
        :param jobUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/lqas/{conversationId}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def listLQAConversations(
        self,
        jobUid: str,
        since: str = None,
        includeDeleted: bool = "False",
        phrase_token: Optional[str] = None,
    ) -> LQAConversationsListDto:
        """
        List LQA conversations

        :param jobUid: string (required), path.
        :param since: string (optional), query.
        :param includeDeleted: boolean (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LQAConversationsListDto
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/lqas"
        params = {"includeDeleted": includeDeleted, "since": since}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LQAConversationsListDto(**r)

    async def getPlainConversation(
        self, conversationId: str, jobUid: str, phrase_token: Optional[str] = None
    ) -> PlainConversationDto:
        """
        Get plain conversation

        :param conversationId: string (required), path.
        :param jobUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PlainConversationDto
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/plains/{conversationId}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PlainConversationDto(**r)

    async def updatePlainConversation(
        self,
        conversationId: str,
        jobUid: str,
        body: EditPlainConversationDto,
        phrase_token: Optional[str] = None,
    ) -> PlainConversationDto:
        """
        Edit plain conversation

        :param conversationId: string (required), path.
        :param jobUid: string (required), path.
        :param body: EditPlainConversationDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PlainConversationDto
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/plains/{conversationId}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PlainConversationDto(**r)

    async def deletePlainConversation(
        self, conversationId: str, jobUid: str, phrase_token: Optional[str] = None
    ) -> None:
        """
        Delete plain conversation

        :param conversationId: string (required), path.
        :param jobUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/plains/{conversationId}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def listPlainConversations(
        self,
        jobUid: str,
        since: str = None,
        includeDeleted: bool = "False",
        phrase_token: Optional[str] = None,
    ) -> PlainConversationsListDto:
        """
        List plain conversations

        :param jobUid: string (required), path.
        :param since: string (optional), query.
        :param includeDeleted: boolean (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PlainConversationsListDto
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/plains"
        params = {"includeDeleted": includeDeleted, "since": since}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PlainConversationsListDto(**r)

    async def deletePlainComment(
        self,
        commentId: str,
        conversationId: str,
        jobUid: str,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete plain comment

        :param commentId: string (required), path.
        :param conversationId: string (required), path.
        :param jobUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/plains/{conversationId}/comments/{commentId}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def createLqaConversation_1(
        self,
        jobUid: str,
        body: CreateLqaConversationDto,
        phrase_token: Optional[str] = None,
    ) -> LQAConversationDto:
        """
        Create LQA conversation

        :param jobUid: string (required), path.
        :param body: CreateLqaConversationDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LQAConversationDto
        """
        endpoint = f"/api2/v2/jobs/{jobUid}/conversations/lqas"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LQAConversationDto(**r)

    async def updateLqaConversation_1(
        self,
        conversationId: str,
        jobUid: str,
        body: EditLqaConversationDto,
        phrase_token: Optional[str] = None,
    ) -> LQAConversationDto:
        """
        Update LQA conversation

        :param conversationId: string (required), path.
        :param jobUid: string (required), path.
        :param body: EditLqaConversationDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LQAConversationDto
        """
        endpoint = f"/api2/v2/jobs/{jobUid}/conversations/lqas/{conversationId}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LQAConversationDto(**r)

    async def addLQAComment_1(
        self,
        conversationId: str,
        jobUid: str,
        body: AddCommentDto,
        phrase_token: Optional[str] = None,
    ) -> AddLqaCommentResultDto:
        """
        Add LQA comment

        :param conversationId: string (required), path.
        :param jobUid: string (required), path.
        :param body: AddCommentDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AddLqaCommentResultDto
        """
        endpoint = (
            f"/api2/v2/jobs/{jobUid}/conversations/lqas/{conversationId}/comments"
        )
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AddLqaCommentResultDto(**r)

    async def updateLQAComment_1(
        self,
        commentId: str,
        conversationId: str,
        jobUid: str,
        body: AddCommentDto,
        phrase_token: Optional[str] = None,
    ) -> LQAConversationDto:
        """
        Edit LQA comment

        :param commentId: string (required), path.
        :param conversationId: string (required), path.
        :param jobUid: string (required), path.
        :param body: AddCommentDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LQAConversationDto
        """
        endpoint = f"/api2/v2/jobs/{jobUid}/conversations/lqas/{conversationId}/comments/{commentId}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LQAConversationDto(**r)

    async def addPlainComment_2(
        self,
        conversationId: str,
        jobUid: str,
        body: AddCommentDto,
        phrase_token: Optional[str] = None,
    ) -> AddPlainCommentResultDto:
        """
        Add plain comment

        :param conversationId: string (required), path.
        :param jobUid: string (required), path.
        :param body: AddCommentDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AddPlainCommentResultDto
        """
        endpoint = (
            f"/api2/v3/jobs/{jobUid}/conversations/plains/{conversationId}/comments"
        )
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AddPlainCommentResultDto(**r)

    async def createSegmentTargetConversation_1(
        self,
        jobUid: str,
        body: CreatePlainConversationDto,
        phrase_token: Optional[str] = None,
    ) -> PlainConversationDto:
        """
        Create plain conversation

        :param jobUid: string (required), path.
        :param body: CreatePlainConversationDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PlainConversationDto
        """
        endpoint = f"/api2/v3/jobs/{jobUid}/conversations/plains"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PlainConversationDto(**r)

    async def updatePlainComment_1(
        self,
        commentId: str,
        conversationId: str,
        jobUid: str,
        body: AddCommentDto,
        phrase_token: Optional[str] = None,
    ) -> PlainConversationDto:
        """
        Edit plain comment

        :param commentId: string (required), path.
        :param conversationId: string (required), path.
        :param jobUid: string (required), path.
        :param body: AddCommentDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PlainConversationDto
        """
        endpoint = f"/api2/v3/jobs/{jobUid}/conversations/plains/{conversationId}/comments/{commentId}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PlainConversationDto(**r)
