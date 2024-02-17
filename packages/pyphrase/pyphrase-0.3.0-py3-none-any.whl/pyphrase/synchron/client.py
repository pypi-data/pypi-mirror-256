import logging
from json import JSONDecodeError
from typing import Any, Optional

import httpx
from httpx import HTTPStatusError

from ..exceptions import NotAuthenticatedError, UnableToAuthenticateError
from ..models import MemsourceAuthTokenModel
from .tags import (
    AdditionalWorkflowStepOperations,
    AnalysisOperations,
    AsyncRequestOperations,
    AuthenticationOperations,
    BilingualFileOperations,
    BusinessUnitOperations,
    ClientOperations,
    ConnectorOperations,
    ConversationsOperations,
    CostCenterOperations,
    CustomFieldsOperations,
    CustomFileTypeOperations,
    DomainOperations,
    EmailTemplateOperations,
    FileOperations,
    GlossaryOperations,
    ImportSettingsOperations,
    JobOperations,
    LanguageAiOperations,
    LanguageQualityAssessmentOperations,
    MachineTranslationOperations,
    MachineTranslationSettingsOperations,
    MappingOperations,
    NetRateSchemeOperations,
    PriceListOperations,
    ProjectOperations,
    ProjectReferenceFileOperations,
    ProjectTemplateOperations,
    ProviderOperations,
    QualityAssuranceOperations,
    QuoteOperations,
    ScimOperations,
    SegmentationRulesOperations,
    SpellCheckOperations,
    SubdomainOperations,
    SupportedLanguagesOperations,
    TermBaseOperations,
    TranslationMemoryOperations,
    TranslationOperations,
    UserOperations,
    VendorOperations,
    WebhookOperations,
    WorkflowChangesOperations,
    WorkflowStepOperations,
    XmlAssistantOperations,
)

MEMSOURCE_BASE_URL = "https://cloud.memsource.com/web"

logger = logging.getLogger(__name__)


class PhraseTMSException(Exception):
    pass


class PhraseTmsTooManyRequestsError(PhraseTMSException):
    pass


exception_map = {"TOO_MANY_REQUESTS": PhraseTmsTooManyRequestsError}


def sync_get_phrase_tms_token(user: str, pw: str) -> MemsourceAuthTokenModel:
    url = f"{MEMSOURCE_BASE_URL}/api2/v1/auth/login"
    payload = {"userName": user, "password": pw}
    _r = httpx.post(url, json=payload)
    r = _r.json()
    token = r.get("token")
    expires = r.get("expires")

    if token is None:
        error_desc = r.get("errorDescription", "UNKNOWN_ERROR_DESCRIPTION")
        error_code = r.get("errorCode", "UNKNOWN_ERROR_CODE")
        raise UnableToAuthenticateError(
            f"Error code: {error_code}. Error description: {error_desc}"
        )
    else:
        return MemsourceAuthTokenModel(token="ApiToken " + token, expires=expires)


class SyncPhraseTMSClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.additional_workflow_step = AdditionalWorkflowStepOperations(self)
        self.analysis = AnalysisOperations(self)
        self.async_request = AsyncRequestOperations(self)
        self.authentication = AuthenticationOperations(self)
        self.bilingual_file = BilingualFileOperations(self)
        self.business_unit = BusinessUnitOperations(self)
        self.client = ClientOperations(self)
        self.connector = ConnectorOperations(self)
        self.conversations = ConversationsOperations(self)
        self.cost_center = CostCenterOperations(self)
        self.custom_fields = CustomFieldsOperations(self)
        self.custom_file_type = CustomFileTypeOperations(self)
        self.net_rate_scheme = NetRateSchemeOperations(self)
        self.domain = DomainOperations(self)
        self.email_template = EmailTemplateOperations(self)
        self.job = JobOperations(self)
        self.file = FileOperations(self)
        self.glossary = GlossaryOperations(self)
        self.translation_memory = TranslationMemoryOperations(self)
        self.supported_languages = SupportedLanguagesOperations(self)
        self.language_quality_assessment = LanguageQualityAssessmentOperations(self)
        self.quality_assurance = QualityAssuranceOperations(self)
        self.machine_translation_settings = MachineTranslationSettingsOperations(self)
        self.machine_translation = MachineTranslationOperations(self)
        self.mapping = MappingOperations(self)
        self.language_ai = LanguageAiOperations(self)
        self.import_settings = ImportSettingsOperations(self)
        self.project = ProjectOperations(self)
        self.translation = TranslationOperations(self)
        self.term_base = TermBaseOperations(self)
        self.project_reference_file = ProjectReferenceFileOperations(self)
        self.project_template = ProjectTemplateOperations(self)
        self.quote = QuoteOperations(self)
        self.scim = ScimOperations(self)
        self.segmentation_rules = SegmentationRulesOperations(self)
        self.spell_check = SpellCheckOperations(self)
        self.subdomain = SubdomainOperations(self)
        self.price_list = PriceListOperations(self)
        self.user = UserOperations(self)
        self.vendor = VendorOperations(self)
        self.webhook = WebhookOperations(self)
        self.workflow_step = WorkflowStepOperations(self)
        self.xml_assistant = XmlAssistantOperations(self)
        self.workflow_changes = WorkflowChangesOperations(self)
        self.provider = ProviderOperations(self)

    def get_bytestream(
        self,
        path: str,
        phrase_token: Optional[str] = None,
        params: Optional[dict] = None,
        payload: Optional[Any] = None,
        files: Optional[Any] = None,
        headers: Optional[dict] = None,
        content: Optional[bytes] = None,
    ) -> bytes:
        token = phrase_token or self.token
        if token is None:
            raise NotAuthenticatedError

        if params is None:
            params = {}

        url = f"{MEMSOURCE_BASE_URL}{path}"
        header = {"Authorization": token}
        if headers is not None:
            header.update(headers)
        logger.info(url, params)
        r = httpx.get(url, params=params, headers=header, timeout=60.0)

        try:
            r.raise_for_status()
        except HTTPStatusError as exc:
            try:
                loaded_errors = r.json()
                error_code = loaded_errors.get("errorCode")
                error_detail = loaded_errors.get("errorDescription")
                msg = f"Call failed: {url=}, {params=}, {r.status_code=}, {error_code=}, {error_detail=}"
                raise PhraseTMSException(msg)
            except:
                logger.exception(f"Call failed: {r} // {url} - {params}")
                raise Exception from exc

        return r.content

    def post_bytestream(
        self,
        path: str,
        phrase_token: Optional[str] = None,
        params: Optional[dict] = None,
        payload: Optional[Any] = None,
        files: Optional[Any] = None,
        headers: Optional[dict] = None,
        content: Optional[bytes] = None,
    ) -> bytes:
        token = phrase_token or self.token
        if token is None:
            raise NotAuthenticatedError

        if params is None:
            params = {}

        url = f"{MEMSOURCE_BASE_URL}{path}"
        header = {"Authorization": token}
        if headers is not None:
            header.update(headers)

        if payload is not None and type(payload) != dict:
            try:
                payload = payload.dict()
            except Exception as e:
                logger.exception(f"Payload could not be cast as dict: {e}")
                raise Exception from e

        logger.info(url, params)
        r = httpx.post(
            url,
            json=payload,
            headers=header,
            params=params,
            files=files,
            content=content,
            timeout=30.0,
        )

        try:
            r.raise_for_status()
        except HTTPStatusError as exc:
            logger.exception(f"Call failed: {r.content} // {url} - {params}")
            raise Exception from exc

        return r.content

    def get(
        self,
        path: str,
        phrase_token: Optional[str] = None,
        params: Optional[dict] = None,
        payload: Optional[Any] = None,
        files: Optional[Any] = None,
        headers: Optional[dict] = None,
        content: Optional[bytes] = None,
    ) -> dict | None:
        token = phrase_token or self.token
        if token is None:
            raise NotAuthenticatedError

        if params is None:
            params = {}
        params = {k: v for k, v in params.items() if v is not None}

        url = f"{MEMSOURCE_BASE_URL}{path}"
        header = {"Authorization": token}
        if headers is not None:
            header.update(headers)

        logger.info(url)
        resp = httpx.get(url, params=params, headers=header, timeout=30.0)
        try:
            resp.raise_for_status()
        except HTTPStatusError as exc:
            try:
                loaded_errors = resp.json()
                error_code = loaded_errors.get("errorCode")
                error_detail = loaded_errors.get("errorDescription")

                msg = f"Call failed: {url=}, {params=}, {resp.status_code=}, {error_code=}, {error_detail=}"
                raise PhraseTMSException(msg)
            except:
                logger.exception(f"Call failed: {resp} // {url} - {params}")
                raise Exception from exc

        try:
            return resp.json()
        except JSONDecodeError:
            return

    def post(
        self,
        path: str,
        phrase_token: Optional[str] = None,
        params: Optional[dict] = None,
        payload: Optional[Any] = None,
        files: Optional[Any] = None,
        headers: Optional[dict] = None,
        content: Optional[bytes] = None,
    ) -> dict | None:
        token = phrase_token or self.token
        if token is None:
            raise NotAuthenticatedError

        url = f"{MEMSOURCE_BASE_URL}{path}"
        header = {"Authorization": token}
        if headers is not None:
            header.update(headers)

        if payload is not None and type(payload) != dict:
            try:
                payload = payload.dict(exclude_none=True)
            except Exception as e:
                logger.exception(f"Payload could not be cast as dict: {e}")
                raise Exception from e
        r = httpx.post(
            url,
            json=payload,
            headers=header,
            params=params,
            files=files,
            content=content,
            timeout=30.0,
        )

        try:
            r.raise_for_status()
        except HTTPStatusError as exc:
            try:
                loaded_errors = r.json()
                error_code = loaded_errors.get("errorCode")
                error_detail = loaded_errors.get("errorDescription")
                msg = f"Call failed: {r.request.method=}, {url=}, {params=}, {r.status_code=}, {error_code=}, {error_detail=}"
            except:
                error_code = None
                msg = None

            if msg:
                specific_exception = exception_map.get(error_code, PhraseTMSException)
                raise specific_exception(msg)

            else:
                logger.exception(f"Call failed: {r} // {url} - {params}")
                raise Exception from exc

        try:
            return r.json()
        except JSONDecodeError:
            return

    def put(
        self,
        path: str,
        phrase_token: Optional[str] = None,
        params: Optional[dict] = None,
        payload: Optional[Any] = None,
        files: Optional[Any] = None,
        headers: Optional[dict] = None,
        content: Optional[bytes] = None,
    ) -> dict | None:
        token = phrase_token or self.token
        if token is None:
            raise NotAuthenticatedError

        url = f"{MEMSOURCE_BASE_URL}{path}"
        header = {"Authorization": token}
        if headers is not None:
            header.update(headers)
        if payload is not None and type(payload) != dict:
            try:
                payload = payload.dict()
            except Exception as e:
                logger.exception(f"Payload could not be cast as dict: {e}")
                raise Exception from e

        r = httpx.put(
            url,
            json=payload,
            headers=header,
            params=params,
            files=files,
            content=content,
            timeout=30.0,
        )

        try:
            r.raise_for_status()
        except HTTPStatusError as exc:
            try:
                loaded_errors = r.json()
                error_code = loaded_errors.get("errorCode")
                error_detail = loaded_errors.get("errorDescription")
                msg = f"Call failed: {url=}, {params=}, {r.status_code=}, {error_code=}, {error_detail=}"
                raise PhraseTMSException(msg)
            except:
                logger.exception(f"Call failed: {r} // {url} - {params}")
                raise Exception from exc

        try:
            return r.json()
        except JSONDecodeError:
            return

    def patch(
        self,
        path: str,
        phrase_token: Optional[str] = None,
        params: Optional[dict] = None,
        payload: Optional[Any] = None,
        files: Optional[Any] = None,
        headers: Optional[dict] = None,
        content: Optional[bytes] = None,
    ) -> dict | None:
        token = phrase_token or self.token
        if token is None:
            raise NotAuthenticatedError

        url = f"{MEMSOURCE_BASE_URL}{path}"
        header = {"Authorization": token}
        if headers is not None:
            header.update(headers)
        if payload is not None and type(payload) != dict:
            try:
                payload = payload.dict()
            except Exception as e:
                logger.exception(f"Payload could not be cast as dict: {e}")
                raise Exception from e

        r = httpx.patch(
            url,
            json=payload,
            headers=header,
            params=params,
            files=files,
            content=content,
            timeout=30.0,
        )

        try:
            r.raise_for_status()
        except HTTPStatusError as exc:
            try:
                loaded_errors = r.json()
                error_code = loaded_errors.get("errorCode")
                error_detail = loaded_errors.get("errorDescription")
                msg = f"Call failed: {url=}, {params=}, {r.status_code=}, {error_code=}, {error_detail=}"
                raise PhraseTMSException(msg)
            except:
                logger.exception(f"Call failed: {r} // {url} - {params}")
                raise Exception from exc

        try:
            return r.json()
        except JSONDecodeError:
            return

    def delete(
        self,
        path: str,
        phrase_token: Optional[str] = None,
        params: Optional[dict] = None,
        payload: Optional[Any] = None,
        files: Optional[Any] = None,
        headers: Optional[dict] = None,
        content: Optional[bytes] = None,
    ) -> dict | None:
        token = phrase_token or self.token
        if token is None:
            raise NotAuthenticatedError

        url = f"{MEMSOURCE_BASE_URL}{path}"
        header = {"Authorization": token}
        if headers is not None:
            header.update(headers)

        r = httpx.delete(url, headers=header, params=params, timeout=30.0)

        try:
            r.raise_for_status()
        except HTTPStatusError as exc:
            try:
                loaded_errors = r.json()
                error_code = loaded_errors.get("errorCode")
                error_detail = loaded_errors.get("errorDescription")
                msg = f"Call failed: {url=}, {params=}, {r.status_code=}, {error_code=}, {error_detail=}"
                raise PhraseTMSException(msg)
            except:
                logger.exception(f"Call failed: {r} // {url} - {params}")
                raise Exception from exc

        try:
            return r.json()
        except JSONDecodeError:
            return
