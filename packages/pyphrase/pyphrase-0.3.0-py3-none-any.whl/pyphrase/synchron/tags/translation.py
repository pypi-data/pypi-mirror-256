from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    AsyncRequestWrapperDto,
    AsyncRequestWrapperV2Dto,
    HumanTranslateJobsDto,
    MachineTranslateResponse,
    PreTranslateJobsV3Dto,
    TranslationRequestDto,
)


class TranslationOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def humanTranslate(
        self,
        projectUid: str,
        body: HumanTranslateJobsDto,
        phrase_token: Optional[str] = None,
    ) -> AsyncRequestWrapperDto:
        """
        Human translate (Gengo or Unbabel)

        :param projectUid: string (required), path.
        :param body: HumanTranslateJobsDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AsyncRequestWrapperDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/humanTranslate"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AsyncRequestWrapperDto(**r)

    def machineTranslationJob(
        self,
        jobUid: str,
        projectUid: str,
        body: TranslationRequestDto,
        phrase_token: Optional[str] = None,
    ) -> MachineTranslateResponse:
        """
        Translate using machine translation
        Configured machine translate settings is used
        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: TranslationRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: MachineTranslateResponse
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/translations/translateWithMachineTranslation"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return MachineTranslateResponse(**r)

    def preTranslateV3(
        self,
        projectUid: str,
        body: PreTranslateJobsV3Dto,
        phrase_token: Optional[str] = None,
    ) -> AsyncRequestWrapperV2Dto:
        """
        Pre-translate job

        :param projectUid: string (required), path.
        :param body: PreTranslateJobsV3Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AsyncRequestWrapperV2Dto
        """
        endpoint = f"/api2/v3/projects/{projectUid}/jobs/preTranslate"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AsyncRequestWrapperV2Dto(**r)
