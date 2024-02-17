from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import ProviderListDtoV2


class ProviderOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def listProviders_4(
        self,
        jobUid: str,
        projectUid: str,
        phrase_token: Optional[str] = None,
    ) -> ProviderListDtoV2:
        """
        Get suggested providers

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProviderListDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/jobs/{jobUid}/providers/suggest"
        params = {}

        files = None
        payload = None

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProviderListDtoV2(**r)
