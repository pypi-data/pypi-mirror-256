from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import LanguageListDto


class SupportedLanguagesOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def listOfLanguages(
        self,
        active: bool = None,
        phrase_token: Optional[str] = None,
    ) -> LanguageListDto:
        """
        List supported languages

        :param active: boolean (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LanguageListDto
        """
        endpoint = "/api2/v1/languages"
        params = {"active": active}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LanguageListDto(**r)
