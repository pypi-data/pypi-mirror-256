from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import ConsumedMtusDto


class LanguageAiOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getConsumedMtus(
        self, phrase_token: Optional[str] = None
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

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ConsumedMtusDto(**r)
