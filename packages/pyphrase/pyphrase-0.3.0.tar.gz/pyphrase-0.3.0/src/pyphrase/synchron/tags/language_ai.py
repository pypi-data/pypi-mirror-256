from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import ConsumedMtusDto


class LanguageAiOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def getConsumedMtus(
        self,
        phrase_token: Optional[str] = None,
    ) -> ConsumedMtusDto:
        """
        Total amount of consumed MTUs in the current month


        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ConsumedMtusDto
        """
        endpoint = "/api2/v1/mtuUsage"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ConsumedMtusDto(**r)
