from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    CreateReferenceFilesRequest,
    ProjectReferenceFilesRequestDto,
    ReferenceFilePageDto,
    ReferenceFilesDto,
    UserReferencesDto,
)


class ProjectReferenceFileOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def listReferenceFiles(
        self,
        projectUid: str,
        createdBy: str = None,
        dateCreatedSince: str = None,
        filename: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        sort: str = "DATE_CREATED",
        order: str = "DESC",
        phrase_token: Optional[str] = None,
    ) -> ReferenceFilePageDto:
        """
        List project reference files

        :param projectUid: string (required), path.
        :param createdBy: string (optional), query. UID of user.
        :param dateCreatedSince: string (optional), query. date time in ISO 8601 UTC format.
        :param filename: string (optional), query.
        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query.
        :param sort: string (optional), query.
        :param order: string (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ReferenceFilePageDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/references"
        params = {
            "filename": filename,
            "dateCreatedSince": dateCreatedSince,
            "createdBy": createdBy,
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

        return ReferenceFilePageDto(**r)

    async def batchDeleteReferenceFiles(
        self,
        projectUid: str,
        body: ProjectReferenceFilesRequestDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete project reference files (batch)

        :param projectUid: string (required), path.
        :param body: ProjectReferenceFilesRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/references"
        params = {}

        files = None
        payload = body

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def downloadReference(
        self, referenceFileId: str, projectUid: str, phrase_token: Optional[str] = None
    ) -> bytes:
        """
        Download project reference file

        :param referenceFileId: string (required), path.
        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/references/{referenceFileId}"
        params = {}

        files = None
        payload = None

        r = await self.client.get_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    async def batchDownloadReferenceFiles(
        self,
        projectUid: str,
        body: ProjectReferenceFilesRequestDto,
        phrase_token: Optional[str] = None,
    ) -> bytes:
        """
        Download project reference files (batch)

        :param projectUid: string (required), path.
        :param body: ProjectReferenceFilesRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/references/download"
        params = {}

        files = None
        payload = body

        r = await self.client.post_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    async def listReferenceFileCreators(
        self, projectUid: str, userName: str = None, phrase_token: Optional[str] = None
    ) -> UserReferencesDto:
        """
        List project reference file creators
        The result is not paged and returns up to 50 users.
                If the requested user is not included, the search can be narrowed down with the `userName` parameter.
        :param projectUid: string (required), path.
        :param userName: string (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: UserReferencesDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/references/creators"
        params = {"userName": userName}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return UserReferencesDto(**r)

    async def createReferenceFiles(
        self,
        projectUid: str,
        multipart: CreateReferenceFilesRequest,
        phrase_token: Optional[str] = None,
    ) -> ReferenceFilesDto:
        """
                Create project reference files
                The `json` request part allows sending additional data as JSON,
        such as a text note that will be used for all the given reference files.
        In case no `file` parts are sent, only 1 reference is created with the given note.
        Either at least one file must be sent or the note must be specified.
        Example:

        ```
        {
            "note": "Sample text"
        }
        ```
                :param projectUid: string (required), path.
                :param multipart: CreateReferenceFilesRequest (required), body. Multipart request with files and JSON.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: ReferenceFilesDto
        """
        endpoint = f"/api2/v2/projects/{projectUid}/references"
        params = {}

        files = None
        payload = multipart

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ReferenceFilesDto(**r)
