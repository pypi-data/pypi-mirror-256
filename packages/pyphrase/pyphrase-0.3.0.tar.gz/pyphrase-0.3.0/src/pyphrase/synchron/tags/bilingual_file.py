from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    ComparedSegmentsDto,
    InputStream,
    ProjectJobPartsDto,
    UploadBilingualFileRequestDto,
)


class BilingualFileOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def convertBilingualFile(
        self, body: InputStream, to: str, frm: str, phrase_token: Optional[str] = None
    ) -> bytes:
        """
        Convert bilingual file

        :param body: InputStream (required), body.
        :param to: string (required), query.
        :param frm: string (required), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = "/api2/v1/bilingualFiles/convert"
        params = {"from": frm, "to": to}

        files = None
        payload = body

        r = self.client.post_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    def compareBilingualFile(
        self,
        body: InputStream,
        workflowLevel: int = "1",
        phrase_token: Optional[str] = None,
    ) -> ComparedSegmentsDto:
        """
        Compare bilingual file
        Compares bilingual file to job state. Returns list of compared segments.
        :param body: InputStream (required), body.
        :param workflowLevel: integer (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ComparedSegmentsDto
        """
        endpoint = "/api2/v1/bilingualFiles/compare"
        params = {"workflowLevel": workflowLevel}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ComparedSegmentsDto(**r)

    def getPreviewFile(
        self, body: InputStream, phrase_token: Optional[str] = None
    ) -> bytes:
        """
        Download preview
        Supports mxliff format
        :param body: InputStream (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = "/api2/v1/bilingualFiles/preview"
        params = {}

        files = None
        payload = body

        r = self.client.post_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    def uploadBilingualFileV2(
        self,
        multipart: UploadBilingualFileRequestDto,
        saveToTransMemory: str = "Confirmed",
        setCompleted: bool = "False",
        phrase_token: Optional[str] = None,
    ) -> ProjectJobPartsDto:
        """
        Upload bilingual file
        Returns updated job parts and projects
        :param multipart: UploadBilingualFileRequestDto (required), body. Multipart request with files.
        :param saveToTransMemory: string (optional), query.
        :param setCompleted: boolean (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectJobPartsDto
        """
        endpoint = "/api2/v2/bilingualFiles"
        params = {"saveToTransMemory": saveToTransMemory, "setCompleted": setCompleted}

        files = None
        payload = multipart

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectJobPartsDto(**r)
