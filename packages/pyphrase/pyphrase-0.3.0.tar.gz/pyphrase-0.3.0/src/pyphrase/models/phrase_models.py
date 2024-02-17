from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

try:
    from pydantic.v1 import BaseModel, Field, confloat, conint, constr
except ImportError:
    from pydantic import BaseModel, Field, confloat, conint, constr


class Model(BaseModel):
    __root__: Any


class Role(str, Enum):
    SYS_ADMIN = "SYS_ADMIN"
    SYS_ADMIN_READ = "SYS_ADMIN_READ"
    ADMIN = "ADMIN"
    PROJECT_MANAGER = "PROJECT_MANAGER"
    LINGUIST = "LINGUIST"
    GUEST = "GUEST"
    SUBMITTER = "SUBMITTER"


class UserReference(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    userName: Optional[str] = None
    email: Optional[str] = None
    role: Optional[Role] = None
    id: Optional[str] = None
    uid: Optional[str] = None


class AdditionalWorkflowStepDto(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None


class AdditionalWorkflowStepRequestDto(BaseModel):
    name: constr(min_length=0, max_length=255) = Field(
        ..., description="Name of the additional workflow step"
    )


class PageDtoAdditionalWorkflowStepDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[AdditionalWorkflowStepDto]] = None


class AnalyseJobReference(BaseModel):
    uid: Optional[str] = None
    filename: Optional[str] = None
    innerId: Optional[str] = None


class CountsDto(BaseModel):
    segments: Optional[float] = None
    words: Optional[float] = None
    characters: Optional[float] = None
    normalizedPages: Optional[float] = None
    percent: Optional[float] = None
    editingTime: Optional[float] = None


class MatchCounts101Dto(BaseModel):
    match100: Optional[CountsDto] = None
    match95: Optional[CountsDto] = None
    match85: Optional[CountsDto] = None
    match75: Optional[CountsDto] = None
    match50: Optional[CountsDto] = None
    match0: Optional[CountsDto] = None
    match101: Optional[CountsDto] = None


class MatchCountsDto(BaseModel):
    match100: Optional[CountsDto] = None
    match95: Optional[CountsDto] = None
    match85: Optional[CountsDto] = None
    match75: Optional[CountsDto] = None
    match50: Optional[CountsDto] = None
    match0: Optional[CountsDto] = None


class MatchCountsNTDtoV1(BaseModel):
    match100: Optional[CountsDto] = None
    match99: Optional[CountsDto] = None


class NetRateSchemeReference(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    name: Optional[str] = None
    dateCreated: Optional[datetime] = None
    createdBy: Optional[UserReference] = None


class IdReference(BaseModel):
    id: str


class Action(str, Enum):
    PRE_ANALYSE = "PRE_ANALYSE"
    POST_ANALYSE = "POST_ANALYSE"
    COMPARE_ANALYSE = "COMPARE_ANALYSE"
    PARENT_ANALYSE = "PARENT_ANALYSE"
    PRE_TRANSLATE = "PRE_TRANSLATE"
    ASYNC_TRANSLATE = "ASYNC_TRANSLATE"
    IMPORT_JOB = "IMPORT_JOB"
    IMPORT_FILE = "IMPORT_FILE"
    ALIGN = "ALIGN"
    EXPORT_TMX_BY_QUERY = "EXPORT_TMX_BY_QUERY"
    EXPORT_TMX = "EXPORT_TMX"
    IMPORT_TMX = "IMPORT_TMX"
    IMPORT_TBX = "IMPORT_TBX"
    INSERT_INTO_TM = "INSERT_INTO_TM"
    DELETE_TM = "DELETE_TM"
    CLEAR_TM = "CLEAR_TM"
    QA = "QA"
    QA_V3 = "QA_V3"
    UPDATE_CONTINUOUS_JOB = "UPDATE_CONTINUOUS_JOB"
    UPDATE_SOURCE = "UPDATE_SOURCE"
    UPDATE_TARGET = "UPDATE_TARGET"
    EXTRACT_CLEANED_TMS = "EXTRACT_CLEANED_TMS"
    GLOSSARY_PUT = "GLOSSARY_PUT"
    GLOSSARY_DELETE = "GLOSSARY_DELETE"
    CREATE_PROJECT = "CREATE_PROJECT"
    EXPORT_COMPLETE_FILE = "EXPORT_COMPLETE_FILE"
    IMPORT_ANNOTATIONS = "IMPORT_ANNOTATIONS"
    FILE_FLOW_CONVERTER_IMPORT = "FILE_FLOW_CONVERTER_IMPORT"
    FILE_FLOW_MT_PRETRANSLATE = "FILE_FLOW_MT_PRETRANSLATE"
    FILE_FLOW_QUALITY_ESTIMATION = "FILE_FLOW_QUALITY_ESTIMATION"


class ErrorDetailDto(BaseModel):
    code: Optional[str] = Field(None, description="Code, e.g. NOT_FOUND.")
    args: Optional[Dict[str, Dict[str, Any]]] = Field(
        None, description='Related arguments, e.g. number => "hello world"'
    )
    message: Optional[str] = Field(None, description="Optional human-readable message.")


class ObjectReference(BaseModel):
    pass


class ProjectReference(BaseModel):
    name: Optional[str] = None
    uid: Optional[str] = None


class UidReference(BaseModel):
    uid: str


class AnalysisType(str, Enum):
    PreAnalyse = "PreAnalyse"
    PostAnalyse = "PostAnalyse"
    PreAnalyseTarget = "PreAnalyseTarget"
    Compare = "Compare"
    PreAnalyseProvider = "PreAnalyseProvider"


class CreateAnalyseListAsyncDto(BaseModel):
    jobs: List[UidReference] = Field(..., max_items=100, min_items=1)
    type: Optional[AnalysisType] = Field(None, description="default: PreAnalyse")
    includeFuzzyRepetitions: Optional[bool] = Field(None, description="Default: true")
    separateFuzzyRepetitions: Optional[bool] = Field(None, description="Default: false")
    includeConfirmedSegments: Optional[bool] = Field(None, description="Default: true")
    includeNumbers: Optional[bool] = Field(None, description="Default: true")
    includeLockedSegments: Optional[bool] = Field(None, description="Default: true")
    countSourceUnits: Optional[bool] = Field(None, description="Default: true")
    includeTransMemory: Optional[bool] = Field(
        None, description="Default: true. Works only for type=PreAnalyse."
    )
    includeNonTranslatables: Optional[bool] = Field(
        None, description="Default: false. Works only for type=PreAnalyse."
    )
    includeMachineTranslationMatches: Optional[bool] = Field(
        None, description="Default: false. Works only for type=PreAnalyse."
    )
    transMemoryPostEditing: Optional[bool] = Field(
        None, description="Default: false. Works only for type=PostAnalyse."
    )
    nonTranslatablePostEditing: Optional[bool] = Field(
        None, description="Default: false. Works only for type=PostAnalyse."
    )
    machineTranslatePostEditing: Optional[bool] = Field(
        None, description="Default: false. Works only for type=PostAnalyse."
    )
    name: Optional[constr(min_length=0, max_length=255)] = None
    netRateScheme: Optional[IdReference] = None
    compareWorkflowLevel: Optional[conint(ge=1, le=15)] = Field(
        None, description="Required for type=Compare"
    )
    useProjectAnalysisSettings: Optional[bool] = Field(
        None,
        description="Default: false. Use default project settings. Will be overwritten with setting sent\n        in the API call.",
    )
    callbackUrl: Optional[str] = None


class AnalyseRecalculateRequestDto(BaseModel):
    analyses: List[IdReference] = Field(..., max_items=100, min_items=1)
    callbackUrl: Optional[str] = None


class CleanupTask(ObjectReference):
    pass


class InputStream(ObjectReference):
    pass


class InputStreamLength(BaseModel):
    stream: Optional[InputStream] = None
    length: Optional[int] = None
    name: Optional[str] = None
    characterEncoding: Optional[str] = None
    extension: Optional[str] = None
    cleanupTask: Optional[CleanupTask] = None


class BulkDeleteAnalyseDto(BaseModel):
    analyses: List[IdReference] = Field(..., max_items=100, min_items=1)
    purge: Optional[bool] = Field(None, description="Default: false")


class ConcurrentRequestsDto(BaseModel):
    limit: Optional[int] = Field(
        None,
        description="Max number of allowed concurrent request, null value means no limit",
    )
    count: Optional[int] = Field(
        None, description="Current count of running concurrent requests"
    )


class LoginResponseDto(BaseModel):
    user: Optional[UserReference] = None
    token: Optional[str] = None
    expires: Optional[datetime] = None
    lastInvalidateAllSessionsPerformed: Optional[datetime] = None


class LoginDto(BaseModel):
    userName: str
    password: str
    code: Optional[str] = Field(
        None, description="Required only for 2-factor authentication"
    )


class LoginToSessionResponseDto(BaseModel):
    user: Optional[UserReference] = None
    cookie: Optional[str] = None
    csrfToken: Optional[str] = None


class LoginToSessionDto(BaseModel):
    userName: str
    password: str
    rememberMe: Optional[bool] = None


class LoginOtherDto(BaseModel):
    userName: str


class EditionDto(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    title: Optional[str] = None


class FeaturesDto(BaseModel):
    icuEnabled: Optional[bool] = None
    rejectJobs: Optional[bool] = None
    qaHighlightsEnabled: Optional[bool] = None
    lqaBulkCommentsCreation: Optional[bool] = None
    mtForTMAbove100Enabled: Optional[bool] = None
    mqmQualityEstimationEnabled: Optional[bool] = None
    tweDarkModeEnabled: Optional[bool] = None


class OrganizationReference(BaseModel):
    uid: Optional[str] = None
    name: Optional[str] = None


class LoginWithGoogleDto(BaseModel):
    idToken: str


class LoginWithAppleDto(BaseModel):
    codeOrRefreshToken: str


class AppleTokenResponseDto(BaseModel):
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[str] = None
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None


class Status(str, Enum):
    NEW = "NEW"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    REJECTED = "REJECTED"
    DELIVERED = "DELIVERED"
    EMAILED = "EMAILED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class ProviderReference(BaseModel):
    type: str
    id: Optional[str] = None
    uid: Optional[str] = None


class USER(ProviderReference):
    userName: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    active: Optional[bool] = None


class VENDOR(ProviderReference):
    name: Optional[str] = None
    defaultProjectOwnerId: Optional[int] = None


class WorkflowStepReference(BaseModel):
    name: Optional[str] = None
    id: Optional[str] = None
    uid: Optional[str] = None
    order: Optional[int] = None
    lqaEnabled: Optional[bool] = None


class State(str, Enum):
    Miss = "Miss"
    Diff = "Diff"


class ComparedSegmentDto(BaseModel):
    uid: Optional[str] = None
    state: Optional[State] = None


class ComparedSegmentsDto(BaseModel):
    segments: Optional[List[ComparedSegmentDto]] = None


class BusinessUnitDto(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    name: Optional[str] = None
    createdBy: Optional[UserReference] = None


class PageDtoBusinessUnitDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[BusinessUnitDto]] = None


class BusinessUnitEditDto(BaseModel):
    name: constr(min_length=0, max_length=255)


class ClientReference(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    name: Optional[str] = None


class PriceListReference(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    uid: Optional[str] = None


class ClientEditDto(BaseModel):
    name: constr(min_length=0, max_length=255)
    externalId: Optional[constr(min_length=0, max_length=255)] = None
    note: Optional[constr(min_length=0, max_length=4096)] = None
    displayNoteInProject: Optional[bool] = Field(None, description="Default: false")
    priceList: Optional[IdReference] = None
    netRateScheme: Optional[IdReference] = None


class IntegrationType(str, Enum):
    AEM_PLUGIN = "AEM_PLUGIN"
    AMAZON_S3 = "AMAZON_S3"
    AZURE = "AZURE"
    BITBUCKET = "BITBUCKET"
    BITBUCKETSERVER = "BITBUCKETSERVER"
    BOX = "BOX"
    BRAZE = "BRAZE"
    CONFLUENCE = "CONFLUENCE"
    CONTENTFUL = "CONTENTFUL"
    CONTENTFULENTRYLEVEL = "CONTENTFULENTRYLEVEL"
    CONTENTSTACK = "CONTENTSTACK"
    DROPBOX = "DROPBOX"
    DRUPAL = "DRUPAL"
    DRUPAL_PLUGIN = "DRUPAL_PLUGIN"
    FTP = "FTP"
    GIT = "GIT"
    GITHUB = "GITHUB"
    GITLAB = "GITLAB"
    GOOGLE = "GOOGLE"
    HELPSCOUT = "HELPSCOUT"
    HUBSPOT = "HUBSPOT"
    JOOMLA = "JOOMLA"
    KENTICO = "KENTICO"
    KENTICO_KONTENT = "KENTICO_KONTENT"
    MAGENTO = "MAGENTO"
    MARKETO = "MARKETO"
    ONEDRIVE = "ONEDRIVE"
    PARDOT = "PARDOT"
    PHRASE = "PHRASE"
    SALESFORCE = "SALESFORCE"
    SFTP = "SFTP"
    SHAREPOINT = "SHAREPOINT"
    SITECORE = "SITECORE"
    TRIDION = "TRIDION"
    TYPO3 = "TYPO3"
    VERBIS = "VERBIS"
    WORDPRESS = "WORDPRESS"
    ZENDESK = "ZENDESK"


class NameDto(AdditionalWorkflowStepDto):
    pass


class ConnectorErrorDetailDto(BaseModel):
    code: Optional[str] = None
    message: Optional[str] = None
    messageCode: Optional[str] = None
    args: Optional[Dict[str, Dict[str, Any]]] = None
    skipPrefix: Optional[bool] = None


class ConnectorErrorsDto(BaseModel):
    errors: Optional[List[ConnectorErrorDetailDto]] = None


class UploadResultDto(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    folder: Optional[str] = None
    encodedName: Optional[str] = None
    size: Optional[int] = None
    error: Optional[str] = None
    asyncTaskId: Optional[str] = None
    errors: Optional[ConnectorErrorsDto] = None


class ErrorDto(BaseModel):
    code: Optional[str] = None
    message: Optional[str] = None


class FileDto(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    encodedName: Optional[str] = None
    contentType: Optional[str] = None
    note: Optional[str] = None
    size: Optional[int] = None
    directory: Optional[bool] = None
    lastModified: Optional[datetime] = None
    dueDate: Optional[datetime] = None
    selected: Optional[bool] = None
    error: Optional[ErrorDto] = None


class FileListDto(BaseModel):
    files: Optional[List[FileDto]] = None
    currentFolder: Optional[str] = None
    encodedCurrentFolder: Optional[str] = None
    rootFolder: Optional[bool] = None
    lastChangedFiles: Optional[List[FileDto]] = None


class UserType(str, Enum):
    PROJECT_OWNER = "PROJECT_OWNER"
    JOB_OWNER = "JOB_OWNER"
    PROVIDER = "PROVIDER"
    GUEST = "GUEST"


class OrganizationType(str, Enum):
    VENDOR = "VENDOR"
    BUYER = "BUYER"


class Repeated(str, Enum):
    REPEATED = "REPEATED"
    NOT_REPEATED = "NOT_REPEATED"


class LQAReference(BaseModel):
    errorCategoryId: conint(ge=1)
    severityId: conint(ge=1)
    user: Optional[IdReference] = None
    repeated: Optional[Repeated] = Field(None, description="Default: `NOT_REPEATED`")


class MentionType(str, Enum):
    USER = "USER"
    GROUP = "GROUP"


class MentionGroupType(str, Enum):
    JOB = "JOB"
    OWNERS = "OWNERS"
    PROVIDERS = "PROVIDERS"
    GUESTS = "GUESTS"
    WORKFLOW_STEP = "WORKFLOW_STEP"


class MentionableGroupDto(BaseModel):
    groupType: Optional[MentionGroupType] = None
    groupName: Optional[str] = None
    groupReference: Optional[UidReference] = None


class Role2(str, Enum):
    PARENT = "PARENT"


class ReferenceCorrelation(BaseModel):
    uid: Optional[str] = None
    role: Optional[Role2] = None


class Name(str, Enum):
    resolved = "resolved"
    unresolved = "unresolved"


class WorkflowStepReferenceV2(BaseModel):
    name: Optional[str] = None
    uid: Optional[str] = None
    id: Optional[str] = None
    order: Optional[int] = None
    lqaEnabled: Optional[bool] = None


class FindConversationsDto(BaseModel):
    jobs: List[UidReference] = Field(..., max_items=100, min_items=1)
    since: Optional[str] = None
    includeDeleted: Optional[bool] = Field(None, description="Default: false")


class CostCenterDto(BusinessUnitDto):
    pass


class PageDtoCostCenterDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[CostCenterDto]] = None


class CostCenterEditDto(BaseModel):
    name: Optional[constr(min_length=0, max_length=255)] = None


class FieldType(str, Enum):
    MULTI_SELECT = "MULTI_SELECT"
    SINGLE_SELECT = "SINGLE_SELECT"
    STRING = "STRING"
    NUMBER = "NUMBER"
    URL = "URL"
    DATE = "DATE"


class AllowedEntity(str, Enum):
    PROJECT = "PROJECT"


class CustomFieldOptionDto(BaseModel):
    uid: Optional[str] = None
    value: Optional[str] = None


class CustomFieldOptionsTruncatedDto(BaseModel):
    truncatedOptions: Optional[List[CustomFieldOptionDto]] = Field(
        None,
        description="Truncated list of options with size 5.\n    To get all options use endpoint for getting options of the specific field",
    )
    remainingCount: Optional[int] = None


class CreateCustomFieldDto(BaseModel):
    name: constr(min_length=0, max_length=255)
    allowedEntities: List[AllowedEntity]
    options: Optional[List[str]] = None
    type: Optional[FieldType] = None
    required: Optional[bool] = None
    description: Optional[constr(min_length=0, max_length=500)] = None


class PageDtoCustomFieldOptionDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[CustomFieldOptionDto]] = None


class AndroidSettingsDto(BaseModel):
    tagRegexp: Optional[str] = None
    icuSubFilter: Optional[bool] = Field(None, description="Default: `false`")


class AsciidocSettingsDto(BaseModel):
    tagRegexp: Optional[str] = None
    htmlInPassthrough: Optional[bool] = Field(None, description="Default: `false`")
    nontranslatableMonospaceCustomStylesRegexp: Optional[str] = None
    extractCustomDocumentAttributeNameRegexp: Optional[str] = Field(
        None, description="Default: `.*`"
    )
    extractBtnMenuLabels: Optional[bool] = Field(None, description="Default: `false`")


class DelimiterType(str, Enum):
    TAB = "TAB"
    COMMA = "COMMA"
    SEMICOLON = "SEMICOLON"
    OTHER = "OTHER"


class CsvSettingsDto(BaseModel):
    delimiter: Optional[str] = Field(None, description="Default: ,")
    delimiterType: Optional[DelimiterType] = Field(None, description="Default: COMMA")
    htmlSubFilter: Optional[bool] = Field(None, description="Default: false")
    tagRegexp: Optional[str] = None
    importColumns: Optional[str] = None
    contextNoteColumns: Optional[str] = None
    contextKeyColumn: Optional[str] = None
    maxLenColumn: Optional[str] = None
    importRows: Optional[str] = None


class DitaSettingsDto(BaseModel):
    includeTags: Optional[str] = None
    excludeTags: Optional[str] = None
    inlineTags: Optional[str] = None
    inlineTagsNonTranslatable: Optional[str] = None
    tagRegexp: Optional[str] = None


class DocBookSettingsDto(DitaSettingsDto):
    pass


class DocSettingsDto(BaseModel):
    comments: Optional[bool] = Field(None, description="Default: false")
    index: Optional[bool] = Field(None, description="Default: true")
    other: Optional[bool] = Field(None, description="Default: false")
    tagRegexp: Optional[str] = None
    hyperlinkTarget: Optional[bool] = Field(None, description="Default: false")
    joinSimilarRuns: Optional[bool] = Field(None, description="Default: false")
    targetFont: Optional[str] = None
    properties: Optional[bool] = Field(None, description="Default: false")
    hidden: Optional[bool] = Field(None, description="Default: false")
    headerFooter: Optional[bool] = Field(None, description="Default: true")


class HtmlSettingsDto(BaseModel):
    breakTagCreatesSegment: Optional[bool] = Field(None, description="Default: true")
    unknownTagCreatesTag: Optional[bool] = Field(None, description="Default: true")
    preserveWhitespace: Optional[bool] = Field(None, description="Default: false")
    importComments: Optional[bool] = Field(None, description="Default: true")
    excludeElements: Optional[str] = Field(
        None, description='Example: "script,blockquote"'
    )
    tagRegexp: Optional[str] = None
    charEntitiesToTags: Optional[str] = None
    translateMetaTagRegexp: Optional[str] = None
    importDefaultMetaTags: Optional[bool] = Field(None, description="Default: true")
    translatableAttributes: Optional[str] = None
    importDefaultAttributes: Optional[bool] = Field(None, description="Default: true")
    nonTranslatableInlineElements: Optional[str] = Field(
        None, description='Example: "code"'
    )
    translatableInlineElements: Optional[str] = Field(
        None, description='Example: "span"'
    )
    updateLang: Optional[bool] = Field(None, description="Default: false")
    escapeDisabled: Optional[bool] = Field(None, description="Default: `false`")


class IdmlSettingsDto(BaseModel):
    extractNotes: Optional[bool] = Field(None, description="Default: false")
    simplifyCodes: Optional[bool] = Field(None, description="Default: true")
    extractMasterSpreads: Optional[bool] = Field(None, description="Default: true")
    extractLockedLayers: Optional[bool] = Field(None, description="Default: true")
    extractInvisibleLayers: Optional[bool] = Field(None, description="Default: false")
    extractHiddenConditionalText: Optional[bool] = Field(
        None, description="Default: false"
    )
    extractHyperlinks: Optional[bool] = Field(None, description="Default: false")
    keepKerning: Optional[bool] = Field(None, description="Default: false")
    keepTracking: Optional[bool] = Field(None, description="Default: false")
    targetFont: Optional[str] = None
    replaceFont: Optional[bool] = Field(None, description="Default: true")
    removeXmlElements: Optional[bool] = Field(None, description="Default: false")
    tagRegexp: Optional[str] = None
    extractCrossReferenceFormats: Optional[bool] = Field(
        None, description="Default: true"
    )
    extractVariables: Optional[bool] = Field(None, description="Default: true")


class JsonSettingsDto(BaseModel):
    tagRegexp: Optional[str] = None
    htmlSubFilter: Optional[bool] = Field(None, description="Default: true")
    icuSubFilter: Optional[bool] = Field(None, description="Default: false")
    excludeKeyRegexp: Optional[str] = None
    includeKeyRegexp: Optional[str] = None
    contextNotePath: Optional[str] = None
    maxLenPath: Optional[str] = None
    contextKeyPath: Optional[str] = None


class MacSettingsDto(BaseModel):
    htmlSubfilter: Optional[bool] = Field(None, description="Default: false")
    tagRegexp: Optional[str] = None
    icuSubFilter: Optional[bool] = Field(None, description="Default: `false`")


class Flavor(str, Enum):
    PLAIN = "PLAIN"
    PHP = "PHP"
    GITHUB = "GITHUB"


class MdSettingsDto(BaseModel):
    hardLineBreaksSegments: Optional[bool] = Field(None, description="Default: true")
    preserveWhiteSpaces: Optional[bool] = Field(None, description="Default: false")
    tagRegexp: Optional[str] = None
    customElements: Optional[str] = None
    ignoredBlockPrefixes: Optional[str] = None
    flavor: Optional[Flavor] = Field(None, description="Default: PLAIN")
    processJekyllFrontMatter: Optional[bool] = Field(None, description="Default: false")
    extractCodeBlocks: Optional[bool] = Field(None, description="Default: true")
    notEscapedCharacters: Optional[str] = None
    excludeCodeElements: Optional[bool] = Field(None, description="Default: false")


class MetadataType(str, Enum):
    CLIENT = "CLIENT"
    DOMAIN = "DOMAIN"
    SUBDOMAIN = "SUBDOMAIN"
    FILENAME = "FILENAME"


class MetadataField(BaseModel):
    type: Optional[MetadataType] = None


class MetadataPrioritySettingsDto(BaseModel):
    prioritizedFields: Optional[List[MetadataField]] = None


class MifSettingsDto(BaseModel):
    extractBodyPages: Optional[bool] = Field(None, description="Default: true")
    extractReferencePages: Optional[bool] = Field(None, description="Default: false")
    extractMasterPages: Optional[bool] = Field(None, description="Default: true")
    extractHiddenPages: Optional[bool] = Field(None, description="Default: false")
    extractVariables: Optional[bool] = Field(None, description="Default: false")
    extractIndexMarkers: Optional[bool] = Field(None, description="Default: true")
    extractLinks: Optional[bool] = Field(None, description="Default: false")
    extractXRefDef: Optional[bool] = Field(None, description="Default: false")
    extractPgfNumFormat: Optional[bool] = Field(None, description="Default: true")
    extractCustomReferencePages: Optional[bool] = Field(
        None, description="Default: true"
    )
    extractDefaultReferencePages: Optional[bool] = Field(
        None, description="Default: false"
    )
    extractUsedVariables: Optional[bool] = Field(None, description="Default: true")
    extractHiddenCondText: Optional[bool] = Field(None, description="Default: false")
    extractUsedXRefDef: Optional[bool] = Field(None, description="Default: true")
    extractUsedPgfNumFormat: Optional[bool] = Field(None, description="Default: true")
    tagRegexp: Optional[str] = None


class NonEmptySegmentAction(str, Enum):
    NONE = "NONE"
    CONFIRM = "CONFIRM"
    LOCK = "LOCK"
    CONFIRM_LOCK = "CONFIRM_LOCK"


class MultilingualCsvSettingsDto(BaseModel):
    sourceColumns: Optional[str] = None
    targetColumns: Optional[str] = None
    contextNoteColumns: Optional[str] = None
    contextKeyColumns: Optional[str] = None
    tagRegexp: Optional[str] = None
    htmlSubFilter: Optional[bool] = Field(None, description="Default: false")
    segmentation: Optional[bool] = Field(None, description="Default: true")
    delimiter: Optional[constr(min_length=0, max_length=255)] = Field(
        None, description="Default: ,"
    )
    delimiterType: Optional[DelimiterType] = Field(None, description="Default: COMMA")
    importRows: Optional[str] = None
    maxLenColumns: Optional[str] = None
    allTargetColumns: Optional[Dict[str, str]] = Field(
        None, description='Format: "language":"column"; example: {"en": "A", "sk": "B"}'
    )
    nonEmptySegmentAction: Optional[NonEmptySegmentAction] = None
    saveConfirmedSegmentsToTm: Optional[bool] = None


class MultilingualXlsSettingsDto(BaseModel):
    sourceColumn: Optional[str] = None
    targetColumns: Optional[Dict[str, str]] = Field(
        None, description='Format: "language":"column"; example: {"en": "A", "sk": "B"}'
    )
    contextNoteColumn: Optional[str] = None
    contextKeyColumn: Optional[str] = None
    tagRegexp: Optional[str] = None
    htmlSubFilter: Optional[bool] = Field(None, description="Default: false")
    segmentation: Optional[bool] = Field(None, description="Default: true")
    importRows: Optional[str] = None
    maxLenColumn: Optional[str] = None
    nonEmptySegmentAction: Optional[NonEmptySegmentAction] = None
    saveConfirmedSegmentsToTm: Optional[bool] = None


class MultilingualXmlSettingsDto(BaseModel):
    translatableElementsXPath: Optional[str] = None
    sourceElementsXPath: Optional[str] = None
    targetElementsXPaths: Optional[Dict[str, str]] = Field(
        None,
        description='\'Format: "language":"xpath";\n            example = \'{"en": "tuv[@lang=\'en\']/seg", "sk": "tuv[@lang=\'sk\']/seg"}',
    )
    inlineElementsNonTranslatableXPath: Optional[str] = None
    tagRegexp: Optional[str] = None
    segmentation: Optional[bool] = Field(None, description="Default: `true`")
    htmlSubFilter: Optional[bool] = Field(None, description="Default: `false`")
    contextKeyXPath: Optional[str] = None
    contextNoteXPath: Optional[str] = None
    maxLenXPath: Optional[str] = None
    preserveWhitespace: Optional[bool] = Field(None, description="Default: `false`")
    preserveCharEntities: Optional[str] = None
    xslUrl: Optional[str] = None
    xslFile: Optional[str] = Field(
        None, description="UID of uploaded XSL file, overrides xslUrl"
    )
    nonEmptySegmentAction: Optional[NonEmptySegmentAction] = None
    saveConfirmedSegmentsToTm: Optional[bool] = None
    icuSubFilter: Optional[bool] = Field(None, description="Default: `false`")


class Filter(str, Enum):
    TRANS_PDF = "TRANS_PDF"
    DEFAULT = "DEFAULT"


class PdfSettingsDto(BaseModel):
    filter: Optional[Filter] = Field(None, description="Default: TRANS_PDF")


class PhpSettingsDto(BaseModel):
    tagRegexp: Optional[str] = None
    htmlSubFilter: Optional[bool] = Field(None, description="Default: false")


class ContextKeySuffixType(str, Enum):
    MSGCTXT = "MSGCTXT"
    MSGID = "MSGID"
    MSGCTXT_AND_MSGID = "MSGCTXT_AND_MSGID"
    MSGCTXT_OR_MSGID = "MSGCTXT_OR_MSGID"


class ImportSetSegmentConfirmedWhen(str, Enum):
    FUZZY = "FUZZY"
    NONFUZZY = "NONFUZZY"


class PoSettingsDto(BaseModel):
    tagRegexp: Optional[str] = None
    exportMultiline: Optional[bool] = Field(None, description="Default: true")
    htmlSubFilter: Optional[bool] = Field(None, description="Default: false")
    segment: Optional[bool] = Field(None, description="Default: false")
    markupSubFilterTranslatable: Optional[str] = None
    markupSubFilterNonTranslatable: Optional[str] = None
    contextKeySuffixType: Optional[ContextKeySuffixType] = None
    saveConfirmedSegments: Optional[bool] = None
    importSetSegmentConfirmedWhen: Optional[ImportSetSegmentConfirmedWhen] = None
    importSetSegmentLockedWhen: Optional[ImportSetSegmentConfirmedWhen] = None
    exportConfirmedLocked: Optional[ImportSetSegmentConfirmedWhen] = None
    exportConfirmedNotLocked: Optional[ImportSetSegmentConfirmedWhen] = None
    exportNotConfirmedLocked: Optional[ImportSetSegmentConfirmedWhen] = None
    exportNotConfirmedNotLocked: Optional[ImportSetSegmentConfirmedWhen] = None
    icuSubFilter: Optional[bool] = Field(None, description="Default: `false`")


class PptSettingsDto(BaseModel):
    hiddenSlides: Optional[bool] = Field(None, description="Default: false")
    other: Optional[bool] = Field(None, description="Default: false")
    notes: Optional[bool] = Field(None, description="Default: false")
    masterSlides: Optional[bool] = Field(None, description="Default: false")


class PropertiesSettingsDto(BaseModel):
    tagRegexp: Optional[str] = None


class PsdSettingsDto(BaseModel):
    extractHiddenLayers: Optional[bool] = Field(None, description="Default: true")
    extractLockedLayers: Optional[bool] = Field(None, description="Default: true")
    tagRegexp: Optional[str] = None


class QuarkTagSettingsDto(BaseModel):
    removeKerningTrackingTags: Optional[bool] = Field(
        None, description="Default: false"
    )
    tagRegexp: Optional[str] = None


class ResxSettingsDto(BaseModel):
    tagRegexp: Optional[str] = None
    htmlSubFilter: Optional[bool] = None


class SdlXlfSettingsDto(BaseModel):
    icuSubFilter: Optional[bool] = Field(None, description="Default: false")
    skipImportRules: Optional[str] = Field(None, description="Default: translate=no")
    importAsConfirmedRules: Optional[str] = None
    importAsLockedRules: Optional[str] = Field(None, description="Default: locked=true")
    exportAttrsWhenConfirmedAndLocked: Optional[str] = Field(
        None, description="Default: locked=true"
    )
    exportAttrsWhenConfirmedAndNotLocked: Optional[str] = None
    exportAttrsWhenNotConfirmedAndLocked: Optional[str] = Field(
        None, description="Default: locked=true"
    )
    exportAttrsWhenNotConfirmedAndNotLocked: Optional[str] = None
    saveConfirmedSegments: Optional[bool] = Field(None, description="Default: true")
    tagRegexp: Optional[str] = None


class SegRuleReference(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    language: Optional[str] = None
    name: Optional[str] = None
    filename: Optional[str] = None
    primary: Optional[bool] = None


class ContextType(str, Enum):
    AUTO = "AUTO"
    PREV_AND_NEXT_SEGMENT = "PREV_AND_NEXT_SEGMENT"
    SEGMENT_KEY = "SEGMENT_KEY"
    NO_CONTEXT = "NO_CONTEXT"


class TMMatchSettingsDto(BaseModel):
    contextType: Optional[ContextType] = Field(
        None, description="Default: PREV_AND_NEXT_SEGMENT"
    )
    prevOrNextSegment: Optional[bool] = Field(None, description="Default: false")
    penalizeMultiContextMatch: Optional[bool] = Field(
        None, description="Default: false"
    )
    ignoreTagMetadata: Optional[bool] = Field(None, description="Default: true")
    metadataPriority: Optional[MetadataPrioritySettingsDto] = None


class TtxSettingsDto(BaseModel):
    saveConfirmedSegments: Optional[bool] = Field(None, description="Default: true")


class TxtSettingsDto(BaseModel):
    tagRegexp: Optional[str] = None
    translatableTextRegexp: Optional[str] = None
    contextKey: Optional[str] = None
    regexpCapturingGroups: Optional[bool] = Field(None, description="Default: false")


class Xlf2SettingsDto(BaseModel):
    icuSubFilter: Optional[bool] = Field(None, description="Default: false")
    importNotes: Optional[bool] = Field(None, description="Default: true")
    saveConfirmedSegments: Optional[bool] = Field(None, description="Default: true")
    segmentation: Optional[bool] = Field(None, description="Default: true")
    lineBreakTags: Optional[bool] = Field(None, description="Default: false")
    preserveWhitespace: Optional[bool] = Field(None, description="Default: true")
    copySourceToTargetIfNotImported: Optional[bool] = Field(
        None, description="Default: true"
    )
    respectTranslateAttr: Optional[bool] = Field(None, description="Default: true")
    skipImportRules: Optional[str] = None
    importAsConfirmedRules: Optional[str] = Field(
        None, description="Default: state=final"
    )
    importAsLockedRules: Optional[str] = None
    exportAttrsWhenConfirmedAndLocked: Optional[str] = Field(
        None, description="Default: state=final"
    )
    exportAttrsWhenConfirmedAndNotLocked: Optional[str] = Field(
        None, description="Default: state=final"
    )
    exportAttrsWhenNotConfirmedAndLocked: Optional[str] = None
    exportAttrsWhenNotConfirmedAndNotLocked: Optional[str] = None
    contextKeyXPath: Optional[str] = None
    preserveCharEntities: Optional[str] = None
    xslUrl: Optional[str] = None
    xslFile: Optional[str] = Field(
        None, description="UID of uploaded XSL file, overrides xslUrl"
    )
    tagRegexp: Optional[str] = None


class XlfSettingsDto(BaseModel):
    icuSubFilter: Optional[bool] = Field(None, description="Default: false")
    importNotes: Optional[bool] = Field(None, description="Default: true")
    segmentation: Optional[bool] = Field(None, description="Default: true")
    skipImportRules: Optional[str] = Field(
        None,
        description="Default: translate=no; examples: translate=no;approved=no;state=needs-adaptation",
    )
    importAsConfirmedRules: Optional[str] = Field(
        None, description="Multiple rules must be separated by semicolon"
    )
    importAsLockedRules: Optional[str] = None
    exportAttrsWhenConfirmedAndLocked: Optional[str] = None
    exportAttrsWhenConfirmedAndNotLocked: Optional[str] = None
    exportAttrsWhenNotConfirmedAndLocked: Optional[str] = None
    exportAttrsWhenNotConfirmedAndNotLocked: Optional[str] = None
    saveConfirmedSegments: Optional[bool] = Field(None, description="Default: true")
    lineBreakTags: Optional[bool] = Field(None, description="Default: false")
    preserveWhitespace: Optional[bool] = Field(None, description="Default: true")
    contextType: Optional[str] = None
    preserveCharEntities: Optional[str] = None
    copySourceToTargetIfNotImported: Optional[bool] = Field(
        None, description="Default: true"
    )
    importXPath: Optional[str] = None
    importAsConfirmedXPath: Optional[str] = None
    importAsLockedXPath: Optional[str] = None
    xslUrl: Optional[str] = None
    xslFile: Optional[str] = Field(
        None, description="UID of uploaded XSL file, overrides xslUrl"
    )
    tagRegexp: Optional[str] = None


class CellFlow(str, Enum):
    DownRight = "DownRight"
    RightDown = "RightDown"
    DownLeft = "DownLeft"
    LeftDown = "LeftDown"


class XlsSettingsDto(BaseModel):
    sheetNames: Optional[bool] = Field(None, description="Default: false")
    hidden: Optional[bool] = Field(None, description="Default: false")
    comments: Optional[bool] = Field(None, description="Default: false")
    other: Optional[bool] = Field(None, description="Default: false")
    cellFlow: Optional[CellFlow] = Field(None, description="Default: DownRight")
    htmlSubfilter: Optional[bool] = Field(None, description="Default: false")
    tagRegexp: Optional[str] = None
    specifiedColumns: Optional[str] = None


class RulesFormat(str, Enum):
    PLAIN = "PLAIN"
    XPATH = "XPATH"


class XmlSettingsDto(BaseModel):
    rulesFormat: Optional[RulesFormat] = Field(None, description='Default: `"PLAIN"`')
    includeElementsPlain: Optional[str] = Field(
        None, description='Default: `"*"`, example: `"para,heading"`'
    )
    excludeElementsPlain: Optional[str] = Field(
        None, description='Example: `"script,par"`'
    )
    includeAttributesPlain: Optional[str] = Field(
        None, description='Example: `"title"`'
    )
    excludeAttributesPlain: Optional[str] = Field(
        None, description='Example: `"lang,href"`'
    )
    inlineElementsNonTranslatablePlain: Optional[str] = Field(
        None, description='Example: `"tt,b"`'
    )
    inlineElementsPlain: Optional[str] = None
    inlineElementsAutoPlain: Optional[bool] = Field(
        None, description="Default: `false`"
    )
    htmlSubfilterElementsPlain: Optional[str] = Field(
        None, description='Example: `"tt,b"`'
    )
    entities: Optional[bool] = Field(None, description="Default: `false`")
    lockElementsPlain: Optional[str] = None
    lockAttributesPlain: Optional[str] = None
    includeXPath: Optional[str] = None
    inlineElementsXpath: Optional[str] = None
    inlineElementsNonTranslatableXPath: Optional[str] = None
    inlineElementsAutoXPath: Optional[bool] = Field(
        None, description="Default: `false`"
    )
    htmlSubfilterElementsXpath: Optional[str] = None
    lockXPath: Optional[str] = None
    segmentation: Optional[bool] = Field(None, description="Default: `true`")
    tagRegexp: Optional[str] = None
    contextNoteXpath: Optional[str] = None
    maxLenXPath: Optional[str] = None
    preserveWhitespaceXPath: Optional[str] = None
    preserveCharEntities: Optional[str] = None
    contextKeyXPath: Optional[str] = None
    xslUrl: Optional[str] = None
    xslFile: Optional[str] = Field(
        None, description="UID of uploaded XSL file, overrides `xslUrl`"
    )
    importComments: Optional[bool] = Field(None, description="Default: `true`")
    icuSubFilter: Optional[bool] = Field(None, description="Default: `false`")
    assistantProfile: Optional[str] = None


class LocaleFormat(str, Enum):
    MEMSOURCE = "MEMSOURCE"
    RFC_5646 = "RFC_5646"
    ANDROID_QUALIFIER = "ANDROID_QUALIFIER"
    ANDROID_QUALIFIER_BCP = "ANDROID_QUALIFIER_BCP"


class YamlSettingsDto(BaseModel):
    htmlSubFilter: Optional[bool] = Field(None, description="Default: false")
    tagRegexp: Optional[str] = None
    includeKeyRegexp: Optional[str] = None
    excludeValueRegexp: Optional[str] = None
    contextPath: Optional[str] = None
    contextKeyPath: Optional[str] = None
    markdownSubfilter: Optional[bool] = Field(None, description="Default: false")
    updateRootElementLang: Optional[bool] = Field(None, description="Default: false")
    localeFormat: Optional[LocaleFormat] = None
    indentEmptyLinesInString: Optional[bool] = Field(None, description="Default: true")
    icuSubFilter: Optional[bool] = Field(None, description="Default: `false`")


class CustomFiletypeType(str, Enum):
    html = "html"
    json = "json"
    xml = "xml"
    multiling_xml = "multiling_xml"
    txt = "txt"


class FileFormat(str, Enum):
    doc = "doc"
    ppt = "ppt"
    xls = "xls"
    xlf = "xlf"
    xlf2 = "xlf2"
    sdlxlif = "sdlxlif"
    ttx = "ttx"
    html = "html"
    xml = "xml"
    mif = "mif"
    tmx = "tmx"
    idml = "idml"
    dita = "dita"
    json = "json"
    po = "po"
    ts = "ts"
    icml = "icml"
    yaml = "yaml"
    properties = "properties"
    csv = "csv"
    android_string = "android_string"
    desktop_entry = "desktop_entry"
    mac_strings = "mac_strings"
    pdf = "pdf"
    windows_rc = "windows_rc"
    xml_properties = "xml_properties"
    joomla_ini = "joomla_ini"
    magento_csv = "magento_csv"
    dtd = "dtd"
    mozilla_properties = "mozilla_properties"
    plist = "plist"
    plain_text = "plain_text"
    srt = "srt"
    sub = "sub"
    sbv = "sbv"
    wiki = "wiki"
    resx = "resx"
    resjson = "resjson"
    chrome_json = "chrome_json"
    epub = "epub"
    svg = "svg"
    docbook = "docbook"
    wpxliff = "wpxliff"
    multiling_xml = "multiling_xml"
    multiling_xls = "multiling_xls"
    mqxliff = "mqxliff"
    php = "php"
    psd = "psd"
    tag = "tag"
    md = "md"
    vtt = "vtt"


class FileImportSettingsCreateDto(BaseModel):
    inputCharset: Optional[str] = None
    outputCharset: Optional[str] = None
    zipCharset: Optional[str] = None
    fileFormat: Optional[FileFormat] = Field(None, description="default: auto-detect")
    autodetectMultilingualFiles: Optional[bool] = Field(
        None,
        description="Try to use multilingual variants for auto-detected CSV and Excel files. Default: true",
    )
    targetLength: Optional[bool] = Field(None, description="Default: false")
    targetLengthMax: Optional[int] = Field(None, description="default: 1000")
    targetLengthPercent: Optional[bool] = Field(None, description="Default: false")
    targetLengthPercentValue: Optional[float] = Field(None, description="default: 130")
    segmentationRuleId: Optional[int] = None
    targetSegmentationRuleId: Optional[int] = None
    android: Optional[AndroidSettingsDto] = None
    csv: Optional[CsvSettingsDto] = None
    dita: Optional[DitaSettingsDto] = None
    docBook: Optional[DocBookSettingsDto] = None
    doc: Optional[DocSettingsDto] = None
    html: Optional[HtmlSettingsDto] = None
    idml: Optional[IdmlSettingsDto] = None
    json_: Optional[JsonSettingsDto] = Field(None, alias="json")
    mac: Optional[MacSettingsDto] = None
    md: Optional[MdSettingsDto] = None
    mif: Optional[MifSettingsDto] = None
    multilingualXls: Optional[MultilingualXlsSettingsDto] = None
    multilingualCsv: Optional[MultilingualCsvSettingsDto] = None
    multilingualXml: Optional[MultilingualXmlSettingsDto] = None
    pdf: Optional[PdfSettingsDto] = None
    php: Optional[PhpSettingsDto] = None
    po: Optional[PoSettingsDto] = None
    ppt: Optional[PptSettingsDto] = None
    properties: Optional[PropertiesSettingsDto] = None
    psd: Optional[PsdSettingsDto] = None
    quarkTag: Optional[QuarkTagSettingsDto] = None
    resx: Optional[ResxSettingsDto] = None
    sdlXlf: Optional[SdlXlfSettingsDto] = None
    tmMatch: Optional[TMMatchSettingsDto] = None
    ttx: Optional[TtxSettingsDto] = None
    txt: Optional[TxtSettingsDto] = None
    xlf2: Optional[Xlf2SettingsDto] = None
    xlf: Optional[XlfSettingsDto] = None
    xls: Optional[XlsSettingsDto] = None
    xml: Optional[XmlSettingsDto] = None
    yaml: Optional[YamlSettingsDto] = None
    asciidoc: Optional[AsciidocSettingsDto] = None


class UpdateCustomFileTypeDto(BaseModel):
    name: Optional[str] = None
    filenamePattern: Optional[str] = None
    type: Optional[CustomFiletypeType] = None
    fileImportSettings: Optional[FileImportSettingsCreateDto] = None


class DeleteCustomFileTypeDto(BaseModel):
    customFileTypes: List[UidReference]


class DiscountSettingsDto(BaseModel):
    repetition: Optional[float] = None
    tm101: Optional[float] = None
    tm100: Optional[float] = None
    tm95: Optional[float] = None
    tm85: Optional[float] = None
    tm75: Optional[float] = None
    tm50: Optional[float] = None
    tm0: Optional[float] = None
    mt100: Optional[float] = None
    mt95: Optional[float] = None
    mt85: Optional[float] = None
    mt75: Optional[float] = None
    mt50: Optional[float] = None
    mt0: Optional[float] = None
    nt100: Optional[float] = None
    nt99: Optional[float] = None
    nt85: Optional[float] = None
    nt75: Optional[float] = None
    nt50: Optional[float] = None
    nt0: Optional[float] = None
    if100: Optional[float] = None
    if95: Optional[float] = None
    if85: Optional[float] = None
    if75: Optional[float] = None
    if50: Optional[float] = None
    if0: Optional[float] = None


class NetRateSchemeWorkflowStepReference(BaseModel):
    id: Optional[str] = None
    workflowStep: Optional[WorkflowStepReference] = None


class PageDtoNetRateSchemeReference(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[NetRateSchemeReference]] = None


class NetRateSchemeWorkflowStepCreate(BaseModel):
    workflowStep: IdReference
    rates: Optional[DiscountSettingsDto] = None


class NetRateSchemeEdit(BaseModel):
    name: constr(min_length=1, max_length=255)
    rates: Optional[DiscountSettingsDto] = None


class NetRateSchemeWorkflowStep(BaseModel):
    id: Optional[str] = None
    workflowStep: Optional[WorkflowStepReference] = None
    rates: Optional[DiscountSettingsDto] = None


class NetRateSchemeWorkflowStepEdit(BaseModel):
    rates: Optional[DiscountSettingsDto] = None


class PageDtoNetRateSchemeWorkflowStepReference(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[NetRateSchemeWorkflowStepReference]] = None


class DomainDto(BusinessUnitDto):
    pass


class PageDtoDomainDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[DomainDto]] = None


class DomainEditDto(CostCenterEditDto):
    pass


class EmailTemplateType(str, Enum):
    JobAssigned = "JobAssigned"
    JobStatusChanged = "JobStatusChanged"
    NextWorkflowStep = "NextWorkflowStep"
    JobRejected = "JobRejected"
    LoginInfo = "LoginInfo"
    ProjectTransferredToBuyer = "ProjectTransferredToBuyer"
    SharedProjectAssigned = "SharedProjectAssigned"
    SharedProjectStatusChanged = "SharedProjectStatusChanged"
    AutomatedProjectCreated = "AutomatedProjectCreated"
    AutomatedProjectSourceUpdated = "AutomatedProjectSourceUpdated"
    AutomatedProjectStatusChanged = "AutomatedProjectStatusChanged"
    JobWidgetProjectQuotePrepared = "JobWidgetProjectQuotePrepared"
    JobWidgetProjectQuotePreparationFailure = "JobWidgetProjectQuotePreparationFailure"
    JobWidgetProjectCreated = "JobWidgetProjectCreated"
    JobWidgetProjectCompleted = "JobWidgetProjectCompleted"
    CmsQuoteReady = "CmsQuoteReady"
    CmsWorkCompleted = "CmsWorkCompleted"
    CmsJobRejected = "CmsJobRejected"
    QUOTE_UPDATED = "QUOTE_UPDATED"
    QUOTE_STATUS_CHANGED = "QUOTE_STATUS_CHANGED"
    LQA_SHARE_REPORT = "LQA_SHARE_REPORT"


class OrganizationEmailTemplateDto(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    type: Optional[EmailTemplateType] = None
    name: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    ccAddress: Optional[str] = None
    bccAddress: Optional[str] = None


class PageDtoOrganizationEmailTemplateDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[OrganizationEmailTemplateDto]] = None


class FileHandoverDto(BaseModel):
    fileId: Optional[str] = Field(None, description="ID of the uploaded file")
    filename: Optional[str] = Field(None, description="Filename of the uploaded file")


class JobPartReferences(BaseModel):
    jobs: List[UidReference] = Field(..., max_items=100, min_items=1)


class UploadedFileDto(BaseModel):
    uid: Optional[str] = None
    name: Optional[str] = None
    size: Optional[int] = None
    type: Optional[str] = None


class RemoteUploadedFileDto(BaseModel):
    uid: Optional[str] = None
    name: Optional[str] = None
    size: Optional[int] = None
    type: Optional[str] = None
    url: Optional[str] = None


class PageDtoUploadedFileDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[UploadedFileDto]] = None


class MachineTranslateSettingsLangsDto(BaseModel):
    id: Optional[str] = Field(None, description="Id")
    sourceLang: Optional[str] = Field(
        None, description="Source language for CUSTOMIZABLE engine"
    )
    targetLangs: Optional[List[str]] = Field(
        None, description="List of target languages for the CUSTOMIZABLE engine"
    )


class MemTransMachineTranslateSettingsDto(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    baseName: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    default_: Optional[bool] = None
    includeTags: Optional[bool] = None
    mtQualityEstimation: Optional[bool] = None
    enabled: Optional[bool] = None
    glossarySupported: Optional[bool] = None
    args: Optional[Dict[str, str]] = None
    langs: Optional[MachineTranslateSettingsLangsDto] = None
    charCount: Optional[int] = Field(
        None, description="Unknown value is represented by value: -1"
    )


class MemsourceTranslateProfileSimpleDto(BaseModel):
    uid: Optional[str] = None
    name: Optional[str] = None
    dateCreated: Optional[datetime] = None
    createdBy: Optional[UserReference] = None
    memsourceTranslate: Optional[MemTransMachineTranslateSettingsDto] = None
    locked: Optional[bool] = None


class GlossaryEditDto(BaseModel):
    name: constr(min_length=0, max_length=255)
    langs: List[str] = Field(..., max_items=2147483647, min_items=1)
    owner: Optional[IdReference] = Field(
        None, description="Owner of the TM must be Admin or PM"
    )


class GlossaryActivationDto(BaseModel):
    active: Optional[bool] = None


class SearchTMClientDto(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class SearchTMDomainDto(SearchTMClientDto):
    pass


class SearchTMProjectDto(BaseModel):
    id: Optional[int] = None
    uid: Optional[str] = None
    name: Optional[str] = None


class SearchTMSubDomainDto(SearchTMClientDto):
    pass


class SearchTMTransMemoryDto(BaseModel):
    uid: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    reverse: Optional[bool] = None


class TagMetadata(BaseModel):
    id: Optional[str] = None
    type: Optional[str] = None
    content: Optional[str] = None
    transAttributes: Optional[str] = None


class TagMetadataDto(TagMetadata):
    pass


class AddCommentDto(BaseModel):
    text: str


class LanguageDto(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    rfc: Optional[str] = None
    android: Optional[str] = None
    androidBcp: Optional[str] = None


class LanguageListDto(BaseModel):
    languages: List[LanguageDto]


class PassFailThresholdDto(BaseModel):
    minScorePercentage: float = Field(
        ...,
        description="Minimum allowed LQA score in percentage in line with MQM scoring (1 - penalties/word-count)",
        example=99.0,
    )


class SeverityDto(BaseModel):
    code: Optional[int] = Field(None, description="Code of the severity category")
    value: Optional[float] = Field(None, description="Allowed values 0.0-100,000.0")


class ToggleableWeightDto(BaseModel):
    enabled: Optional[bool] = Field(
        None, description="If this error category is enabled, default false"
    )
    weight: Optional[float] = Field(
        None, description="Weight of this error category (0.1 - 99.9)", example=1.0
    )
    code: Optional[int] = Field(None, description="Code of the error category")


class VerityWeightsDto(BaseModel):
    verity: Optional[ToggleableWeightDto] = None
    cultureSpecificReference: Optional[ToggleableWeightDto] = None


class LqaProfileReferenceDto(BaseModel):
    uid: str = Field(..., description="UID of the profile", example="string")
    name: str = Field(..., description="Name of the profile")
    isDefault: bool = Field(
        ..., description="If profile is set as default for organization"
    )
    createdBy: UserReference = Field(..., description="User who created the profile")
    dateCreated: datetime = Field(..., description="When profile was created")
    organization: UidReference


class PageDtoLqaProfileReferenceDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[LqaProfileReferenceDto]] = None


class MachineTranslateStatusDto(BaseModel):
    uid: Optional[str] = None
    ok: Optional[bool] = None
    error: Optional[str] = None


class MachineTranslateSettingsDto(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    baseName: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    default_: Optional[bool] = None
    includeTags: Optional[bool] = None
    mtQualityEstimation: Optional[bool] = None
    enabled: Optional[bool] = None
    args: Optional[Dict[str, str]] = None
    langs: Optional[MachineTranslateSettingsLangsDto] = None


class MachineTranslateSettingsPbmDto(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    baseName: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    default_: Optional[bool] = None
    includeTags: Optional[bool] = None
    mtQualityEstimation: Optional[bool] = None
    args: Optional[Dict[str, str | None]] = None
    payForMtPossible: Optional[bool] = None
    payForMtActive: Optional[bool] = None
    charCount: Optional[int] = None
    sharingSettings: Optional[int] = None
    langs: Optional[MachineTranslateSettingsLangsDto] = None


class PageDtoMachineTranslateSettingsPbmDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[MachineTranslateSettingsPbmDto]] = None


class TypesDto(BaseModel):
    types: Optional[List[str]] = None


class MachineTranslateResponse(BaseModel):
    translations: Optional[List[str]] = None


class TranslationRequestExtendedDto(BaseModel):
    sourceTexts: List[str] = Field(..., max_items=2147483647, min_items=1)
    from_: str = Field(..., alias="from")
    to: str
    filename: Optional[str] = None


class TaskMappingDto(BaseModel):
    taskId: Optional[str] = None
    workflowLevel: Optional[str] = None
    resourcePath: Optional[str] = None
    project: Optional[ObjectReference] = None
    job: Optional[ObjectReference] = None


class ProjectTermBaseReference(BaseModel):
    id: Optional[str] = None
    termBase: Optional[ObjectReference] = None
    name: Optional[str] = None
    writeMode: Optional[bool] = None
    targetLang: Optional[str] = None
    readMode: Optional[bool] = None
    workflowStep: Optional[ObjectReference] = None


class ProjectTranslationMemoryReference(BaseModel):
    id: Optional[str] = None
    transMem: Optional[ObjectReference] = None
    name: Optional[str] = None
    workflowStep: Optional[ObjectReference] = None
    targetLang: Optional[str] = None
    penalty: Optional[float] = None
    readMode: Optional[bool] = None


class ConsumedMtusDto(BaseModel):
    consumedMtus: Optional[int] = None


class ImportSettingsEditDto(BaseModel):
    uid: str
    name: str
    fileImportSettings: FileImportSettingsCreateDto


class ImportSettingsReference(BaseModel):
    uid: Optional[str] = None
    name: Optional[str] = None
    createdBy: Optional[UserReference] = None
    dateCreated: Optional[datetime] = None


class PageDtoImportSettingsReference(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[ImportSettingsReference]] = None


class ImportSettingsCreateDto(BaseModel):
    name: str
    fileImportSettings: FileImportSettingsCreateDto


class BusinessUnitReference(BaseModel):
    name: Optional[str] = None
    id: Optional[str] = None
    uid: Optional[str] = None


class DiscountSchemeReference(NetRateSchemeReference):
    pass


class DomainReference(BusinessUnitReference):
    pass


class SubDomainReference(BusinessUnitReference):
    pass


class FileNamingSettingsDto(BaseModel):
    renameCompleted: Optional[bool] = None
    completedFilePattern: Optional[constr(min_length=0, max_length=255)] = None
    targetFolderPath: Optional[constr(min_length=0, max_length=255)] = None


class VendorSecuritySettingsDto(BaseModel):
    canChangeSharedJobDueDateEnabled: Optional[bool] = Field(
        None, description="Default: `false`"
    )
    canChangeSharedJobDueDate: Optional[List[UidReference]] = None
    jobVendorsMayUploadReferences: Optional[bool] = Field(
        None, description="Default: `false`"
    )


class MachineTranslationSettingsDto(BaseModel):
    useMachineTranslation: Optional[bool] = Field(
        None, description="Pre-translate from machine translation. Default: false"
    )
    lock100PercentMatches: Optional[bool] = Field(
        None,
        description="Lock section: 100% machine translation matches. Default: false",
    )
    confirmMatches: Optional[bool] = Field(
        None,
        description="Set segment status to confirmed for:\n                machine translation matches above `confirmMatchesThreshold`. Default: false",
    )
    confirmMatchesThreshold: Optional[confloat(ge=0.0, le=1.0)] = Field(
        None, description="Machine translation matches percent. Default: `1.0`"
    )
    useAltTransOnly: Optional[bool] = Field(
        None,
        description="Do not put machine translations to target and use alt-trans fields (alt-trans in mxlf).\nDefault: false",
    )
    mtQeMatchesInEditors: Optional[bool] = Field(
        None,
        description="Display quality-estimated machine translation matches in Memsource Editor. Default: false",
    )
    mtForTMAbove100: Optional[bool] = Field(
        None,
        description="Use machine translation for segments with a TM match of 100% or more. Default: false",
    )


class NonTranslatableSettingsDto(BaseModel):
    preTranslateNonTranslatables: Optional[bool] = Field(
        None, description="Pre-translate non-translatables. Default: false"
    )
    confirm100PercentMatches: Optional[bool] = Field(
        None,
        description="Set segment status to confirmed for: 100% non-translatable matches. Default: false",
    )
    lock100PercentMatches: Optional[bool] = Field(
        None, description="Lock section: 100% non-translatable matches. Default: false"
    )
    nonTranslatablesInEditors: Optional[bool] = Field(
        None, description="If non-translatables are enabled in Editors."
    )


class RepetitionsSettingsDto(BaseModel):
    autoPropagateRepetitions: Optional[bool] = Field(
        None, description="Propagate repetitions. Default: false"
    )
    confirmRepetitions: Optional[bool] = Field(
        None,
        description="Set segment status to confirmed for: Repetitions. Default: false",
    )
    autoPropagateToLockedRepetitions: Optional[bool] = Field(
        None,
        description="Changes in 1st repetition propagate upon confirmation into subsequent locked repetitions. Default: false",
    )
    lockSubsequentRepetitions: Optional[bool] = Field(
        None,
        description="If auto-propagated subsequent repetitions should be locked. Default: false",
    )


class TranslationMemorySettingsDto(BaseModel):
    useTranslationMemory: Optional[bool] = Field(
        None, description="Pre-translate from translation memory. Default: false"
    )
    translationMemoryThreshold: Optional[confloat(ge=0.0, le=1.01)] = Field(
        None, description="Pre-translation threshold percent"
    )
    confirm100PercentMatches: Optional[bool] = Field(
        None,
        description="Set segment status to confirmed for: 100% translation memory matches. Default: false",
    )
    confirm101PercentMatches: Optional[bool] = Field(
        None,
        description="Set segment status to confirmed for: 101% translation memory matches. Default: false",
    )
    lock100PercentMatches: Optional[bool] = Field(
        None,
        description="Lock section: 100% translation memory matches. Default: false",
    )
    lock101PercentMatches: Optional[bool] = Field(
        None,
        description="Lock section: 101% translation memory matches. Default: false",
    )


class Number(ObjectReference):
    pass


class QaCheckType(str, Enum):
    VOID = "VOID"
    NUMBER = "NUMBER"
    STRING = "STRING"
    REGEX = "REGEX"
    MORAVIA = "MORAVIA"


class Name1(str, Enum):
    emptyTarget = "emptyTarget"
    inconsistentTranslation = "inconsistentTranslation"
    joinMarksInconsistency = "joinMarksInconsistency"
    missingNumber = "missingNumber"
    segmentNotConfirmed = "segmentNotConfirmed"
    nonConformingTerms = "nonConformingTerms"
    multipleSpaces = "multipleSpaces"
    endPunctuation = "endPunctuation"
    targetLength = "targetLength"
    absoluteTargetLength = "absoluteTargetLength"
    relativeTargetLength = "relativeTargetLength"
    inconsistentFormatting = "inconsistentFormatting"
    unresolvedComment = "unresolvedComment"
    emptyPairTags = "emptyPairTags"
    strictJobStatus = "strictJobStatus"
    forbiddenStringsEnabled = "forbiddenStringsEnabled"
    excludeLockedSegments = "excludeLockedSegments"
    ignoreNotApprovedTerms = "ignoreNotApprovedTerms"
    spellCheck = "spellCheck"
    repeatedWords = "repeatedWords"
    inconsistentTagContent = "inconsistentTagContent"
    emptyTagContent = "emptyTagContent"
    malformed = "malformed"
    forbiddenTerms = "forbiddenTerms"
    targetLengthPercent = "targetLengthPercent"
    targetLengthPerSegment = "targetLengthPerSegment"
    newerAtLowerLevel = "newerAtLowerLevel"
    leadingAndTrailingSpaces = "leadingAndTrailingSpaces"
    targetSourceIdentical = "targetSourceIdentical"
    ignoreInAllWorkflowSteps = "ignoreInAllWorkflowSteps"
    regexp = "regexp"
    unmodifiedFuzzyTranslation = "unmodifiedFuzzyTranslation"
    unmodifiedFuzzyTranslationTM = "unmodifiedFuzzyTranslationTM"
    unmodifiedFuzzyTranslationMTNT = "unmodifiedFuzzyTranslationMTNT"
    moravia = "moravia"
    extraNumbers = "extraNumbers"
    nestedTags = "nestedTags"


class QACheckDtoV2(BaseModel):
    type: QaCheckType
    name: Name1


class QASettingsDtoV2(BaseModel):
    checks: Optional[List[QACheckDtoV2]] = None


class RegexpCheckRuleDtoV2(BaseModel):
    description: Optional[str] = None
    sourceRegexp: Optional[str] = None
    targetRegexp: Optional[str] = None
    id: Optional[str] = None
    ignorable: Optional[bool] = None
    instant: Optional[bool] = None


class STRING(QACheckDtoV2):
    ignorable: Optional[bool] = None
    enabled: Optional[bool] = None
    value: Optional[str] = None
    instant: Optional[bool] = None


class VOID(QACheckDtoV2):
    ignorable: Optional[bool] = None
    enabled: Optional[bool] = None
    instant: Optional[bool] = None


class EditQASettingsDtoV2(BaseModel):
    checks: Optional[List[Dict[str, Dict[str, Any]]]] = Field(
        None,
        description="checks",
        example='\n        {\n            "ignorable": false,\n            "enabled": true,\n            "type": "VOID",\n            "instant": false,\n            "name": "emptyTarget"\n        },\n        {\n            "ignorable": false,\n            "enabled": true,\n            "value": 12,\n            "type": "NUMBER",\n            "name": "targetLength"\n        },\n        {\n            "ignorable": false,\n            "enabled": true,\n            "value": "ASAP, irony",\n            "type": "STRING",\n            "instant": true,\n            "name": "forbiddenStrings"\n        },\n        {\n            "enabled": true,\n            "profile": "jiris",\n            "ignorable": true,\n            "type": "MORAVIA",\n            "name": "moravia"\n        },\n        {\n            "rules": [\n                {\n                    "description": "Description",\n                    "sourceRegexp": ".+",\n                    "targetRegexp": ".+",\n                    "ignorable": true\n                },\n                {\n                    "description": "Description",\n                    "sourceRegexp": "i+",\n                    "targetRegexp": "e+",\n                    "ignorable": false\n                }\n            ],\n            "type": "REGEX",\n            "name": "regexp"\n        },\n        {\n            "enabled": true,\n            "ignorable": true,\n            "type": "VOID",\n            "name": "customQa"\n        }\n    ',
    )


class EditPlainConversationDto(BaseModel):
    status: Optional[Name] = None
    correlation: Optional[ReferenceCorrelation] = None


class Status2(str, Enum):
    NEW = "NEW"
    ASSIGNED = "ASSIGNED"
    COMPLETED = "COMPLETED"
    ACCEPTED_BY_VENDOR = "ACCEPTED_BY_VENDOR"
    DECLINED_BY_VENDOR = "DECLINED_BY_VENDOR"
    COMPLETED_BY_VENDOR = "COMPLETED_BY_VENDOR"
    CANCELLED = "CANCELLED"


class BuyerReference(ClientReference):
    pass


class CostCenterReference(BusinessUnitReference):
    pass


class MachineTranslateSettingsReference(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None


class ProgressDto(BaseModel):
    totalCount: Optional[int] = None
    finishedCount: Optional[int] = None
    overdueCount: Optional[int] = None


class ProjectWorkflowSettingsReference(BaseModel):
    propagateTranslationsToLowerWfDuringUpdateSource: Optional[bool] = None


class ProjectWorkflowStepDto(BaseModel):
    id: Optional[int] = None
    abbreviation: Optional[str] = None
    name: Optional[str] = None
    workflowLevel: Optional[int] = None
    workflowStep: Optional[ObjectReference] = None
    lqaProfileUid: Optional[str] = None


class ReferenceFileReference(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    filename: Optional[str] = None
    note: Optional[str] = None
    dateCreated: Optional[datetime] = None
    createdBy: Optional[UserReference] = None


class VendorReference(ClientReference):
    pass


class Providers(BaseModel):
    all: Optional[List[ProviderReference]] = None
    relevant: Optional[List[ProviderReference]] = None


class ProjectMTSettingsPerLangDto(BaseModel):
    targetLang: str
    machineTranslateSettings: Optional[UidReference] = None


class AddTargetLangDto(BaseModel):
    targetLangs: Optional[List[str]] = Field(None, max_items=2147483647, min_items=1)


class ProjectTemplateWorkflowSettingsAssignedToDto(BaseModel):
    targetLang: Optional[str] = None
    providers: Optional[List[ProviderReference]] = None


class ProjectTemplateWorkflowSettingsDto(BaseModel):
    workflowStep: Optional[WorkflowStepReference] = None
    assignedTo: Optional[List[ProjectTemplateWorkflowSettingsAssignedToDto]] = None


class AddWorkflowStepsDto(BaseModel):
    workflowSteps: Optional[List[IdReference]] = Field(
        None, max_items=2147483647, min_items=1
    )


class AssignVendorDto(BaseModel):
    vendor: Optional[IdReference] = None
    dateDue: Optional[datetime] = None


class CloneProjectDto(BaseModel):
    name: str


class PageDtoProviderReference(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[ProviderReference]] = None


class SetProjectStatusDto(BaseModel):
    status: Status2


class FinancialSettingsDto(BaseModel):
    netRateScheme: Optional[NetRateSchemeReference] = None
    priceList: Optional[PriceListReference] = None


class SetFinancialSettingsDto(BaseModel):
    netRateScheme: Optional[IdReference] = None
    priceList: Optional[IdReference] = None


class EnabledCheck(str, Enum):
    EmptyTranslation = "EmptyTranslation"
    TrailingPunctuation = "TrailingPunctuation"
    Formatting = "Formatting"
    JoinTags = "JoinTags"
    MissingNumbersV3 = "MissingNumbersV3"
    MultipleSpacesV3 = "MultipleSpacesV3"
    NonConformingTerm = "NonConformingTerm"
    NotConfirmed = "NotConfirmed"
    TranslationLength = "TranslationLength"
    AbsoluteLength = "AbsoluteLength"
    RelativeLength = "RelativeLength"
    UnresolvedComment = "UnresolvedComment"
    EmptyPairTags = "EmptyPairTags"
    InconsistentTranslationTargetSource = "InconsistentTranslationTargetSource"
    InconsistentTranslationSourceTarget = "InconsistentTranslationSourceTarget"
    ForbiddenString = "ForbiddenString"
    SpellCheck = "SpellCheck"
    RepeatedWord = "RepeatedWord"
    InconsistentTagContent = "InconsistentTagContent"
    EmptyTagContent = "EmptyTagContent"
    Malformed = "Malformed"
    ForbiddenTerm = "ForbiddenTerm"
    NewerAtLowerLevel = "NewerAtLowerLevel"
    LeadingAndTrailingSpaces = "LeadingAndTrailingSpaces"
    LeadingSpaces = "LeadingSpaces"
    TrailingSpaces = "TrailingSpaces"
    TargetSourceIdentical = "TargetSourceIdentical"
    SourceOrTargetRegexp = "SourceOrTargetRegexp"
    UnmodifiedFuzzyTranslation = "UnmodifiedFuzzyTranslation"
    UnmodifiedFuzzyTranslationTM = "UnmodifiedFuzzyTranslationTM"
    UnmodifiedFuzzyTranslationMTNT = "UnmodifiedFuzzyTranslationMTNT"
    Moravia = "Moravia"
    ExtraNumbersV3 = "ExtraNumbersV3"
    UnresolvedConversation = "UnresolvedConversation"
    NestedTags = "NestedTags"
    FuzzyInconsistencyTargetSource = "FuzzyInconsistencyTargetSource"
    FuzzyInconsistencySourceTarget = "FuzzyInconsistencySourceTarget"
    CustomQA = "CustomQA"
    MissingNonTranslatableAnnotation = "MissingNonTranslatableAnnotation"


class EnabledQualityChecksDto(BaseModel):
    enabledChecks: Optional[List[EnabledCheck]] = None


class LqaErrorCategoryDto(BaseModel):
    errorCategoryId: Optional[int] = None
    name: Optional[str] = None
    enabled: Optional[bool] = None
    errorCategories: Optional[List[LqaErrorCategoryDto]] = None


class LqaSeverityDto(BaseModel):
    severityId: Optional[int] = None
    name: Optional[str] = None
    weight: Optional[int] = None


class MTSettingsPerLanguageDto(BaseModel):
    targetLang: str = Field(
        ..., description="mtSettings is set for whole project if targetLang == null"
    )
    machineTranslateSettings: Optional[MachineTranslateSettingsDto] = None


class MTSettingsPerLanguageListDto(BaseModel):
    mtSettingsPerLangList: Optional[List[MTSettingsPerLanguageDto]] = Field(
        None, unique_items=True
    )


class Status7(str, Enum):
    APPROVED = "APPROVED"
    DECLINED = "DECLINED"
    DRAFT = "DRAFT"
    FOR_APPROVAL = "FOR_APPROVAL"
    NEW = "NEW"


class BillingUnit(str, Enum):
    Character = "Character"
    Word = "Word"
    Page = "Page"
    Hour = "Hour"


class QuoteType(str, Enum):
    BUYER = "BUYER"
    PROVIDER = "PROVIDER"


class QuoteDto(BaseModel):
    id: Optional[int] = None
    uid: Optional[str] = None
    name: Optional[str] = None
    status: Optional[Status7] = None
    currency: Optional[str] = None
    billingUnit: Optional[BillingUnit] = None
    createdBy: Optional[UserReference] = None
    dateCreated: Optional[datetime] = None
    totalPrice: Optional[float] = None
    netRateScheme: Optional[NetRateSchemeReference] = None
    priceList: Optional[PriceListReference] = None
    workflowStepList: Optional[List[WorkflowStepReference]] = None
    provider: Optional[ProviderReference] = None
    customerEmail: Optional[str] = None
    quoteType: Optional[QuoteType] = None
    editable: Optional[bool] = None
    outdated: Optional[bool] = None


class EditProjectMTSettPerLangDto(BaseModel):
    targetLang: str
    machineTranslateSettings: Optional[IdReference] = None


class EditProjectMTSettPerLangListDto(BaseModel):
    mtSettingsPerLangList: Optional[List[EditProjectMTSettPerLangDto]] = None


class EditProjectMTSettingsDto(BaseModel):
    machineTranslateSettings: Optional[IdReference] = None


class AnalyseSettingsDto(BaseModel):
    type: Optional[AnalysisType] = None
    includeFuzzyRepetitions: Optional[bool] = Field(None, description="Default: false")
    separateFuzzyRepetitions: Optional[bool] = Field(None, description="Default: false")
    includeNonTranslatables: Optional[bool] = Field(None, description="Default: false")
    includeMachineTranslationMatches: Optional[bool] = Field(
        None, description="Default: false"
    )
    includeConfirmedSegments: Optional[bool] = Field(None, description="Default: false")
    includeNumbers: Optional[bool] = Field(None, description="Default: false")
    includeLockedSegments: Optional[bool] = Field(None, description="Default: false")
    countSourceUnits: Optional[bool] = Field(None, description="Default: false")
    includeTransMemory: Optional[bool] = Field(None, description="Default: false")
    namingPattern: Optional[str] = None
    analyzeByLanguage: Optional[bool] = Field(None, description="Default: false")
    analyzeByProvider: Optional[bool] = Field(None, description="Default: false")
    allowAutomaticPostAnalysis: Optional[bool] = Field(
        None,
        description="If automatic post analysis should be created after update source. Default: false",
    )
    transMemoryPostEditing: Optional[bool] = Field(None, description="Default: false")
    nonTranslatablePostEditing: Optional[bool] = Field(
        None, description="Default: false"
    )
    machineTranslatePostEditing: Optional[bool] = Field(
        None, description="Default: false"
    )


class CreateCustomFieldInstanceDto(BaseModel):
    customField: UidReference
    selectedOptions: Optional[List[UidReference]] = None
    value: Optional[constr(min_length=0, max_length=4096)] = None


class CreateCustomFieldInstancesDto(BaseModel):
    customFieldInstances: Optional[List[CreateCustomFieldInstanceDto]] = None


class UpdateCustomFieldInstanceDto(BaseModel):
    selectedOptions: Optional[List[UidReference]] = None
    value: Optional[constr(min_length=0, max_length=4096)] = None


class UpdateCustomFieldInstanceWithUidDto(BaseModel):
    customFieldInstance: UidReference
    customField: Optional[UidReference] = None
    selectedOptions: Optional[List[UidReference]] = None
    value: Optional[constr(min_length=0, max_length=4096)] = None


class UpdateCustomFieldInstancesDto(BaseModel):
    addInstances: Optional[List[CreateCustomFieldInstanceDto]] = None
    removeInstances: Optional[List[UidReference]] = None
    updateInstances: Optional[List[UpdateCustomFieldInstanceWithUidDto]] = None


class SplitJobActionDto(BaseModel):
    segmentOrdinals: Optional[List[int]] = Field(
        None, max_items=2147483647, min_items=1
    )
    partCount: Optional[int] = None
    partSize: Optional[int] = None
    wordCount: Optional[int] = None
    byDocumentPart: Optional[bool] = Field(
        None, description="Can be used only for PowerPoint files"
    )


class JobStatusChangeActionDto(BaseModel):
    requestedStatus: Optional[Status] = None
    notifyOwner: Optional[bool] = Field(
        None,
        description="Default: false; Both project owner and job owner are notified;\n                    the parameter is subordinated to notification settings in the project",
    )
    propagateStatus: Optional[bool] = Field(
        None,
        description="Default: false;\n        Controls both job status and email notifications to previous/next provider",
    )


class ContinuousJobInfoDto(BaseModel):
    dateUpdated: Optional[datetime] = None


class Status8(str, Enum):
    RUNNING = "RUNNING"
    ERROR = "ERROR"
    OK = "OK"


class ImportStatusDto(BaseModel):
    status: Optional[Status8] = None
    errorMessage: Optional[str] = None


class JobReference(BaseModel):
    uid: Optional[str] = None
    filename: Optional[str] = None


class ProjectWorkflowStepReference(BaseModel):
    name: Optional[str] = None
    id: Optional[str] = None
    order: Optional[int] = None
    workflowLevel: Optional[int] = None


class SubstituteDto(BaseModel):
    source: str
    target: str


class JobPartReadyReferences(BaseModel):
    jobs: Optional[List[UidReference]] = Field(None, max_items=100, min_items=1)


class UpdateIgnoredWarning(IdReference):
    pass


class JobPartStatusChangeDto(BaseModel):
    status: Optional[Status] = None
    changedDate: Optional[datetime] = None
    changedBy: Optional[UserReference] = None


class JobPartStatusChangesDto(BaseModel):
    statusChanges: Optional[List[JobPartStatusChangeDto]] = None


class JobPartUpdateSingleDto(BaseModel):
    status: Status
    dateDue: Optional[datetime] = None
    providers: Optional[List[ProviderReference]] = None


class JobPartPatchSingleDto(BaseModel):
    status: Optional[Status] = None
    dateDue: Optional[datetime] = None
    providers: Optional[List[ProviderReference]] = None


class TranslationResourcesDto(BaseModel):
    machineTranslateSettings: Optional[MachineTranslateSettingsReference] = None
    translationMemories: Optional[List[ProjectTranslationMemoryReference]] = None
    termBases: Optional[List[ProjectTermBaseReference]] = None


class WorkflowStepDto(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    name: Optional[str] = None
    abbr: Optional[str] = None
    order: Optional[int] = None
    lqaEnabled: Optional[bool] = None


class TargetFileWarningsDto(BaseModel):
    warnings: Optional[List[str]] = None


class PreviewType(str, Enum):
    ORIGINAL = "ORIGINAL"
    PDF = "PDF"


class PreviewUrlDto(BaseModel):
    type: Optional[PreviewType] = None
    url: Optional[str] = None


class PreviewUrlsDto(BaseModel):
    previews: Optional[List[PreviewUrlDto]] = None


class AsyncRequestReference(BaseModel):
    id: Optional[str] = None
    dateCreated: Optional[datetime] = None
    action: Optional[Action] = None


class JobCreateRemoteFileDto(BaseModel):
    connectorToken: str
    remoteFolder: Optional[str] = None
    remoteFileName: str
    remoteFileNameRegex: Optional[bool] = None
    continuous: Optional[bool] = None


class NotifyProviderDto(BaseModel):
    organizationEmailTemplate: IdReference
    notificationIntervalInMinutes: Optional[conint(ge=0, le=1440)] = None


class User(BaseModel):
    id: int


class JobPartUpdateSourceDto(BaseModel):
    uid: Optional[str] = None
    status: Optional[Status] = None
    targetLang: Optional[str] = None
    filename: Optional[str] = None
    workflowLevel: Optional[int] = None
    workflowStep: Optional[WorkflowStepReference] = None


class JobUpdateSourceResponseDto(BaseModel):
    asyncRequest: Optional[AsyncRequestReference] = None
    jobs: Optional[List[JobPartUpdateSourceDto]] = None


class JobPartDeleteReferences(JobPartReferences):
    pass


class Level(str, Enum):
    STANDARD = "STANDARD"
    PRO = "PRO"


class HumanTranslateJobsDto(BaseModel):
    jobs: List[UidReference] = Field(..., max_items=100, min_items=1)
    humanTranslateSettings: IdReference
    comment: Optional[str] = None
    glossaryId: Optional[str] = None
    usePreferredTranslators: Optional[bool] = None
    level: Optional[Level] = None
    callbackUrl: Optional[str] = None


class UpdateSourceMetadataDto(BaseModel):
    """jobs` - **required** - list of jobs UID reference (maximum size `100`)
    - `preTranslate` - pre translate flag (default `false`)
    - `allowAutomaticPostAnalysis` - if automatic post editing analysis should be created. If not specified then value
                                     is taken from the analyse settings of the project
    - `callbackUrl` - consumer callback"""

    jobs: List[UidReference] = Field(..., max_items=100, min_items=1)
    callbackUrl: Optional[str] = None
    allowAutomaticPostAnalysis: Optional[bool] = None
    preTranslate: Optional[bool] = False


class NotifyJobPartsRequestDto(BaseModel):
    jobs: List[UidReference]
    emailTemplate: IdReference
    cc: Optional[List[str]] = None
    bcc: Optional[List[str]] = None


class GetBilingualFileDto(BaseModel):
    jobs: Optional[List[UidReference]] = Field(None, max_items=1000, min_items=1)


class JobPartUpdateBatchDto(BaseModel):
    jobs: Optional[List[UidReference]] = Field(None, max_items=100, min_items=1)
    status: Status
    dateDue: Optional[datetime] = None
    providers: Optional[List[ProviderReference]] = None


class SegmentReference(BaseModel):
    uid: Optional[str] = None


class UpdateIgnoredChecksDto(BaseModel):
    segment: SegmentReference
    warningTypes: List[EnabledCheck] = Field(..., max_items=100, min_items=1)


class SearchJobsRequestDto(BaseModel):
    jobs: List[UidReference] = Field(
        ..., description="Max: 50 records", max_items=50, min_items=1
    )


class QualityAssuranceDto(BaseModel):
    segmentsCount: Optional[int] = None
    warningsCount: Optional[int] = None
    ignoredWarningsCount: Optional[int] = None


class SegmentsCountsDto(BaseModel):
    allConfirmed: Optional[bool] = None
    charsCount: Optional[int] = None
    completedCharsCount: Optional[int] = None
    confirmedCharsCount: Optional[int] = None
    confirmedLockedCharsCount: Optional[int] = None
    lockedCharsCount: Optional[int] = None
    segmentsCount: Optional[int] = None
    completedSegmentsCount: Optional[int] = None
    lockedSegmentsCount: Optional[int] = None
    segmentGroupsCount: Optional[int] = None
    translatedSegmentsCount: Optional[int] = None
    translatedLockedSegmentsCount: Optional[int] = None
    wordsCount: Optional[int] = None
    completedWordsCount: Optional[int] = None
    confirmedWordsCount: Optional[int] = None
    confirmedLockedWordsCount: Optional[int] = None
    lockedWordsCount: Optional[int] = None
    addedSegments: Optional[int] = None
    addedWords: Optional[int] = None
    machineTranslationPostEditedSegmentsCount: Optional[int] = None
    machineTranslationRelevantSegmentsCount: Optional[int] = None
    qualityAssurance: Optional[QualityAssuranceDto] = None
    qualityAssuranceResolved: Optional[bool] = None


class ImportStatusDtoV2(ImportStatusDto):
    pass


class JobRemoteFileReference(BaseModel):
    humanReadableFolder: Optional[str] = None
    humanReadableFileName: Optional[str] = None
    encodedFolder: Optional[str] = None
    encodedFileName: Optional[str] = None


class TermBaseDto(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    internalId: Optional[int] = None
    name: str
    langs: Optional[List[str]] = None
    client: Optional[ClientReference] = None
    domain: Optional[DomainReference] = None
    subDomain: Optional[SubDomainReference] = None
    businessUnit: Optional[BusinessUnitReference] = None
    createdBy: Optional[UserReference] = None
    owner: Optional[UserReference] = None
    dateCreated: Optional[datetime] = None
    note: Optional[str] = None
    canShow: Optional[bool] = None


class Status17(str, Enum):
    New = "New"
    Approved = "Approved"


class TermDto(BaseModel):
    id: Optional[str] = None
    text: str
    lang: Optional[str] = None
    rtl: Optional[bool] = None
    modifiedAt: Optional[datetime] = None
    createdAt: Optional[datetime] = None
    modifiedBy: Optional[UserReference] = None
    createdBy: Optional[UserReference] = None
    caseSensitive: Optional[bool] = None
    exactMatch: Optional[bool] = None
    forbidden: Optional[bool] = None
    preferred: Optional[bool] = None
    status: Optional[Status17] = None
    conceptId: Optional[str] = None
    usage: Optional[str] = None
    note: Optional[str] = None
    writable: Optional[bool] = None
    shortTranslation: Optional[str] = None
    termType: Optional[str] = None
    partOfSpeech: Optional[str] = None
    gender: Optional[str] = None
    number: Optional[str] = None
    definition: Optional[str] = None
    domain: Optional[str] = None
    subDomains: Optional[List[str]] = None
    url: Optional[str] = None
    conceptNote: Optional[str] = None


class Match(BaseModel):
    beginIndex: Optional[int] = None
    text: Optional[str] = None


class TermPairDto(BaseModel):
    sourceTerm: TermDto
    targetTerm: TermDto


class TermType(str, Enum):
    FULL_FORM = "FULL_FORM"
    SHORT_FORM = "SHORT_FORM"
    ACRONYM = "ACRONYM"
    ABBREVIATION = "ABBREVIATION"
    PHRASE = "PHRASE"
    VARIANT = "VARIANT"


class PartOfSpeech(str, Enum):
    ADJECTIVE = "ADJECTIVE"
    NOUN = "NOUN"
    VERB = "VERB"
    ADVERB = "ADVERB"


class Gender(str, Enum):
    MASCULINE = "MASCULINE"
    FEMININE = "FEMININE"
    NEUTRAL = "NEUTRAL"


class Number1(str, Enum):
    SINGULAR = "SINGULAR"
    PLURAL = "PLURAL"
    UNCOUNTABLE = "UNCOUNTABLE"


class TermCreateByJobDto(BaseModel):
    text: str
    caseSensitive: Optional[bool] = Field(None, description="Default: false")
    exactMatch: Optional[bool] = Field(None, description="Default: false")
    forbidden: Optional[bool] = Field(None, description="Default: false")
    preferred: Optional[bool] = Field(None, description="Default: false")
    usage: Optional[str] = None
    note: Optional[str] = None
    shortTranslation: Optional[str] = None
    termType: Optional[TermType] = None
    partOfSpeech: Optional[PartOfSpeech] = None
    gender: Optional[Gender] = None
    number: Optional[Number1] = None


class CreateReferenceFileNoteDto(BaseModel):
    note: str


class ReferenceFileAccessDto(BaseModel):
    canCreate: Optional[bool] = None


class ReferenceFilePageDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[ReferenceFileReference]] = None
    access: Optional[ReferenceFileAccessDto] = None


class ProjectReferenceFilesRequestDto(BaseModel):
    referenceFiles: List[IdReference]


class UserReferencesDto(BaseModel):
    users: Optional[List[UserReference]] = None


class TransMemoryDto(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    internalId: Optional[int] = None
    name: Optional[str] = None
    sourceLang: Optional[str] = None
    targetLangs: Optional[List[str]] = None
    client: Optional[ClientReference] = None
    businessUnit: Optional[BusinessUnitReference] = None
    domain: Optional[DomainReference] = None
    subDomain: Optional[SubDomainReference] = None
    note: Optional[str] = None
    dateCreated: Optional[datetime] = None
    createdBy: Optional[UserReference] = None
    owner: Optional[UserReference] = None


class AssignmentPerTargetLangDto(ProjectTemplateWorkflowSettingsAssignedToDto):
    pass


class ProjectTemplateNotifyProviderDto(BaseModel):
    organizationEmailTemplate: ObjectReference
    notificationIntervalInMinutes: Optional[conint(ge=0, le=1440)] = None


class ProjectWorkflowSettingsDto(BaseModel):
    completeUnassigned: Optional[bool] = None
    propagateTranslationsToLowerWfDuringUpdateSource: Optional[bool] = None


class WorkflowStepSettingsDto(BaseModel):
    workflowStep: Optional[WorkflowStepReference] = None
    assignedTo: Optional[List[ProjectTemplateWorkflowSettingsAssignedToDto]] = None
    notifyProvider: Optional[ProjectTemplateNotifyProviderDto] = None
    lqaProfile: Optional[UidReference] = None


class ProjectTemplateCreateActionDto(BaseModel):
    project: UidReference
    name: constr(min_length=0, max_length=255)
    importSettings: Optional[UidReference] = None
    useDynamicTitle: Optional[bool] = None
    dynamicTitle: Optional[constr(min_length=0, max_length=255)] = None


class WorkflowStepSettingsEditDto(BaseModel):
    workflowStep: Optional[IdReference] = None
    assignedTo: Optional[List[ProjectTemplateWorkflowSettingsAssignedToDto]] = None
    notifyProvider: Optional[ProjectTemplateNotifyProviderDto] = None
    lqaProfile: Optional[UidReference] = None


class ProjectTemplateReference(BaseModel):
    templateName: Optional[str] = None
    sourceLang: Optional[str] = None
    targetLangs: Optional[List[str]] = None
    id: Optional[str] = None
    uid: Optional[str] = None
    owner: Optional[UserReference] = None
    domain: Optional[DomainReference] = None
    subDomain: Optional[SubDomainReference] = None
    costCenter: Optional[CostCenterReference] = None
    businessUnit: Optional[BusinessUnitReference] = None
    projectWorkflowSettings: Optional[ProjectWorkflowSettingsReference] = None
    note: Optional[str] = None
    client: Optional[ClientReference] = None


class AbstractAnalyseSettingsDto(BaseModel):
    type: Optional[AnalysisType] = Field(
        None, description="Response differs based on analyse type"
    )
    includeConfirmedSegments: Optional[bool] = Field(None, description="Default: false")
    includeNumbers: Optional[bool] = Field(None, description="Default: false")
    includeLockedSegments: Optional[bool] = Field(None, description="Default: false")
    countSourceUnits: Optional[bool] = Field(None, description="Default: false")
    includeTransMemory: Optional[bool] = Field(None, description="Default: false")
    namingPattern: Optional[str] = None
    analyzeByLanguage: Optional[bool] = Field(None, description="Default: false")
    analyzeByProvider: Optional[bool] = Field(None, description="Default: false")
    allowAutomaticPostAnalysis: Optional[bool] = Field(
        None,
        description="If automatic post analysis should be created after update source. Default: false",
    )


class PostAnalyse(AbstractAnalyseSettingsDto):
    transMemoryPostEditing: Optional[bool] = Field(None, description="Default: false")
    nonTranslatablePostEditing: Optional[bool] = Field(
        None, description="Default: false"
    )
    machineTranslatePostEditing: Optional[bool] = Field(
        None, description="Default: false"
    )


class PreAnalyse(AbstractAnalyseSettingsDto):
    includeFuzzyRepetitions: Optional[bool] = Field(None, description="Default: false")
    separateFuzzyRepetitions: Optional[bool] = Field(None, description="Default: false")
    includeNonTranslatables: Optional[bool] = Field(None, description="Default: false")
    includeMachineTranslationMatches: Optional[bool] = Field(
        None, description="Default: false"
    )


class PreAnalyseTargetCompare(AbstractAnalyseSettingsDto):
    transMemoryPostEditing: Optional[bool] = Field(None, description="Default: false")
    nonTranslatablePostEditing: Optional[bool] = Field(
        None, description="Default: false"
    )
    machineTranslatePostEditing: Optional[bool] = Field(
        None, description="Default: false"
    )
    includeFuzzyRepetitions: Optional[bool] = Field(None, description="Default: false")
    separateFuzzyRepetitions: Optional[bool] = Field(None, description="Default: false")
    includeNonTranslatables: Optional[bool] = Field(None, description="Default: false")
    includeMachineTranslationMatches: Optional[bool] = Field(
        None, description="Default: false"
    )


class EditAnalyseSettingsDto(BaseModel):
    type: Optional[AnalysisType] = None
    includeFuzzyRepetitions: Optional[bool] = Field(None, description="Default: false")
    separateFuzzyRepetitions: Optional[bool] = Field(None, description="Default: false")
    includeNonTranslatables: Optional[bool] = Field(None, description="Default: false")
    includeMachineTranslationMatches: Optional[bool] = Field(
        None, description="Default: false"
    )
    includeConfirmedSegments: Optional[bool] = Field(None, description="Default: false")
    includeNumbers: Optional[bool] = Field(None, description="Default: false")
    includeLockedSegments: Optional[bool] = Field(None, description="Default: false")
    transMemoryPostEditing: Optional[bool] = Field(None, description="Default: false")
    nonTranslatablePostEditing: Optional[bool] = Field(
        None, description="Default: false"
    )
    machineTranslatePostEditing: Optional[bool] = Field(
        None, description="Default: false"
    )
    countSourceUnits: Optional[bool] = Field(None, description="Default: false")
    includeTransMemory: Optional[bool] = Field(None, description="Default: false")
    namingPattern: Optional[constr(min_length=0, max_length=255)] = None
    analyzeByLanguage: Optional[bool] = Field(
        None, description="Mutually exclusive with analyzeByProvider. Default: false"
    )
    analyzeByProvider: Optional[bool] = Field(
        None, description="Mutually exclusive with analyzeByLanguage. Default: true"
    )
    allowAutomaticPostAnalysis: Optional[bool] = Field(
        None, description="Default: false"
    )


class ProjectTemplateTermBaseDto(BaseModel):
    targetLocale: Optional[str] = None
    workflowStep: Optional[WorkflowStepReference] = None
    readMode: Optional[bool] = None
    writeMode: Optional[bool] = None
    termBase: Optional[TermBaseDto] = None
    qualityAssurance: Optional[bool] = None


class ProjectTemplateTermBaseListDto(BaseModel):
    termBases: Optional[List[ProjectTemplateTermBaseDto]] = None


class SetProjectTemplateTermBaseDto(BaseModel):
    readTermBases: Optional[List[IdReference]] = None
    writeTermBase: Optional[IdReference] = None
    qualityAssuranceTermBases: Optional[List[IdReference]] = None
    targetLang: Optional[str] = None
    workflowStep: Optional[IdReference] = None


class ProjectSecuritySettingsDtoV2(BaseModel):
    downloadEnabled: Optional[bool] = None
    webEditorEnabledForLinguists: Optional[bool] = None
    showUserDataToLinguists: Optional[bool] = None
    emailNotifications: Optional[bool] = None
    strictWorkflowFinish: Optional[bool] = None
    useVendors: Optional[bool] = None
    linguistsMayEditLockedSegments: Optional[bool] = None
    usersMaySetAutoPropagation: Optional[bool] = None
    allowLoadingExternalContentInEditors: Optional[bool] = None
    allowLoadingIframes: Optional[bool] = None
    linguistsMayEditSource: Optional[bool] = None
    linguistsMayEditTagContent: Optional[bool] = None
    linguistsMayDownloadLqaReport: Optional[bool] = None
    usernamesDisplayedInLqaReport: Optional[bool] = None
    userMaySetInstantQA: Optional[bool] = None
    triggerWebhooks: Optional[bool] = None
    vendors: Optional[VendorSecuritySettingsDto] = None
    allowedDomains: Optional[List[str]] = None


class EditProjectSecuritySettingsDtoV2(BaseModel):
    downloadEnabled: Optional[bool] = Field(None, description="Default: `false`")
    webEditorEnabledForLinguists: Optional[bool] = Field(
        None, description="Default: `false`"
    )
    showUserDataToLinguists: Optional[bool] = Field(
        None, description="Default: `false`"
    )
    emailNotifications: Optional[bool] = Field(None, description="Default: `false`")
    strictWorkflowFinish: Optional[bool] = Field(None, description="Default: `false`")
    useVendors: Optional[bool] = Field(None, description="Default: `false`")
    linguistsMayEditLockedSegments: Optional[bool] = Field(
        None, description="Default: `false`"
    )
    usersMaySetAutoPropagation: Optional[bool] = Field(
        None, description="Default: `true`"
    )
    allowLoadingExternalContentInEditors: Optional[bool] = Field(
        None, description="Default: `true`"
    )
    allowLoadingIframes: Optional[bool] = Field(None, description="Default: `false`")
    linguistsMayEditSource: Optional[bool] = Field(None, description="Default: `true`")
    linguistsMayEditTagContent: Optional[bool] = Field(
        None, description="Default: `true`"
    )
    linguistsMayDownloadLqaReport: Optional[bool] = Field(
        None, description="Default: `true`"
    )
    usernamesDisplayedInLqaReport: Optional[bool] = Field(
        None, description="Default: `true`"
    )
    userMaySetInstantQA: Optional[bool] = Field(None, description="Default: `true`")
    triggerWebhooks: Optional[bool] = Field(None, description="Default: `true`")
    notifyJobOwnerStatusChanged: Optional[bool] = Field(
        None, description="Default: `false`"
    )
    vendors: Optional[VendorSecuritySettingsDto] = None
    allowedDomains: Optional[List[str]] = None


class ProjectTermBaseDto(ProjectTemplateTermBaseDto):
    pass


class ProjectTermBaseListDto(BaseModel):
    termBases: Optional[List[ProjectTermBaseDto]] = None


class SetTermBaseDto(BaseModel):
    readTermBases: Optional[List[IdReference]] = None
    writeTermBase: Optional[IdReference] = None
    qualityAssuranceTermBases: Optional[List[IdReference]] = None
    targetLang: Optional[str] = None


class PageDtoTermBaseDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[TermBaseDto]] = None


class SearchTMRequestDto(BaseModel):
    segment: str
    workflowLevel: Optional[conint(ge=1, le=15)] = None
    scoreThreshold: Optional[confloat(ge=0.0, le=1.01)] = None
    previousSegment: Optional[str] = None
    nextSegment: Optional[str] = None
    contextKey: Optional[str] = None
    maxSegments: Optional[conint(ge=0, le=5)] = Field(None, description="Default: 5")
    maxSubSegments: Optional[conint(ge=0, le=5)] = Field(None, description="Default: 5")
    tagMetadata: Optional[List[TagMetadataDto]] = None
    targetLangs: List[str] = Field(..., max_items=2147483647, min_items=1)


class EmailQuotesResponseDto(BaseModel):
    recipients: Optional[List[str]] = None


class EmailQuotesRequestDto(BaseModel):
    quotes: List[UidReference]
    subject: str
    body: str
    cc: Optional[str] = None
    bcc: Optional[str] = None


class AttributeType(str, Enum):
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    DECIMAL = "DECIMAL"
    INTEGER = "INTEGER"
    DATE_TIME = "DATE_TIME"
    BINARY = "BINARY"
    REFERENCE = "REFERENCE"
    COMPLEX = "COMPLEX"


class Mutability(str, Enum):
    READ_ONLY = "READ_ONLY"
    READ_WRITE = "READ_WRITE"
    IMMUTABLE = "IMMUTABLE"
    WRITE_ONLY = "WRITE_ONLY"


class Returned(str, Enum):
    ALWAYS = "ALWAYS"
    NEVER = "NEVER"
    DEFAULT = "DEFAULT"
    REQUEST = "REQUEST"


class Uniqueness(str, Enum):
    NONE = "NONE"
    SERVER = "SERVER"
    GLOBAL = "GLOBAL"


class Attribute(BaseModel):
    name: Optional[str] = None
    type: Optional[AttributeType] = None
    subAttributes: Optional[List[Attribute]] = None
    multiValued: Optional[bool] = None
    description: Optional[str] = None
    required: Optional[bool] = None
    caseExact: Optional[bool] = None
    mutability: Optional[Mutability] = None
    returned: Optional[Returned] = None
    uniqueness: Optional[Uniqueness] = None


class ScimResourceSchema(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    attributes: Optional[List[Attribute]] = None


class AuthSchema(BaseModel):
    type: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    specUrl: Optional[str] = None
    primary: Optional[bool] = None


class Supported(BaseModel):
    supported: Optional[bool] = None


class SchemaExtension(BaseModel):
    schema_: Optional[str] = Field(None, alias="schema")
    required: Optional[bool] = None


class ScimResourceTypeSchema(BaseModel):
    schemas: Optional[List[str]] = None
    id: Optional[str] = None
    name: Optional[str] = None
    endpoint: Optional[str] = None
    description: Optional[str] = None
    schema_: Optional[str] = Field(None, alias="schema")
    schemaExtensions: Optional[List[SchemaExtension]] = None


class Email(BaseModel):
    value: Optional[str] = None
    type: Optional[str] = None
    primary: Optional[bool] = Field(None, description="Default: false")


class Name2(BaseModel):
    givenName: str
    familyName: str


class ScimMeta(BaseModel):
    created: Optional[datetime] = None
    location: Optional[str] = None


class ScimUserCoreDto(BaseModel):
    id: Optional[str] = None
    userName: str
    name: Name2
    active: Optional[bool] = Field(None, description="Default: true")
    emails: List[Email] = Field(..., max_items=2147483647, min_items=1)
    meta: Optional[ScimMeta] = None


class SegmentationRuleDto(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    name: str
    locale: Optional[str] = None
    primary: Optional[bool] = Field(None, description="Default: false")
    filename: str
    dateCreated: Optional[datetime] = None
    createdBy: Optional[UserReference] = Field(None, description="created by user")


class SegmentationRuleReference(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    name: str
    locale: Optional[str] = None
    primary: Optional[bool] = Field(None, description="Default: false")
    filename: str
    dateCreated: Optional[datetime] = None


class EditSegmentationRuleDto(BaseModel):
    name: constr(min_length=0, max_length=255)
    primary: Optional[bool] = Field(None, description="Default: false")


class MisspelledWord(BaseModel):
    word: Optional[str] = None
    offset: Optional[int] = None


class SpellCheckRequestDto(BaseModel):
    lang: str
    texts: List[str]
    referenceTexts: Optional[List[str]] = None
    zeroLengthSeparator: Optional[str] = None


class Suggestion(BaseModel):
    text: Optional[str] = None


class SuggestRequestDto(BaseModel):
    lang: str
    words: List[str]
    referenceTexts: Optional[List[str]] = None


class DictionaryItemDto(BaseModel):
    lang: str
    word: str


class SubDomainDto(BusinessUnitDto):
    pass


class PageDtoSubDomainDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[SubDomainDto]] = None


class SubDomainEditDto(CostCenterEditDto):
    pass


class MetadataTbDto(BaseModel):
    termsCount: Optional[int] = None
    metadataByLanguage: Optional[Dict[str, int]] = None


class TermBaseEditDto(BaseModel):
    name: constr(min_length=0, max_length=255)
    langs: List[str] = Field(..., max_items=2147483647, min_items=1)
    client: Optional[IdReference] = None
    domain: Optional[IdReference] = None
    subDomain: Optional[IdReference] = None
    businessUnit: Optional[IdReference] = None
    owner: Optional[IdReference] = Field(
        None, description="Owner of the TM must be Admin or PM"
    )
    note: Optional[constr(min_length=0, max_length=4096)] = None


class ImportTermBaseResponseDto(BaseModel):
    langs: Optional[List[str]] = None
    createdTermsCount: Optional[int] = None
    updatedTermsCount: Optional[int] = None


class ConceptWithMetadataDto(BaseModel):
    id: Optional[str] = None
    domain: Optional[DomainReference] = None
    subdomains: Optional[List[SubDomainReference]] = None
    url: Optional[str] = None
    definition: Optional[str] = None
    conceptNote: Optional[str] = None


class ConceptEditDto(BaseModel):
    domain: Optional[UidReference] = None
    subdomains: Optional[List[UidReference]] = None
    definition: Optional[str] = None
    url: Optional[str] = None
    conceptNote: Optional[str] = None


class TermCreateDto(BaseModel):
    text: str
    lang: str
    caseSensitive: Optional[bool] = Field(None, description="Default: false")
    exactMatch: Optional[bool] = Field(None, description="Default: false")
    forbidden: Optional[bool] = Field(None, description="Default: false")
    preferred: Optional[bool] = Field(None, description="Default: false")
    status: Optional[Status17] = None
    conceptId: Optional[str] = None
    usage: Optional[str] = None
    note: Optional[str] = None
    shortTranslation: Optional[str] = None
    termType: Optional[TermType] = None
    partOfSpeech: Optional[PartOfSpeech] = None
    gender: Optional[Gender] = None
    number: Optional[Number1] = None


class TermEditDto(BaseModel):
    text: str
    lang: Optional[str] = None
    caseSensitive: Optional[bool] = Field(None, description="Default: false")
    exactMatch: Optional[bool] = Field(None, description="Default: false")
    forbidden: Optional[bool] = Field(None, description="Default: false")
    preferred: Optional[bool] = Field(None, description="Default: false")
    status: Optional[Status17] = None
    usage: Optional[str] = None
    note: Optional[str] = None
    shortTranslation: Optional[str] = None
    termType: Optional[TermType] = None
    partOfSpeech: Optional[PartOfSpeech] = None
    gender: Optional[Gender] = None
    number: Optional[Number1] = None


class ConceptListReference(BaseModel):
    concepts: List[IdReference] = Field(..., max_items=100, min_items=1)


class ConceptDto(BaseModel):
    id: Optional[str] = None
    writable: Optional[bool] = None
    terms: Optional[List[List[TermDto]]] = None


class BrowseResponseListDto(BaseModel):
    searchResults: Optional[List[ConceptDto]] = None


class BrowseRequestDto(BaseModel):
    queryLang: Optional[str] = None
    query: Optional[str] = None
    status: Optional[str] = None
    pageNumber: Optional[int] = None
    pageSize: Optional[conint(ge=1, le=50)] = None


class TermBaseSearchRequestDto(BaseModel):
    targetLangs: List[str]
    sourceLang: str
    query: str
    status: Optional[Status17] = None


class SearchRequestDto(BaseModel):
    query: str
    sourceLang: str
    targetLangs: Optional[List[str]] = None
    previousSegment: Optional[str] = None
    nextSegment: Optional[str] = None
    tagMetadata: Optional[List[TagMetadataDto]] = None
    trimQuery: Optional[bool] = Field(
        None,
        description="Remove leading and trailing whitespace from query. Default: true",
    )
    phraseQuery: Optional[bool] = Field(
        None, description="Return both wildcard and exact search results. Default: true"
    )


class TransMemoryCreateDto(BaseModel):
    name: constr(min_length=0, max_length=255)
    sourceLang: str
    targetLangs: List[str]
    client: Optional[IdReference] = None
    businessUnit: Optional[IdReference] = None
    domain: Optional[IdReference] = None
    subDomain: Optional[IdReference] = None
    note: Optional[constr(min_length=0, max_length=4096)] = None


class TransMemoryEditDto(BaseModel):
    name: constr(min_length=0, max_length=255)
    targetLangs: List[str] = Field(
        ..., description="New target languages to add. No languages can be removed"
    )
    client: Optional[IdReference] = None
    businessUnit: Optional[IdReference] = None
    domain: Optional[IdReference] = None
    subDomain: Optional[IdReference] = None
    owner: Optional[IdReference] = Field(
        None, description="Owner of the TM must be Admin or PM"
    )
    note: Optional[constr(min_length=0, max_length=4096)] = None


class TargetLanguageDto(BaseModel):
    language: str


class OutputFormat(str, Enum):
    TXT = "TXT"
    TSV = "TSV"


class CleanedTransMemoriesDto(BaseModel):
    uids: List[str]
    outputFormat: Optional[OutputFormat] = None
    preserveRatio: Optional[confloat(le=1.0, gt=0.0)] = None
    targetLangs: Optional[List[str]] = None


class SegmentDto(BaseModel):
    targetLang: str
    sourceSegment: str
    targetSegment: str
    previousSourceSegment: Optional[str] = None
    nextSourceSegment: Optional[str] = None
    sourceTagMetadata: Optional[List[TagMetadataDto]] = None
    targetTagMetadata: Optional[List[TagMetadataDto]] = None


class LanguageMetadata1(BaseModel):
    segmentsCount: Optional[int] = None


class TranslationDto(BaseModel):
    lang: str
    text: str


class WildCardSearchRequestDto(BaseModel):
    query: Optional[str] = None
    sourceLang: str
    targetLangs: Optional[List[str]] = None
    count: Optional[conint(ge=1, le=50)] = None
    offset: Optional[int] = None
    sourceLangs: Optional[List[str]] = None


class Query(BaseModel):
    query: Optional[str] = None
    lang: Optional[str] = None


class ExportByQueryDto(BaseModel):
    exportTargetLangs: List[str]
    queries: List[str]
    queryLangs: List[str]
    createdAtMin: Optional[datetime] = None
    createdAtMax: Optional[datetime] = None
    modifiedAtMin: Optional[datetime] = None
    modifiedAtMax: Optional[datetime] = None
    createdBy: Optional[IdReference] = None
    modifiedBy: Optional[IdReference] = None
    filename: Optional[str] = None
    project: Optional[UidReference] = None
    callbackUrl: Optional[str] = None


class TranslationRequestDto(BaseModel):
    sourceTexts: List[str] = Field(..., max_items=2147483647, min_items=1)


class TranslationPriceDto(BaseModel):
    workflowStep: Optional[WorkflowStepDto] = None
    price: Optional[float] = None


class TranslationPriceSetDto(BaseModel):
    sourceLang: Optional[str] = None
    targetLang: Optional[str] = None
    minimumPrice: Optional[float] = None
    prices: Optional[List[TranslationPriceDto]] = None


class BillingUnit2(str, Enum):
    Word = "Word"
    Page = "Page"
    Character = "Character"
    Hour = "Hour"


class TranslationPriceListCreateDto(BaseModel):
    name: str
    currencyCode: str
    billingUnit: Optional[BillingUnit2] = Field(None, description="Default: Word")


class TranslationPriceSetListDto(BaseModel):
    priceSets: Optional[List[TranslationPriceSetDto]] = None


class TranslationPriceSetCreateDto(BaseModel):
    sourceLanguages: List[str] = Field(..., max_items=100, min_items=1)
    targetLanguages: List[str] = Field(..., max_items=100, min_items=1)


class TranslationPriceSetBulkDeleteDto(BaseModel):
    sourceLanguages: Optional[List[str]] = None
    targetLanguages: Optional[List[str]] = None


class PageDtoTranslationPriceSetDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[TranslationPriceSetDto]] = None


class TranslationPriceSetBulkMinimumPricesDto(BaseModel):
    sourceLanguages: Optional[List[str]] = None
    targetLanguages: Optional[List[str]] = None
    minimumPrice: Optional[float] = None


class TranslationPriceSetBulkPricesDto(BaseModel):
    sourceLanguages: Optional[List[str]] = None
    targetLanguages: Optional[List[str]] = None
    price: Optional[float] = None
    workflowSteps: Optional[List[IdReference]] = Field(None, max_items=15, min_items=0)


class AssignedJobDto(BaseModel):
    uid: Optional[str] = None
    innerId: Optional[str] = None
    filename: Optional[str] = None
    dateDue: Optional[datetime] = None
    dateCreated: Optional[datetime] = None
    status: Optional[Status] = None
    targetLang: Optional[str] = None
    sourceLang: Optional[str] = None
    project: Optional[ProjectReference] = None
    workflowStep: Optional[ProjectWorkflowStepReference] = None
    importStatus: Optional[ImportStatusDto] = None
    imported: Optional[bool] = None


class PageDtoAssignedJobDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[AssignedJobDto]] = None


class UserPasswordEditDto(BaseModel):
    password: constr(min_length=8, max_length=255)


class UserDto(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    userName: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    dateCreated: Optional[datetime] = None
    dateDeleted: Optional[datetime] = None
    createdBy: Optional[UserReference] = None
    role: Optional[Role] = None
    timezone: Optional[str] = None
    note: Optional[str] = None
    terminologist: Optional[bool] = None
    sourceLangs: Optional[List[str]] = None
    targetLangs: Optional[List[str]] = None
    active: Optional[bool] = None
    priceList: Optional[PriceListReference] = None
    netRateScheme: Optional[DiscountSchemeReference] = None


class PageDtoProjectReference(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[ProjectReference]] = None


class UserStatisticsDto(BaseModel):
    date: Optional[datetime] = None
    ipAddress: Optional[str] = None
    ipCountry: Optional[str] = None
    userAgent: Optional[str] = None


class UserStatisticsListDto(BaseModel):
    userStatistics: List[UserStatisticsDto]


class PageDtoUserDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[UserDto]] = None


class PageDtoWorkflowStepReference(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[WorkflowStepReference]] = None


class PageDtoString(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[str]] = None


class LastLoginDto(BaseModel):
    user: Optional[UserReference] = None
    lastLoginDate: Optional[datetime] = None


class PageDtoLastLoginDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[LastLoginDto]] = None


class VendorDto(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    name: Optional[str] = None
    vendorToken: Optional[str] = None
    priceList: Optional[PriceListReference] = None
    netRateScheme: Optional[DiscountSchemeReference] = None
    sourceLocales: Optional[List[str]] = None
    targetLocales: Optional[List[str]] = None
    clients: Optional[List[ClientReference]] = None
    domains: Optional[List[DomainReference]] = None
    subDomains: Optional[List[SubDomainReference]] = None
    workflowSteps: Optional[List[WorkflowStepReference]] = None


class PageDtoVendorDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[VendorDto]] = None


class CreateVendorDto(BaseModel):
    vendorToken: str
    netRateScheme: Optional[UidReference] = None
    priceList: Optional[UidReference] = None
    sourceLocales: Optional[List[str]] = None
    targetLocales: Optional[List[str]] = None
    clients: Optional[List[UidReference]] = None
    domains: Optional[List[UidReference]] = None
    subDomains: Optional[List[UidReference]] = None
    workflowSteps: Optional[List[UidReference]] = None


class TriggerEvent(str, Enum):
    JOB_STATUS_CHANGED = "JOB_STATUS_CHANGED"
    JOB_CREATED = "JOB_CREATED"
    JOB_DELETED = "JOB_DELETED"
    JOB_UNSHARED = "JOB_UNSHARED"
    JOB_ASSIGNED = "JOB_ASSIGNED"
    JOB_DUE_DATE_CHANGED = "JOB_DUE_DATE_CHANGED"
    JOB_UPDATED = "JOB_UPDATED"
    JOB_TARGET_UPDATED = "JOB_TARGET_UPDATED"
    JOB_EXPORTED = "JOB_EXPORTED"
    JOB_UNEXPORTED = "JOB_UNEXPORTED"
    PROJECT_CREATED = "PROJECT_CREATED"
    PROJECT_DELETED = "PROJECT_DELETED"
    PROJECT_UNSHARED = "PROJECT_UNSHARED"
    PROJECT_STATUS_CHANGED = "PROJECT_STATUS_CHANGED"
    PROJECT_DUE_DATE_CHANGED = "PROJECT_DUE_DATE_CHANGED"
    SHARED_PROJECT_ASSIGNED = "SHARED_PROJECT_ASSIGNED"
    PROJECT_METADATA_UPDATED = "PROJECT_METADATA_UPDATED"
    PRE_TRANSLATION_FINISHED = "PRE_TRANSLATION_FINISHED"
    ANALYSIS_CREATED = "ANALYSIS_CREATED"
    CONTINUOUS_JOB_UPDATED = "CONTINUOUS_JOB_UPDATED"
    PROJECT_TEMPLATE_CREATED = "PROJECT_TEMPLATE_CREATED"
    PROJECT_TEMPLATE_UPDATED = "PROJECT_TEMPLATE_UPDATED"
    PROJECT_TEMPLATE_DELETED = "PROJECT_TEMPLATE_DELETED"
    RAW_MT_CONVERTER_IMPORT_FINISHED = "RAW_MT_CONVERTER_IMPORT_FINISHED"
    RAW_MT_PRE_TRANSLATION_FINISHED = "RAW_MT_PRE_TRANSLATION_FINISHED"
    RAW_MT_QUALITY_ESTIMATION_FINISHED = "RAW_MT_QUALITY_ESTIMATION_FINISHED"


class WebhookCallDto(BaseModel):
    uid: Optional[str] = None
    parentUid: Optional[str] = None
    eventUid: Optional[str] = None
    webhookSettings: Optional[UidReference] = None
    createdAt: Optional[datetime] = None
    url: Optional[str] = None
    forced: Optional[bool] = None
    lastForcedAt: Optional[datetime] = None
    body: Optional[str] = None
    triggerEvent: Optional[TriggerEvent] = None
    retryAttempt: Optional[int] = None
    statusCode: Optional[int] = None
    errorMessage: Optional[str] = None


class ReplayRequestDto(BaseModel):
    webhookCalls: Optional[List[UidReference]] = None


class PageDtoWorkflowStepDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[WorkflowStepDto]] = None


class CreateWorkflowStepDto(BaseModel):
    name: constr(min_length=1, max_length=255) = Field(
        ..., description="Name of the lqa workflow step"
    )
    order: Optional[int] = Field(None, description="Order value")
    lqaEnabled: Optional[bool] = Field(None, description="Default: false")
    abbr: constr(min_length=1, max_length=3) = Field(..., description="Abbreviation")


class EditWorkflowStepDto(BaseModel):
    name: Optional[constr(min_length=1, max_length=255)] = Field(
        None, description="Name of the lqa workflow step"
    )
    order: Optional[int] = Field(None, description="Order value")
    lqaEnabled: Optional[bool] = Field(None, description="Default: false")
    abbr: Optional[constr(min_length=1, max_length=3)] = Field(
        None, description="Abbreviation"
    )


class XmlAssistantProfileListDto(BaseModel):
    uid: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    createdAt: Optional[datetime] = None
    createdBy: Optional[UserReference] = None
    updatedAt: Optional[datetime] = None
    updatedBy: Optional[UserReference] = None


class MatchCountsNTDto(MatchCountsDto):
    pass


class BulkEditAnalyseV2Dto(BaseModel):
    analyses: List[IdReference] = Field(..., max_items=100, min_items=1)
    name: Optional[constr(min_length=0, max_length=255)] = None
    provider: Optional[ProviderReference] = None
    netRateScheme: Optional[UidReference] = None


class ErrorDetailDtoV2(ErrorDetailDto):
    pass


class CreateAnalyseAsyncV2Dto(BaseModel):
    jobs: List[UidReference] = Field(..., max_items=50000, min_items=1)
    type: Optional[AnalysisType] = Field(None, description="default: PreAnalyse")
    includeFuzzyRepetitions: Optional[bool] = Field(None, description="Default: true")
    separateFuzzyRepetitions: Optional[bool] = Field(None, description="Default: false")
    includeConfirmedSegments: Optional[bool] = Field(None, description="Default: true")
    includeNumbers: Optional[bool] = Field(None, description="Default: true")
    includeLockedSegments: Optional[bool] = Field(None, description="Default: true")
    countSourceUnits: Optional[bool] = Field(None, description="Default: true")
    includeTransMemory: Optional[bool] = Field(
        None, description="Default: true. Works only for type=PreAnalyse."
    )
    includeNonTranslatables: Optional[bool] = Field(
        None, description="Default: false. Works only for type=PreAnalyse."
    )
    includeMachineTranslationMatches: Optional[bool] = Field(
        None, description="Default: false. Works only for type=PreAnalyse."
    )
    transMemoryPostEditing: Optional[bool] = Field(
        None, description="Default: false. Works only for type=PostAnalyse."
    )
    nonTranslatablePostEditing: Optional[bool] = Field(
        None, description="Default: false. Works only for type=PostAnalyse."
    )
    machineTranslatePostEditing: Optional[bool] = Field(
        None, description="Default: false. Works only for type=PostAnalyse."
    )
    name: Optional[constr(min_length=0, max_length=255)] = None
    netRateScheme: Optional[IdReference] = None
    compareWorkflowLevel: Optional[conint(ge=1, le=15)] = Field(
        None, description="Required for type=Compare"
    )
    useProjectAnalysisSettings: Optional[bool] = Field(
        None,
        description="Default: false. Use default project settings. Will be overwritten with setting sent\n        in the API call.",
    )
    callbackUrl: Optional[str] = None
    provider: Optional[ProviderReference] = None


class EditAnalyseV2Dto(BaseModel):
    name: Optional[constr(min_length=0, max_length=255)] = None
    provider: Optional[ProviderReference] = None
    netRateScheme: Optional[UidReference] = None


class MultipartFile(BaseModel):
    contentType: Optional[str] = None
    name: Optional[str] = None
    empty: Optional[bool] = None
    bytes: Optional[List[str]] = None
    size: Optional[int] = None
    inputStream: Optional[InputStream] = None
    originalFilename: Optional[str] = None


class UploadBilingualFileRequestDto(BaseModel):
    file: MultipartFile = Field(
        ..., description="One or more bilingual files and/or ZIP archives (max 50)"
    )


class Action3(str, Enum):
    GUI_UPLOAD = "GUI_UPLOAD"
    GUI_DOWNLOAD = "GUI_DOWNLOAD"
    GUI_REIMPORT = "GUI_REIMPORT"
    GUI_REIMPORT_TARGET = "GUI_REIMPORT_TARGET"
    CJ_UPLOAD = "CJ_UPLOAD"
    CJ_DOWNLOAD = "CJ_DOWNLOAD"
    APC_UPLOAD = "APC_UPLOAD"
    APC_DOWNLOAD = "APC_DOWNLOAD"
    API_UPLOAD = "API_UPLOAD"
    API_DOWNLOAD = "API_DOWNLOAD"
    SUBMITTER_PORTAL_DOWNLOAD = "SUBMITTER_PORTAL_DOWNLOAD"


class AsyncFileOpResponseDto(BaseModel):
    id: Optional[str] = None
    createdBy: Optional[UserReference] = None
    dateCreated: Optional[datetime] = None
    fileName: Optional[str] = None
    action: Optional[Action3] = None


class GetFileRequestParamsDto(BaseModel):
    sourceLang: Optional[str] = None
    targetLang: Optional[str] = None
    callbackUrl: str = Field(
        ..., example='{"callbackUrl": "https://www.yourdomain.com/callback_endpoint"}'
    )


class Response(BaseModel):
    context: Optional[Dict[str, Dict[str, Any]]] = None
    cancelled: Optional[bool] = None
    done: Optional[bool] = None


class WorkflowChangesDto(JobPartReferences):
    pass


class EditLqaConversationDto(BaseModel):
    lqaDescription: Optional[str] = None
    lqa: List[LQAReference]
    status: Optional[Name] = None
    correlation: Optional[ReferenceCorrelation] = None


class PageDtoUserReference(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[UserReference]] = None


class ProviderListDtoV2(BaseModel):
    providers: Optional[Providers] = None


class ProgressDtoV2(ProgressDto):
    pass


class LqaProfilesForWsV2Dto(BaseModel):
    workflowStep: Optional[IdReference] = None
    lqaProfile: Optional[UidReference] = None


class CustomFieldInstanceApiDto(BaseModel):
    customField: Optional[UidReference] = None
    selectedOptions: Optional[List[UidReference]] = None
    value: Optional[constr(min_length=0, max_length=4096)] = None


class EditProjectV2Dto(BaseModel):
    name: constr(min_length=0, max_length=255)
    status: Optional[Status2] = None
    client: Optional[IdReference] = None
    businessUnit: Optional[IdReference] = None
    domain: Optional[IdReference] = None
    subDomain: Optional[IdReference] = None
    owner: Optional[IdReference] = Field(None, description="Owner must be Admin or PM")
    purchaseOrder: Optional[constr(min_length=0, max_length=255)] = None
    dateDue: Optional[datetime] = None
    note: Optional[constr(min_length=0, max_length=4096)] = None
    fileHandover: Optional[bool] = Field(None, description="Default: false")
    propagateTranslationsToLowerWfDuringUpdateSource: Optional[bool] = Field(
        None, description="Default: false"
    )
    lqaProfiles: Optional[List[LqaProfilesForWsV2Dto]] = Field(
        None, description="Lqa profiles that will be added to workflow steps"
    )
    archived: Optional[bool] = Field(None, description="Default: false")
    customFields: Optional[List[CustomFieldInstanceApiDto]] = Field(
        None, description="Custom fields for project"
    )


class CreateProjectFromTemplateV2Dto(BaseModel):
    name: constr(min_length=0, max_length=255)
    sourceLang: Optional[str] = None
    targetLangs: Optional[List[str]] = None
    workflowSteps: Optional[List[IdReference]] = None
    dateDue: Optional[datetime] = None
    note: Optional[str] = None
    client: Optional[IdReference] = None
    businessUnit: Optional[IdReference] = None
    domain: Optional[IdReference] = None
    subDomain: Optional[IdReference] = None
    costCenter: Optional[IdReference] = None


class CreateProjectFromTemplateAsyncV2Dto(BaseModel):
    name: constr(min_length=0, max_length=255)
    sourceLang: Optional[str] = None
    targetLangs: Optional[List[str]] = None
    workflowSteps: Optional[List[IdReference]] = None
    dateDue: Optional[datetime] = None
    note: Optional[str] = None
    client: Optional[IdReference] = None
    businessUnit: Optional[IdReference] = None
    domain: Optional[IdReference] = None
    subDomain: Optional[IdReference] = None
    costCenter: Optional[IdReference] = None
    callbackUrl: Optional[str] = None


class EnabledCheckContextDtoV2(BaseModel):
    moraviaProfileId: Optional[str] = None
    customQaDisplayName: Optional[str] = None
    provider: Optional[str] = None


class EnabledCheckDtoV2(BaseModel):
    checkerType: Optional[str] = None
    context: Optional[EnabledCheckContextDtoV2] = None


class QualityAssuranceChecksDtoV2(BaseModel):
    forbiddenStrings: Optional[List[str]] = None
    enabledChecks: Optional[List[EnabledCheckDtoV2]] = Field(
        None,
        description="enabledChecks",
        example='\n   [\n      {\n         "checkerType":"EmptyTranslation",\n         "ignorable":false\n      },\n      {\n         "checkerType":"TrailingPunctuation",\n         "ignorable":false\n      },\n      {\n         "checkerType":"Formatting",\n         "ignorable":false\n      },\n      {\n         "checkerType":"JoinTags",\n         "ignorable":false\n      },\n      {\n         "checkerType":"MissingNumbers",\n         "ignorable":false\n      },\n      {\n         "checkerType":"MultipleSpaces",\n         "ignorable":false\n      },\n      {\n         "checkerType":"NonConformingTerm",\n         "ignorable":false\n      },\n      {\n         "checkerType":"NotConfirmed",\n         "ignorable":false\n      },\n      {\n         "checkerType":"TranslationLength",\n         "ignorable":false\n      },\n      {\n         "checkerType": "AbsoluteLength",\n         "ignorable": false\n      },\n      {\n         "checkerType": "RelativeLength",\n         "ignorable": false\n      },\n      {\n         "checkerType":"EmptyPairTags",\n         "ignorable":false\n      },\n      {\n         "checkerType":"InconsistentTranslationTargetSource",\n         "ignorable":true\n      },\n      {\n         "checkerType":"InconsistentTranslationSourceTarget",\n         "ignorable":true\n      },\n      {\n         "checkerType":"ForbiddenString",\n         "ignorable":false\n      },\n      {\n         "checkerType":"SpellCheck",\n         "ignorable":false\n      },\n      {\n         "checkerType":"RepeatedWords",\n         "ignorable":false\n      },\n      {\n         "checkerType":"InconsistentTagContent",\n         "ignorable":false\n      },\n      {\n         "checkerType":"EmptyTagContent",\n         "ignorable":false\n      },\n      {\n         "checkerType":"Malformed",\n         "ignorable":false\n      },\n      {\n         "checkerType":"ForbiddenTerm",\n         "ignorable":false\n      },\n      {\n         "checkerType":"NewerAtLowerLevel",\n         "ignorable":false\n      },\n      {\n         "checkerType":"LeadingAndTrailingSpaces",\n         "ignorable":false\n      },\n      {\n         "checkerType":"TargetSourceIdentical",\n         "ignorable":false\n      },\n      {\n         "checkerType":"SourceOrTargetRegexp"\n      },\n      {\n         "checkerType":"UnmodifiedFuzzyTranslationTM",\n         "ignorable":true\n      },\n      {\n         "checkerType":"UnmodifiedFuzzyTranslationMTNT",\n         "ignorable":true\n      },\n      {\n         "checkerType":"Moravia",\n         "ignorable":false,\n         "context": {"moraviaProfileId": "MoraviaProfileIdValue"}\n      },\n      {\n         "checkerType":"ExtraNumbers",\n         "ignorable":true\n      },\n      {\n         "checkerType":"UnresolvedConversation",\n         "ignorable":false\n      },\n      {\n         "checkerType":"NestedTags",\n         "ignorable":false\n      },\n      {\n         "checkerType":"FuzzyInconsistency",\n         "ignorable":true\n      }\n   ]\n',
    )
    excludeLockedSegments: Optional[bool] = None
    userCanSetInstantQA: Optional[bool] = None
    strictJobStatus: Optional[bool] = None
    regexpRules: Optional[List[RegexpCheckRuleDtoV2]] = None


class WebEditorLinkDtoV2(BaseModel):
    url: Optional[str] = None
    warnings: Optional[List[ErrorDetailDtoV2]] = None


class CreateWebEditorLinkDtoV2(BaseModel):
    jobs: List[UidReference] = Field(
        ...,
        description="Maximum supported number of jobs is 260",
        max_items=2147483647,
        min_items=1,
    )


class SubstituteDtoV2(BaseModel):
    source: constr(min_length=1, max_length=1)
    target: constr(min_length=1, max_length=1)


class JobPartReadyDeleteTranslationFilterDto(BaseModel):
    filename: Optional[str] = None
    statuses: Optional[List[str]] = None
    targetLang: Optional[str] = None
    provider: Optional[ProviderReference] = None
    owner: Optional[UidReference] = None
    dateDue: Optional[datetime] = None
    dueInHours: Optional[int] = None
    overdue: Optional[bool] = None


class TranslationSegmentsReferenceV2(BaseModel):
    confirmed: Optional[bool] = Field(
        None,
        description="Remove confirmed (true), unconfirmed (false) or both segments (null). Default: null",
    )
    locked: Optional[bool] = Field(
        None,
        description="Remove locked (true), unlocked (false) or both segments (null). Default: false",
    )


class ReferenceFilesDto(BaseModel):
    referenceFiles: Optional[List[ReferenceFileReference]] = None


class CreateReferenceFilesRequest(BaseModel):
    file: Optional[List[MultipartFile]] = Field(
        None, description="Files with appropriate `Content-Type` header"
    )
    json_: Optional[CreateReferenceFileNoteDto] = Field(
        None,
        alias="json",
        description="Additional data in JSON format (`Content-Type`: `application/json)`",
    )


class TransMemoryDtoV2(TransMemoryDto):
    pass


class TransMemoryReferenceDtoV2(BaseModel):
    internalId: Optional[int] = None
    uid: str
    name: Optional[str] = None
    sourceLang: Optional[str] = None
    targetLangs: Optional[List[str]] = None


class ProjectTemplateTransMemoryV2Dto(BaseModel):
    targetLocale: Optional[str] = None
    workflowStep: Optional[WorkflowStepReferenceV2] = None
    readMode: Optional[bool] = None
    writeMode: Optional[bool] = None
    transMemory: Optional[TransMemoryDtoV2] = None
    penalty: Optional[float] = None
    applyPenaltyTo101Only: Optional[bool] = None
    order: Optional[int] = None


class SetProjectTemplateTransMemoryV2Dto(BaseModel):
    transMemory: UidReference
    readMode: Optional[bool] = Field(None, description="Default: false")
    writeMode: Optional[bool] = Field(
        None,
        description="Can be set only for Translation Memory with read == true.<br/>\n        Max 2 write TMs allowed per project.<br/>\n        Default: false",
    )
    penalty: Optional[confloat(ge=0.0, le=100.0)] = None
    applyPenaltyTo101Only: Optional[bool] = Field(
        None, description="Can be set only for penalty == 1<br/>Default: false"
    )
    order: Optional[int] = None


class AdditionalWorkflowStepV2Dto(AdditionalWorkflowStepDto):
    pass


class QuoteV2Dto(BaseModel):
    id: Optional[int] = None
    uid: Optional[str] = None
    name: Optional[str] = None
    status: Optional[Status7] = None
    currency: Optional[str] = None
    billingUnit: Optional[BillingUnit] = None
    createdBy: Optional[UserReference] = None
    dateCreated: Optional[datetime] = None
    totalPrice: Optional[float] = None
    netRateScheme: Optional[NetRateSchemeReference] = None
    priceList: Optional[PriceListReference] = None
    workflowStepList: Optional[List[WorkflowStepReference]] = None
    provider: Optional[ProviderReference] = None
    customerEmail: Optional[str] = None
    quoteType: Optional[QuoteType] = None
    editable: Optional[bool] = None
    outdated: Optional[bool] = None
    additionalSteps: Optional[List[AdditionalWorkflowStepV2Dto]] = None


class QuoteUnitsDto(BaseModel):
    analyseLanguagePart: IdReference
    value: Optional[confloat(ge=0.0)] = None


class QuoteWorkflowSettingDto(BaseModel):
    workflowStep: IdReference
    units: Optional[List[QuoteUnitsDto]] = Field(None, max_items=100, min_items=0)


class AsyncExportTMDto(BaseModel):
    transMemory: Optional[ObjectReference] = None
    exportTargetLangs: Optional[List[str]] = None


class ExportTMDto(BaseModel):
    exportTargetLangs: Optional[List[str]] = None
    callbackUrl: Optional[str] = None


class Status26(str, Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class WebHookDtoV2(BaseModel):
    name: Optional[str] = None
    id: Optional[str] = None
    uid: Optional[str] = None
    url: str
    events: Optional[List[TriggerEvent]] = None
    secretToken: Optional[constr(min_length=1, max_length=255)] = None
    hidden: Optional[bool] = Field(None, description="Default: false")
    status: Optional[Status26] = None
    failedAttempts: Optional[int] = None
    created: Optional[datetime] = None
    createdBy: Optional[UserReference] = None
    lastModified: Optional[datetime] = None
    lastModifiedBy: Optional[UserReference] = None


class CreateWebHookDto(BaseModel):
    name: Optional[constr(min_length=0, max_length=255)] = None
    url: str
    events: List[TriggerEvent]
    secretToken: Optional[constr(min_length=0, max_length=255)] = None
    hidden: Optional[bool] = Field(None, description="Default: false")
    status: Optional[Status26] = Field(None, description="Default: ENABLED")


class WebhookPreviewDto(BaseModel):
    event: Optional[TriggerEvent] = None
    preview: Optional[str] = None


class WebhookPreviewsDto(BaseModel):
    previews: Optional[List[WebhookPreviewDto]] = None


class ConceptDtov2(BaseModel):
    id: Optional[str] = None
    definition: Optional[str] = None
    domain: Optional[str] = None
    subDomains: Optional[List[str]] = None
    url: Optional[str] = None
    note: Optional[str] = None


class TermBaseReference(BusinessUnitReference):
    pass


class TermV2Dto(BaseModel):
    id: Optional[str] = None
    text: str
    lang: Optional[str] = None
    rtl: Optional[bool] = None
    modifiedAt: Optional[datetime] = None
    createdAt: Optional[datetime] = None
    modifiedBy: Optional[UserReference] = None
    createdBy: Optional[UserReference] = None
    caseSensitive: Optional[bool] = None
    exactMatch: Optional[bool] = None
    forbidden: Optional[bool] = None
    preferred: Optional[bool] = None
    status: Optional[Status17] = None
    conceptId: Optional[str] = None
    usage: Optional[str] = None
    note: Optional[str] = None
    writable: Optional[bool] = None
    shortTranslation: Optional[str] = None
    termType: Optional[str] = None
    partOfSpeech: Optional[str] = None
    gender: Optional[str] = None
    number: Optional[str] = None


class SearchTbInTextByJobRequestDto(BaseModel):
    text: str
    reverse: Optional[bool] = Field(None, description="Default: false")
    zeroLengthSeparator: Optional[str] = None


class SearchTbResponseDto(BaseModel):
    termBase: Optional[TermBaseReference] = None
    concept: Optional[ConceptDtov2] = None
    sourceTerm: Optional[TermV2Dto] = None
    translationTerms: Optional[List[TermV2Dto]] = None


class SearchTbResponseListDto(BaseModel):
    searchResults: Optional[List[SearchTbResponseDto]] = None


class SearchTbByJobRequestDto(BaseModel):
    query: str
    count: Optional[int] = Field(None, description="Default: 15")
    offset: Optional[int] = Field(None, description="Default: 0")
    reverse: Optional[bool] = Field(None, description="Default: false")


class LoginResponseV3Dto(LoginResponseDto):
    pass


class LoginV3Dto(BaseModel):
    userUid: Optional[str] = Field(
        None, description="When not filled, default user of identity will be logged in"
    )
    userName: str
    password: str
    code: Optional[str] = Field(
        None, description="Required only for 2-factor authentication"
    )


class LoginToSessionResponseV3Dto(LoginToSessionResponseDto):
    pass


class LoginToSessionV3Dto(BaseModel):
    userUid: Optional[str] = Field(
        None, description="When not filled, default user of identity will be logged in"
    )
    userName: str
    password: str
    rememberMe: Optional[bool] = None
    twoFactorCode: Optional[int] = None
    captchaCode: Optional[str] = None


class LoginOtherV3Dto(BaseModel):
    userUid: Optional[str] = Field(
        None, description="When not filled, default user of identity will be logged in"
    )
    userName: str


class ErrorDetailDtoV3(ErrorDetailDto):
    pass


class JobPartPatchResultDto(BaseModel):
    updated: Optional[int] = Field(
        None, description="Number of successfully updated job parts"
    )
    errors: Optional[List[ErrorDetailDtoV3]] = Field(
        None, description="Errors and their counts encountered during the update"
    )


class JobPartPatchBatchDto(BaseModel):
    jobs: List[UidReference] = Field(..., max_items=100, min_items=1)
    status: Optional[Status] = None
    dateDue: Optional[datetime] = None
    clearDateDue: Optional[bool] = None
    providers: Optional[List[ProviderReference]] = None


class SearchTMClientDtoV3(SearchTMClientDto):
    pass


class SearchTMDomainDtoV3(SearchTMClientDto):
    pass


class SearchTMProjectDtoV3(SearchTMProjectDto):
    pass


class SearchTMSubDomainDtoV3(SearchTMClientDto):
    pass


class SearchTMTransMemoryDtoV3(SearchTMTransMemoryDto):
    pass


class WildCardSearchByJobRequestDtoV3(BaseModel):
    query: str
    reverse: Optional[bool] = Field(None, description="Default: false")
    count: Optional[conint(ge=1, le=50)] = None
    offset: Optional[int] = None


class SearchTMByJobRequestDtoV3(BaseModel):
    query: str
    reverse: Optional[bool] = Field(None, description="Default: false")
    scoreThreshold: Optional[confloat(ge=0.0, le=1.01)] = Field(
        None, description="Default: 0.0"
    )
    maxResults: Optional[conint(ge=1, le=100)] = Field(None, description="Default: 15")


class AnalyseLanguagePartReference(BaseModel):
    id: Optional[str] = None
    sourceLang: Optional[str] = None
    targetLang: Optional[str] = None
    jobs: Optional[List[AnalyseJobReference]] = None


class AnalyseReference(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    innerId: Optional[str] = None
    type: Optional[AnalysisType] = None
    name: Optional[str] = None
    provider: Optional[ProviderReference] = None
    createdBy: Optional[UserReference] = None
    dateCreated: Optional[datetime] = None
    netRateScheme: Optional[NetRateSchemeReference] = None
    analyseLanguageParts: Optional[List[AnalyseLanguagePartReference]] = None
    outdated: Optional[bool] = None
    importStatus: Optional[ImportStatusDto] = None
    pureWarnings: Optional[List[str]] = None


class PageDtoAnalyseReference(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[AnalyseReference]] = None


class CreateProjectV3Dto(BaseModel):
    name: constr(min_length=0, max_length=255)
    sourceLang: str
    targetLangs: List[str]
    client: Optional[IdReference] = Field(None, description="Client referenced by id")
    businessUnit: Optional[IdReference] = None
    domain: Optional[IdReference] = None
    subDomain: Optional[IdReference] = None
    costCenter: Optional[IdReference] = None
    purchaseOrder: Optional[constr(min_length=0, max_length=255)] = None
    workflowSteps: Optional[List[IdReference]] = None
    dateDue: Optional[datetime] = None
    note: Optional[constr(min_length=0, max_length=4096)] = None
    lqaProfiles: Optional[List[LqaProfilesForWsV2Dto]] = Field(
        None, description="Lqa profiles that will be added to workflow steps"
    )
    customFields: Optional[List[CustomFieldInstanceApiDto]] = Field(
        None, description="Custom fields for project"
    )
    fileHandover: Optional[bool] = Field(None, description="Default: false")
    propagateTranslationsToLowerWfDuringUpdateSource: Optional[bool] = Field(
        None, description="Default: false"
    )


class MisspelledWordDto(MisspelledWord):
    pass


class Position(BaseModel):
    beginIndex: Optional[int] = None
    endIndex: Optional[int] = None


class Term(BaseModel):
    text: Optional[str] = None
    preferred: Optional[bool] = None


class SegmentWarning(BaseModel):
    id: Optional[str] = None
    ignored: Optional[bool] = None
    type: Optional[str] = None
    repetitionGroupId: Optional[str] = None


class QualityAssuranceRunDtoV3(BaseModel):
    initialSegment: Optional[SegmentReference] = None
    maxQaWarningsCount: Optional[conint(ge=1, le=1000)] = Field(
        None,
        description="Maximum number of QA warnings in result, default: 100. For efficiency reasons QA\nwarnings are processed with minimum segments chunk size 10, therefore slightly more warnings are returned.",
    )
    warningTypes: Optional[List[EnabledCheck]] = Field(None, max_items=100, min_items=0)


class JobPartSegmentsDtoV3(BaseModel):
    job: UidReference
    segments: List[str]


class QualityAssuranceSegmentsRunDtoV3(BaseModel):
    jobsAndSegments: List[JobPartSegmentsDtoV3] = Field(..., max_items=100, min_items=1)
    warningTypes: Optional[List[EnabledCheck]] = Field(
        None, description="When empty only fast checks run", max_items=100, min_items=0
    )
    maxQaWarningsCount: Optional[conint(ge=1, le=1000)] = Field(
        None,
        description="Maximum number of QA warnings in result, default: 100. For efficiency reasons QA\nwarnings are processed with minimum segments chunk size 10, therefore slightly more warnings are returned.",
    )


class JobExportResponseDto(BaseModel):
    jobs: Optional[List[UidReference]] = None


class JobExportActionDto(BaseModel):
    jobs: List[UidReference] = Field(..., max_items=1000, min_items=1)


class JobMachineTranslationSettingsV3Dto(BaseModel):
    useMachineTranslation: Optional[bool] = Field(
        None, description="Pre-translate from machine translation. Default: true"
    )
    lock100PercentMatches: Optional[bool] = Field(
        None,
        description="Lock section: 100% machine translation matches. Default: false",
    )
    confirmMatches: Optional[bool] = Field(
        None,
        description="Set segment status to confirmed for:\n                machine translation matches above `confirmMatchesThreshold`. Default: false",
    )
    confirmMatchesThreshold: Optional[confloat(ge=0.0, le=1.0)] = Field(
        None, description="Machine translation matches percent. Default: `1.0`"
    )
    useAltTransOnly: Optional[bool] = Field(
        None,
        description="Do not put machine translations to target and use alt-trans fields (alt-trans in mxlf).\nDefault: false",
    )


class JobNonTranslatableSettingsV3Dto(BaseModel):
    preTranslateNonTranslatables: Optional[bool] = Field(
        None, description="Pre-translate non-translatables. Default: true"
    )
    confirm100PercentMatches: Optional[bool] = Field(
        None,
        description="Set segment status to confirmed for: 100% non-translatable matches. Default: false",
    )
    lock100PercentMatches: Optional[bool] = Field(
        None, description="Lock section: 100% non-translatable matches. Default: false"
    )


class JobTranslationMemorySettingsV3Dto(BaseModel):
    useTranslationMemory: Optional[bool] = Field(
        None, description="Pre-translate from translation memory. Default: true"
    )
    translationMemoryThreshold: Optional[confloat(ge=0.0, le=1.01)] = Field(
        None, description="Pre-translation threshold percent. Default: 0.7"
    )
    confirm100PercentMatches: Optional[bool] = Field(
        None,
        description="Set segment status to confirmed for: 100% translation memory matches. Default: false",
    )
    confirm101PercentMatches: Optional[bool] = Field(
        None,
        description="Set segment status to confirmed for: 101% translation memory matches. Default: false",
    )
    lock100PercentMatches: Optional[bool] = Field(
        None,
        description="Lock section: 100% translation memory matches. Default: false",
    )
    lock101PercentMatches: Optional[bool] = Field(
        None,
        description="Lock section: 101% translation memory matches. Default: false",
    )


class PreTranslateJobSettingsV3Dto(BaseModel):
    autoPropagateRepetitions: Optional[bool] = Field(
        None, description="Propagate repetitions. Default: false"
    )
    confirmRepetitions: Optional[bool] = Field(
        None,
        description="Set segment status to confirmed for: Repetitions. Default: false",
    )
    setJobStatusCompleted: Optional[bool] = Field(
        None,
        description="Pre-translate & set job to completed: Set job to completed once pre-translated. Default: false",
    )
    setJobStatusCompletedWhenConfirmed: Optional[bool] = Field(
        None,
        description="Pre-translate & set job to completed when all segments confirmed:\nSet job to completed once pre-translated and all segments are confirmed. Default: false",
    )
    setProjectStatusCompleted: Optional[bool] = Field(
        None,
        description="Pre-translate & set job to completed: Set project to completed once all jobs pre-translated.\n        Default: false",
    )
    overwriteExistingTranslations: Optional[bool] = Field(
        None,
        description="Overwrite existing translations in target segments. Default: false",
    )
    translationMemorySettings: Optional[JobTranslationMemorySettingsV3Dto] = None
    machineTranslationSettings: Optional[JobMachineTranslationSettingsV3Dto] = None
    nonTranslatableSettings: Optional[JobNonTranslatableSettingsV3Dto] = None


class SegmentFilter(str, Enum):
    LOCKED = "LOCKED"
    NOT_LOCKED = "NOT_LOCKED"


class PreTranslateJobsV3Dto(BaseModel):
    jobs: List[UidReference] = Field(
        ..., description="Jobs to be pre-translated", max_items=100, min_items=1
    )
    segmentFilters: Optional[List[SegmentFilter]] = None
    useProjectPreTranslateSettings: Optional[bool] = Field(
        None,
        description="If pre-translate settings from project should be used.\nIf true, preTranslateSettings values are ignored. Default: `false`",
    )
    callbackUrl: Optional[str] = None
    preTranslateSettings: Optional[PreTranslateJobSettingsV3Dto] = Field(
        None,
        description="Pre-translate settings, used if useProjectPreTranslateSettings is false",
    )


class TransMemoryDtoV3(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    internalId: Optional[int] = None
    name: Optional[str] = None
    sourceLang: Optional[str] = None
    targetLangs: Optional[List[str]] = None
    client: Optional[ClientReference] = None
    businessUnit: Optional[BusinessUnitReference] = None
    domain: Optional[DomainReference] = None
    subDomain: Optional[SubDomainReference] = None
    note: Optional[str] = None
    dateCreated: Optional[datetime] = None
    createdBy: Optional[UserReference] = None


class WorkflowStepReferenceV3(WorkflowStepReference):
    pass


class ProjectTransMemoryDtoV3(BaseModel):
    transMemory: Optional[TransMemoryDtoV3] = None
    penalty: Optional[float] = None
    applyPenaltyTo101Only: Optional[bool] = None
    targetLocale: Optional[str] = None
    workflowStep: Optional[WorkflowStepReferenceV3] = None
    readMode: Optional[bool] = None
    writeMode: Optional[bool] = None
    order: Optional[int] = None


class ProjectTransMemoryListDtoV3(BaseModel):
    transMemories: Optional[List[ProjectTransMemoryDtoV3]] = None


class SetProjectTransMemoryV3Dto(SetProjectTemplateTransMemoryV2Dto):
    pass


class Role4(str, Enum):
    ADMIN = "ADMIN"
    PROJECT_MANAGER = "PROJECT_MANAGER"
    LINGUIST = "LINGUIST"
    GUEST = "GUEST"
    SUBMITTER = "SUBMITTER"


class UserDetailsDtoV3(BaseModel):
    uid: constr(min_length=0, max_length=255)
    userName: constr(min_length=0, max_length=255)
    firstName: constr(min_length=0, max_length=255)
    lastName: constr(min_length=0, max_length=255)
    email: constr(min_length=0, max_length=255)
    dateCreated: Optional[datetime] = None
    dateDeleted: Optional[datetime] = None
    createdBy: Optional[UserReference] = None
    role: Role4
    assignableRoles: Optional[List[str]] = None
    timezone: constr(min_length=0, max_length=255)
    note: Optional[constr(min_length=0, max_length=4096)] = None
    receiveNewsletter: Optional[bool] = None
    active: Optional[bool] = None
    pendingEmailChange: Optional[bool] = Field(
        None, description="If user has email change pending (new email not verified)"
    )


class AbstractUserCreateDto(BaseModel):
    userName: constr(min_length=0, max_length=255)
    firstName: constr(min_length=0, max_length=255)
    lastName: constr(min_length=0, max_length=255)
    email: constr(min_length=0, max_length=255)
    password: constr(min_length=0, max_length=255)
    role: Role = Field(
        ...,
        description='Enum: "ADMIN", "PROJECT_MANAGER", "LINGUIST", "GUEST", "SUBMITTER"',
    )
    timezone: constr(min_length=0, max_length=255)
    receiveNewsletter: Optional[bool] = Field(None, description="Default: true")
    note: Optional[constr(min_length=0, max_length=4096)] = None
    active: Optional[bool] = Field(None, description="Default: true")


class GUEST(AbstractUserCreateDto):
    client: UidReference
    enableMT: Optional[bool] = Field(None, description="Enable MT. Default: true")
    projectViewOther: Optional[bool] = Field(
        None, description="View projects created by other users. Default: true"
    )
    projectViewOtherLinguist: Optional[bool] = Field(
        None, description="Show provider names. Default: true"
    )
    projectViewOtherEditor: Optional[bool] = Field(
        None, description="Edit jobs in Memsource Editor. Default: true"
    )
    transMemoryViewOther: Optional[bool] = Field(
        None, description="View TMs created by other users. Default: true"
    )
    transMemoryEditOther: Optional[bool] = Field(
        None, description="Modify TMs created by other users. Default: true"
    )
    transMemoryExportOther: Optional[bool] = Field(
        None, description="Export TMs created by other users. Default: true"
    )
    transMemoryImportOther: Optional[bool] = Field(
        None, description="Import into TMs created by other users. Default: true"
    )
    termBaseViewOther: Optional[bool] = Field(
        None, description="View TBs created by other users. Default: true"
    )
    termBaseEditOther: Optional[bool] = Field(
        None, description="Modify TBs created by other users. Default: true"
    )
    termBaseExportOther: Optional[bool] = Field(
        None, description="Export TBs created by other users. Default: true"
    )
    termBaseImportOther: Optional[bool] = Field(
        None, description="Import into TBs created by other users. Default: true"
    )
    termBaseApproveOther: Optional[bool] = Field(
        None, description="Approve terms in TBs created by other users. Default: true"
    )


class LINGUIST(AbstractUserCreateDto):
    editAllTermsInTB: Optional[bool] = Field(
        None, description="Edit all terms in TB. Default: false"
    )
    editTranslationsInTM: Optional[bool] = Field(
        None, description="Edit translations in TM. Default: false"
    )
    enableMT: Optional[bool] = Field(None, description="Enable MT. Default: true")
    mayRejectJobs: Optional[bool] = Field(
        None, description="Reject jobs. Default: false"
    )
    sourceLocales: Optional[List[str]] = None
    targetLocales: Optional[List[str]] = None
    workflowSteps: Optional[List[UidReference]] = None
    clients: Optional[List[UidReference]] = None
    domains: Optional[List[UidReference]] = None
    subDomains: Optional[List[UidReference]] = None
    netRateScheme: Optional[UidReference] = Field(None, description="Net rate scheme")
    translationPriceList: Optional[UidReference] = Field(None, description="Price list")


class DashboardSetting(str, Enum):
    ALL_DATA = "ALL_DATA"
    OWN_DATA = "OWN_DATA"
    NO_DASHBOARD = "NO_DASHBOARD"


class PROJECTMANAGER(AbstractUserCreateDto):
    sourceLocales: Optional[List[str]] = None
    targetLocales: Optional[List[str]] = None
    workflowSteps: Optional[List[UidReference]] = None
    clients: Optional[List[UidReference]] = None
    domains: Optional[List[UidReference]] = None
    subDomains: Optional[List[UidReference]] = None
    projectCreate: Optional[bool] = Field(
        None, description="Enable project creation. Default: true"
    )
    projectViewOther: Optional[bool] = Field(
        None, description="View projects created by other users. Default: true"
    )
    projectEditOther: Optional[bool] = Field(
        None, description="Modify projects created by other users. Default: true"
    )
    projectDeleteOther: Optional[bool] = Field(
        None, description="Delete projects created by other users. Default: true"
    )
    projectClients: Optional[List[UidReference]] = Field(
        None, description="Access projects of a selected clients only"
    )
    projectBusinessUnits: Optional[List[UidReference]] = Field(
        None, description="Access projects of selected business units only"
    )
    projectTemplateCreate: Optional[bool] = Field(
        None, description="Enable project templates creation. Default: true"
    )
    projectTemplateViewOther: Optional[bool] = Field(
        None, description="View project templates created by other users. Default: true"
    )
    projectTemplateEditOther: Optional[bool] = Field(
        None,
        description="Modify project templates created by other users. Default: true",
    )
    projectTemplateDeleteOther: Optional[bool] = Field(
        None,
        description="Delete project templates created by other users. Default: true",
    )
    projectTemplateClients: Optional[List[UidReference]] = Field(
        None, description="Access project templates of a selected clients only"
    )
    projectTemplateBusinessUnits: Optional[List[UidReference]] = Field(
        None, description="Access project templates of selected business units only"
    )
    transMemoryCreate: Optional[bool] = Field(
        None, description="Enable TMs creation. Default: true"
    )
    transMemoryViewOther: Optional[bool] = Field(
        None, description="View TMs created by other users. Default: true"
    )
    transMemoryEditOther: Optional[bool] = Field(
        None, description="Modify TMs created by other users. Default: true"
    )
    transMemoryDeleteOther: Optional[bool] = Field(
        None, description="Delete TMs created by other users. Default: true"
    )
    transMemoryExportOther: Optional[bool] = Field(
        None, description="Export TMs created by other users. Default: true"
    )
    transMemoryImportOther: Optional[bool] = Field(
        None, description="Import into TMs created by other users. Default: true"
    )
    transMemoryClients: Optional[List[UidReference]] = Field(
        None, description="Access TMs of a selected clients only"
    )
    transMemoryBusinessUnits: Optional[List[UidReference]] = Field(
        None, description="Access TMs of selected business units only"
    )
    termBaseCreate: Optional[bool] = Field(
        None, description="Enable TBs creation. Default: true"
    )
    termBaseViewOther: Optional[bool] = Field(
        None, description="View TBs created by other users. Default: true"
    )
    termBaseEditOther: Optional[bool] = Field(
        None, description="Modify TBs created by other users. Default: true"
    )
    termBaseDeleteOther: Optional[bool] = Field(
        None, description="Delete TBs created by other users. Default: true"
    )
    termBaseExportOther: Optional[bool] = Field(
        None, description="Export TBs created by other users. Default: true"
    )
    termBaseImportOther: Optional[bool] = Field(
        None, description="Import into TBs created by other users. Default: true"
    )
    termBaseApproveOther: Optional[bool] = Field(
        None, description="Approve terms in TBs created by other users. Default: true"
    )
    termBaseClients: Optional[List[UidReference]] = Field(
        None, description="Access TBs of a selected clients only"
    )
    termBaseBusinessUnits: Optional[List[UidReference]] = Field(
        None, description="Access TBs of selected business units only"
    )
    userCreate: Optional[bool] = Field(
        None, description="Enable users creation. Default: true"
    )
    userViewOther: Optional[bool] = Field(
        None, description="View users created by other users. Default: true"
    )
    userEditOther: Optional[bool] = Field(
        None, description="Modify users created by other users. Default: true"
    )
    userDeleteOther: Optional[bool] = Field(
        None, description="Delete users created by other users. Default: true"
    )
    clientDomainSubDomainCreate: Optional[bool] = Field(
        None, description="Enable clients, domains, subdomains creation. Default: true"
    )
    clientDomainSubDomainViewOther: Optional[bool] = Field(
        None,
        description="View clients, domains, subdomains created by other users. Default: true",
    )
    clientDomainSubDomainEditOther: Optional[bool] = Field(
        None,
        description="Modify clients, domains, subdomains created by other users. Default: true",
    )
    clientDomainSubDomainDeleteOther: Optional[bool] = Field(
        None,
        description="Delete clients, domains, subdomains created by other users. Default: true",
    )
    vendorCreate: Optional[bool] = Field(
        None, description="Enable Vendors creation. Default: true"
    )
    vendorViewOther: Optional[bool] = Field(
        None, description="View Vendors created by other users. Default: true"
    )
    vendorEditOther: Optional[bool] = Field(
        None, description="Modify Vendors created by other users. Default: true"
    )
    vendorDeleteOther: Optional[bool] = Field(
        None, description="Delete Vendors created by other users. Default: true"
    )
    dashboardSetting: Optional[DashboardSetting] = Field(
        None, description="Home page dashboards. Default: OWN_DATA"
    )
    setupServer: Optional[bool] = Field(
        None, description="Modify setup's server settings. Default: true"
    )


class SUBMITTER(AbstractUserCreateDto):
    automationWidgets: Optional[List[IdReference]] = Field(
        None,
        description="If no automation widgets are assigned in request the default automation widgets will be assigned instead",
    )
    projectViewCreatedByOtherSubmitters: Optional[bool] = Field(
        None, description="View projects created by other Submitters. Default: false"
    )


class AbstractUserEditDto(BaseModel):
    userName: constr(min_length=0, max_length=255)
    firstName: constr(min_length=0, max_length=255)
    lastName: constr(min_length=0, max_length=255)
    email: constr(min_length=0, max_length=255)
    role: Role = Field(
        ...,
        description='Enum: "ADMIN", "PROJECT_MANAGER", "LINGUIST", "GUEST", "SUBMITTER"',
    )
    timezone: constr(min_length=0, max_length=255)
    receiveNewsletter: Optional[bool] = Field(None, description="Default: true")
    note: Optional[constr(min_length=0, max_length=4096)] = None
    active: Optional[bool] = Field(None, description="Default: true")


class GUESTEDIT(AbstractUserEditDto):
    client: UidReference
    enableMT: Optional[bool] = Field(None, description="Enable MT. Default: true")
    projectViewOther: Optional[bool] = Field(
        None, description="View projects created by other users. Default: true"
    )
    projectViewOtherLinguist: Optional[bool] = Field(
        None, description="Show provider names. Default: true"
    )
    projectViewOtherEditor: Optional[bool] = Field(
        None, description="Edit jobs in Memsource Editor. Default: true"
    )
    transMemoryViewOther: Optional[bool] = Field(
        None, description="View TMs created by other users. Default: true"
    )
    transMemoryEditOther: Optional[bool] = Field(
        None, description="Modify TMs created by other users. Default: true"
    )
    transMemoryExportOther: Optional[bool] = Field(
        None, description="Export TMs created by other users. Default: true"
    )
    transMemoryImportOther: Optional[bool] = Field(
        None, description="Import into TMs created by other users. Default: true"
    )
    termBaseViewOther: Optional[bool] = Field(
        None, description="View TBs created by other users. Default: true"
    )
    termBaseEditOther: Optional[bool] = Field(
        None, description="Modify TBs created by other users. Default: true"
    )
    termBaseExportOther: Optional[bool] = Field(
        None, description="Export TBs created by other users. Default: true"
    )
    termBaseImportOther: Optional[bool] = Field(
        None, description="Import into TBs created by other users. Default: true"
    )
    termBaseApproveOther: Optional[bool] = Field(
        None, description="Approve terms in TBs created by other users. Default: true"
    )


class LINGUISTEDIT(AbstractUserEditDto):
    editAllTermsInTB: Optional[bool] = Field(
        None, description="Edit all terms in TB. Default: false"
    )
    editTranslationsInTM: Optional[bool] = Field(
        None, description="Edit translations in TM. Default: false"
    )
    enableMT: Optional[bool] = Field(None, description="Enable MT. Default: true")
    mayRejectJobs: Optional[bool] = Field(
        None, description="Reject jobs. Default: false"
    )
    sourceLocales: Optional[List[str]] = None
    targetLocales: Optional[List[str]] = None
    workflowSteps: Optional[List[UidReference]] = None
    clients: Optional[List[UidReference]] = None
    domains: Optional[List[UidReference]] = None
    subDomains: Optional[List[UidReference]] = None
    netRateScheme: Optional[UidReference] = Field(None, description="Net rate scheme")
    translationPriceList: Optional[UidReference] = Field(None, description="Price list")


class PROJECTMANAGEREDIT(AbstractUserEditDto):
    sourceLocales: Optional[List[str]] = None
    targetLocales: Optional[List[str]] = None
    workflowSteps: Optional[List[UidReference]] = None
    clients: Optional[List[UidReference]] = None
    domains: Optional[List[UidReference]] = None
    subDomains: Optional[List[UidReference]] = None
    projectCreate: Optional[bool] = Field(
        None, description="Enable project creation. Default: true"
    )
    projectViewOther: Optional[bool] = Field(
        None, description="View projects created by other users. Default: true"
    )
    projectEditOther: Optional[bool] = Field(
        None, description="Modify projects created by other users. Default: true"
    )
    projectDeleteOther: Optional[bool] = Field(
        None, description="Delete projects created by other users. Default: true"
    )
    projectClients: Optional[List[UidReference]] = Field(
        None, description="Access projects of a selected clients only"
    )
    projectBusinessUnits: Optional[List[UidReference]] = Field(
        None, description="Access projects of selected business units only"
    )
    projectTemplateCreate: Optional[bool] = Field(
        None, description="Enable project templates creation. Default: true"
    )
    projectTemplateViewOther: Optional[bool] = Field(
        None, description="View project templates created by other users. Default: true"
    )
    projectTemplateEditOther: Optional[bool] = Field(
        None,
        description="Modify project templates created by other users. Default: true",
    )
    projectTemplateDeleteOther: Optional[bool] = Field(
        None,
        description="Delete project templates created by other users. Default: true",
    )
    projectTemplateClients: Optional[List[UidReference]] = Field(
        None, description="Access project templates of a selected clients only"
    )
    projectTemplateBusinessUnits: Optional[List[UidReference]] = Field(
        None, description="Access project templates of selected business units only"
    )
    transMemoryCreate: Optional[bool] = Field(
        None, description="Enable TMs creation. Default: true"
    )
    transMemoryViewOther: Optional[bool] = Field(
        None, description="View TMs created by other users. Default: true"
    )
    transMemoryEditOther: Optional[bool] = Field(
        None, description="Modify TMs created by other users. Default: true"
    )
    transMemoryDeleteOther: Optional[bool] = Field(
        None, description="Delete TMs created by other users. Default: true"
    )
    transMemoryExportOther: Optional[bool] = Field(
        None, description="Export TMs created by other users. Default: true"
    )
    transMemoryImportOther: Optional[bool] = Field(
        None, description="Import into TMs created by other users. Default: true"
    )
    transMemoryClients: Optional[List[UidReference]] = Field(
        None, description="Access TMs of a selected clients only"
    )
    transMemoryBusinessUnits: Optional[List[UidReference]] = Field(
        None, description="Access TMs of selected business units only"
    )
    termBaseCreate: Optional[bool] = Field(
        None, description="Enable TBs creation. Default: true"
    )
    termBaseViewOther: Optional[bool] = Field(
        None, description="View TBs created by other users. Default: true"
    )
    termBaseEditOther: Optional[bool] = Field(
        None, description="Modify TBs created by other users. Default: true"
    )
    termBaseDeleteOther: Optional[bool] = Field(
        None, description="Delete TBs created by other users. Default: true"
    )
    termBaseExportOther: Optional[bool] = Field(
        None, description="Export TBs created by other users. Default: true"
    )
    termBaseImportOther: Optional[bool] = Field(
        None, description="Import into TBs created by other users. Default: true"
    )
    termBaseApproveOther: Optional[bool] = Field(
        None, description="Approve terms in TBs created by other users. Default: true"
    )
    termBaseClients: Optional[List[UidReference]] = Field(
        None, description="Access TBs of a selected clients only"
    )
    termBaseBusinessUnits: Optional[List[UidReference]] = Field(
        None, description="Access TBs of selected business units only"
    )
    userCreate: Optional[bool] = Field(
        None, description="Enable users creation. Default: true"
    )
    userViewOther: Optional[bool] = Field(
        None, description="View users created by other users. Default: true"
    )
    userEditOther: Optional[bool] = Field(
        None, description="Modify users created by other users. Default: true"
    )
    userDeleteOther: Optional[bool] = Field(
        None, description="Delete users created by other users. Default: true"
    )
    clientDomainSubDomainCreate: Optional[bool] = Field(
        None, description="Enable clients, domains, subdomains creation. Default: true"
    )
    clientDomainSubDomainViewOther: Optional[bool] = Field(
        None,
        description="View clients, domains, subdomains created by other users. Default: true",
    )
    clientDomainSubDomainEditOther: Optional[bool] = Field(
        None,
        description="Modify clients, domains, subdomains created by other users. Default: true",
    )
    clientDomainSubDomainDeleteOther: Optional[bool] = Field(
        None,
        description="Delete clients, domains, subdomains created by other users. Default: true",
    )
    vendorCreate: Optional[bool] = Field(
        None, description="Enable Vendors creation. Default: true"
    )
    vendorViewOther: Optional[bool] = Field(
        None, description="View Vendors created by other users. Default: true"
    )
    vendorEditOther: Optional[bool] = Field(
        None, description="Modify Vendors created by other users. Default: true"
    )
    vendorDeleteOther: Optional[bool] = Field(
        None, description="Delete Vendors created by other users. Default: true"
    )
    dashboardSetting: Optional[DashboardSetting] = Field(
        None, description="Home page dashboards. Default: OWN_DATA"
    )
    setupServer: Optional[bool] = Field(
        None, description="Modify setup's server settings. Default: true"
    )


class SUBMITTEREDIT(AbstractUserEditDto):
    automationWidgets: List[IdReference]
    projectViewCreatedByOtherSubmitters: Optional[bool] = Field(
        None, description="View projects created by other Submitters. Default: false"
    )


class PreTranslateSettingsV4Dto(BaseModel):
    preTranslateOnJobCreation: Optional[bool] = Field(
        None,
        description="Pre-translate & set job to completed: Pre-translate on job creation. Default: false",
    )
    setJobStatusCompleted: Optional[bool] = Field(
        None,
        description="Pre-translate & set job to completed: Set job to completed once pre-translated. Default: false",
    )
    setJobStatusCompletedWhenConfirmed: Optional[bool] = Field(
        None,
        description="Pre-translate & set job to completed when all segments confirmed:\nSet job to completed once pre-translated and all segments are confirmed. Default: false",
    )
    setProjectStatusCompleted: Optional[bool] = Field(
        None,
        description="Pre-translate & set job to completed: Set project to completed once all jobs pre-translated.\n        Default: false",
    )
    overwriteExistingTranslations: Optional[bool] = Field(
        None,
        description="Overwrite existing translations in target segments. Default: false",
    )
    translationMemorySettings: Optional[TranslationMemorySettingsDto] = None
    machineTranslationSettings: Optional[MachineTranslationSettingsDto] = None
    nonTranslatableSettings: Optional[NonTranslatableSettingsDto] = None
    repetitionsSettings: Optional[RepetitionsSettingsDto] = None


class DataDtoV1(BaseModel):
    available: Optional[bool] = None
    all: Optional[CountsDto] = None
    repetitions: Optional[CountsDto] = None
    transMemoryMatches: Optional[MatchCounts101Dto] = None
    machineTranslationMatches: Optional[MatchCountsDto] = None
    nonTranslatablesMatches: Optional[MatchCountsNTDtoV1] = None
    internalFuzzyMatches: Optional[MatchCountsDto] = None


class AsyncResponseDto(BaseModel):
    dateCreated: Optional[datetime] = None
    errorCode: Optional[str] = None
    errorDesc: Optional[str] = None
    errorDetails: Optional[List[ErrorDetailDto]] = None
    warnings: Optional[List[ErrorDetailDto]] = None
    acceptedSegmentsCount: Optional[int] = None


class AnalyseJobDto(BaseModel):
    uid: Optional[str] = None
    filename: Optional[str] = None
    data: Optional[DataDtoV1] = None
    discountedData: Optional[DataDtoV1] = None


class PageDtoAnalyseJobDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[AnalyseJobDto]] = None


class AsyncRequestStatusDto(BaseModel):
    concurrentRequests: Optional[ConcurrentRequestsDto] = Field(
        None, description="Current count of running requests and the allowed limit"
    )


class LoginUserDto(BaseModel):
    user: Optional[UserReference] = None
    csrfToken: Optional[str] = None
    organization: Optional[OrganizationReference] = None
    edition: Optional[EditionDto] = None
    features: Optional[FeaturesDto] = None


class JobPartReference(BaseModel):
    uid: Optional[str] = None
    status: Optional[Status] = None
    providers: Optional[List[ProviderReference]] = None
    targetLang: Optional[str] = None
    workflowLevel: Optional[int] = None
    workflowStep: Optional[WorkflowStepReference] = None
    filename: Optional[str] = None
    dateDue: Optional[datetime] = None
    dateCreated: Optional[datetime] = None
    updateSourceDate: Optional[datetime] = None
    imported: Optional[bool] = None
    jobAssignedEmailTemplate: Optional[ObjectReference] = None
    notificationIntervalInMinutes: Optional[int] = None
    continuous: Optional[bool] = None
    sourceFileUid: Optional[str] = None


class ProjectJobPartsDto(BaseModel):
    jobs: Optional[List[JobPartReference]] = None
    project: Optional[ProjectReference] = None


class ClientDto(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    name: Optional[str] = None
    externalId: Optional[str] = None
    note: Optional[str] = None
    displayNoteInProject: Optional[bool] = Field(None, description="Default: false")
    priceList: Optional[PriceListReference] = None
    netRateScheme: Optional[NetRateSchemeReference] = None
    createdBy: Optional[UserReference] = None


class PageDtoClientDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[ClientDto]] = None


class AutomatedProjectSettingsDto(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    organization: Optional[NameDto] = None
    active: Optional[bool] = None
    sourceLang: Optional[str] = None
    targetLangs: Optional[List[str]] = Field(None, unique_items=True)
    connector: Optional[NameDto] = None
    remoteFolder: Optional[str] = None


class ConnectorDto(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[IntegrationType] = None
    organization: Optional[NameDto] = None
    createdBy: Optional[NameDto] = None
    createdAt: Optional[datetime] = None
    localToken: Optional[str] = None
    automatedProjectSettings: Optional[List[AutomatedProjectSettingsDto]] = None


class ConnectorListDto(BaseModel):
    connectors: Optional[List[ConnectorDto]] = None
    totalCount: Optional[int] = None


class LQAReferences(BaseModel):
    taskId: Optional[str] = None
    jobPartUid: Optional[str] = None
    transGroupId: conint(ge=0)
    segmentId: str
    conversationTitle: Optional[str] = None
    conversationTitleOffset: Optional[conint(ge=0)] = None
    commentedText: Optional[str] = None
    correlation: Optional[ReferenceCorrelation] = None
    lqa: List[LQAReference] = Field(..., max_items=2147483647, min_items=1)


class PlainReferences(BaseModel):
    taskId: Optional[str] = None
    jobPartUid: Optional[str] = None
    transGroupId: conint(ge=0)
    segmentId: str
    conversationTitle: Optional[str] = None
    conversationTitleOffset: Optional[conint(ge=0)] = None
    commentedText: Optional[str] = None
    correlation: Optional[ReferenceCorrelation] = None


class ProjectWorkflowStepDtoV2(BaseModel):
    id: Optional[int] = None
    abbreviation: Optional[str] = None
    name: Optional[str] = None
    workflowLevel: Optional[int] = None
    workflowStep: Optional[WorkflowStepReferenceV2] = None


class CustomFieldDto(BaseModel):
    uid: Optional[str] = None
    name: Optional[str] = None
    type: Optional[FieldType] = None
    allowedEntities: Optional[List[AllowedEntity]] = None
    options: Optional[CustomFieldOptionsTruncatedDto] = None
    createdAt: Optional[datetime] = None
    createdBy: Optional[UserReference] = None
    lastModified: Optional[datetime] = None
    lastModifiedBy: Optional[UserReference] = None
    requiredFrom: Optional[datetime] = None
    required: Optional[bool] = None
    description: Optional[str] = None


class PageDtoCustomFieldDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[CustomFieldDto]] = None


class FileImportSettingsDto(BaseModel):
    inputCharset: Optional[str] = None
    outputCharset: Optional[str] = None
    zipCharset: Optional[str] = None
    fileFormat: Optional[str] = None
    autodetectMultilingualFiles: Optional[bool] = None
    targetLength: Optional[bool] = None
    targetLengthMax: Optional[int] = None
    targetLengthPercent: Optional[bool] = None
    targetLengthPercentValue: Optional[float] = None
    android: Optional[AndroidSettingsDto] = None
    idml: Optional[IdmlSettingsDto] = None
    xls: Optional[XlsSettingsDto] = None
    multilingualXml: Optional[MultilingualXmlSettingsDto] = None
    php: Optional[PhpSettingsDto] = None
    resx: Optional[ResxSettingsDto] = None
    json_: Optional[JsonSettingsDto] = Field(None, alias="json")
    html: Optional[HtmlSettingsDto] = None
    multilingualXls: Optional[MultilingualXlsSettingsDto] = None
    multilingualCsv: Optional[MultilingualCsvSettingsDto] = None
    csv: Optional[CsvSettingsDto] = None
    txt: Optional[TxtSettingsDto] = None
    xlf2: Optional[Xlf2SettingsDto] = None
    quarkTag: Optional[QuarkTagSettingsDto] = None
    pdf: Optional[PdfSettingsDto] = None
    tmMatch: Optional[TMMatchSettingsDto] = None
    xml: Optional[XmlSettingsDto] = None
    mif: Optional[MifSettingsDto] = None
    properties: Optional[PropertiesSettingsDto] = None
    doc: Optional[DocSettingsDto] = None
    xlf: Optional[XlfSettingsDto] = None
    sdlXlf: Optional[SdlXlfSettingsDto] = None
    ttx: Optional[TtxSettingsDto] = None
    ppt: Optional[PptSettingsDto] = None
    yaml: Optional[YamlSettingsDto] = None
    dita: Optional[DitaSettingsDto] = None
    docBook: Optional[DocBookSettingsDto] = None
    po: Optional[PoSettingsDto] = None
    mac: Optional[MacSettingsDto] = None
    md: Optional[MdSettingsDto] = None
    psd: Optional[PsdSettingsDto] = None
    asciidoc: Optional[AsciidocSettingsDto] = None
    segRule: Optional[SegRuleReference] = None
    targetSegRule: Optional[SegRuleReference] = None


class CreateCustomFileTypeDto(BaseModel):
    name: str
    filenamePattern: str
    type: CustomFiletypeType
    fileImportSettings: Optional[FileImportSettingsCreateDto] = None


class NetRateScheme(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    name: Optional[str] = None
    organization: Optional[OrganizationReference] = None
    dateCreated: Optional[datetime] = None
    createdBy: Optional[UserReference] = None
    workflowStepNetSchemes: Optional[List[NetRateSchemeWorkflowStepReference]] = None
    rates: Optional[DiscountSettingsDto] = None


class DiscountSchemeCreateDto(BaseModel):
    name: constr(min_length=1, max_length=255)
    rates: Optional[DiscountSettingsDto] = None
    workflowStepNetSchemes: Optional[List[NetRateSchemeWorkflowStepCreate]] = None


class GlossaryDto(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    internalId: Optional[int] = None
    name: str
    langs: Optional[List[str]] = None
    createdBy: Optional[UserReference] = None
    owner: Optional[UserReference] = None
    dateCreated: Optional[datetime] = None
    profileCount: Optional[int] = None
    active: Optional[bool] = None
    profiles: Optional[List[MemsourceTranslateProfileSimpleDto]] = None


class PageDtoGlossaryDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[GlossaryDto]] = None


class SearchTMSegmentDto(BaseModel):
    id: Optional[str] = None
    text: Optional[str] = None
    lang: Optional[str] = None
    rtl: Optional[bool] = None
    modifiedAt: Optional[int] = None
    createdAt: Optional[int] = None
    modifiedBy: Optional[UserReference] = None
    createdBy: Optional[UserReference] = None
    filename: Optional[str] = None
    project: Optional[SearchTMProjectDto] = None
    client: Optional[SearchTMClientDto] = None
    domain: Optional[SearchTMDomainDto] = None
    subDomain: Optional[SearchTMSubDomainDto] = None
    tagMetadata: Optional[List[TagMetadata]] = None
    previousSegment: Optional[str] = None
    nextSegment: Optional[str] = None
    key: Optional[str] = None


class SearchTMByJobRequestDto(BaseModel):
    segment: str
    workflowLevel: Optional[conint(ge=1, le=15)] = None
    scoreThreshold: Optional[confloat(ge=0.0, le=1.01)] = None
    previousSegment: Optional[str] = None
    nextSegment: Optional[str] = None
    contextKey: Optional[str] = None
    maxSegments: Optional[conint(ge=0, le=5)] = Field(None, description="Default: 5")
    maxSubSegments: Optional[conint(ge=0, le=5)] = Field(None, description="Default: 5")
    tagMetadata: Optional[List[TagMetadataDto]] = None


class AccuracyWeightsDto(BaseModel):
    accuracy: Optional[ToggleableWeightDto] = None
    addition: Optional[ToggleableWeightDto] = None
    omission: Optional[ToggleableWeightDto] = None
    mistranslation: Optional[ToggleableWeightDto] = None
    underTranslation: Optional[ToggleableWeightDto] = None
    untranslated: Optional[ToggleableWeightDto] = None
    improperTmMatch: Optional[ToggleableWeightDto] = None
    overTranslation: Optional[ToggleableWeightDto] = None


class DesignWeightsDto(BaseModel):
    design: Optional[ToggleableWeightDto] = None
    length: Optional[ToggleableWeightDto] = None
    localFormatting: Optional[ToggleableWeightDto] = None
    markup: Optional[ToggleableWeightDto] = None
    missingText: Optional[ToggleableWeightDto] = None
    truncation: Optional[ToggleableWeightDto] = None


class FluencyWeightsDto(BaseModel):
    fluency: Optional[ToggleableWeightDto] = None
    punctuation: Optional[ToggleableWeightDto] = None
    spelling: Optional[ToggleableWeightDto] = None
    grammar: Optional[ToggleableWeightDto] = None
    grammaticalRegister: Optional[ToggleableWeightDto] = None
    inconsistency: Optional[ToggleableWeightDto] = None
    crossReference: Optional[ToggleableWeightDto] = None
    characterEncoding: Optional[ToggleableWeightDto] = None


class LocaleConventionWeightsDto(BaseModel):
    localeConvention: Optional[ToggleableWeightDto] = None
    addressFormat: Optional[ToggleableWeightDto] = None
    dateFormat: Optional[ToggleableWeightDto] = None
    currencyFormat: Optional[ToggleableWeightDto] = None
    measurementFormat: Optional[ToggleableWeightDto] = None
    shortcutKey: Optional[ToggleableWeightDto] = None
    telephoneFormat: Optional[ToggleableWeightDto] = None


class OtherWeightsDto(BaseModel):
    other: Optional[ToggleableWeightDto] = None


class PenaltyPointsDto(BaseModel):
    neutral: Optional[SeverityDto] = None
    minor: Optional[SeverityDto] = None
    major: Optional[SeverityDto] = None
    critical: Optional[SeverityDto] = None


class StyleWeightsDto(BaseModel):
    style: Optional[ToggleableWeightDto] = None
    awkward: Optional[ToggleableWeightDto] = None
    companyStyle: Optional[ToggleableWeightDto] = None
    inconsistentStyle: Optional[ToggleableWeightDto] = None
    thirdPartyStyle: Optional[ToggleableWeightDto] = None
    unidiomatic: Optional[ToggleableWeightDto] = None


class TerminologyWeightsDto(BaseModel):
    terminology: Optional[ToggleableWeightDto] = None
    inconsistentWithTb: Optional[ToggleableWeightDto] = None
    inconsistentUseOfTerminology: Optional[ToggleableWeightDto] = None


class ImportSettingsDto(BaseModel):
    uid: Optional[str] = None
    name: Optional[str] = None
    createdBy: Optional[UserReference] = None
    dateCreated: Optional[datetime | str] = None
    fileImportSettings: Optional[FileImportSettingsDto] = None


class MORAVIA(QACheckDtoV2):
    enabled: Optional[bool] = None
    profile: Optional[str] = None
    ignorable: Optional[bool] = None
    instant: Optional[bool] = None


class NUMBER(QACheckDtoV2):
    ignorable: Optional[bool] = None
    enabled: Optional[bool] = None
    value: Optional[Number] = None
    instant: Optional[bool] = None


class REGEX(QACheckDtoV2):
    rules: Optional[List[RegexpCheckRuleDtoV2]] = None


class CreatePlainConversationDto(BaseModel):
    comment: Optional[AddCommentDto] = None
    references: PlainReferences


class MTSettingsPerLanguageReference(BaseModel):
    targetLang: Optional[str] = Field(
        None, description="mtSettings is set for whole project if targetLang == null"
    )
    machineTranslateSettings: Optional[MachineTranslateSettingsReference] = None


class PatchProjectDto(BaseModel):
    name: Optional[constr(min_length=0, max_length=255)] = None
    status: Optional[Status2] = None
    client: Optional[IdReference] = None
    businessUnit: Optional[IdReference] = None
    domain: Optional[IdReference] = None
    subDomain: Optional[IdReference] = None
    owner: Optional[IdReference] = None
    purchaseOrder: Optional[constr(min_length=0, max_length=255)] = None
    dateDue: Optional[datetime] = None
    note: Optional[constr(min_length=0, max_length=4096)] = None
    machineTranslateSettings: Optional[UidReference] = None
    machineTranslateSettingsPerLangs: Optional[List[ProjectMTSettingsPerLangDto]] = None
    archived: Optional[bool] = None


class ProjectTemplateDto(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    templateName: Optional[str] = None
    sourceLang: Optional[str] = None
    targetLangs: Optional[List[str]] = Field(None, unique_items=True)
    workflowSettings: Optional[List[ProjectTemplateWorkflowSettingsDto]] = None


class JobPartsDto(BaseModel):
    jobs: Optional[List[JobPartReference]] = None


class LqaSettingsDto(BaseModel):
    enabled: Optional[bool] = None
    severities: Optional[List[LqaSeverityDto]] = None
    categories: Optional[List[LqaErrorCategoryDto]] = None


class PageDtoQuoteDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[QuoteDto]] = None


class CustomFieldInstanceDto(BaseModel):
    uid: Optional[str] = None
    customField: Optional[CustomFieldDto] = None
    selectedOptions: Optional[List[CustomFieldOptionDto]] = None
    value: Optional[str] = None
    createdAt: Optional[datetime] = None
    createdBy: Optional[UidReference] = None
    updatedAt: Optional[datetime] = None
    updatedBy: Optional[UidReference] = None


class CustomFieldInstancesDto(BaseModel):
    customFieldInstances: Optional[List[CustomFieldInstanceDto]] = None


class PageDtoCustomFieldInstanceDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[CustomFieldInstanceDto]] = None


class JobPartExtendedDto(BaseModel):
    uid: Optional[str] = None
    innerId: Optional[str] = Field(
        None,
        description="InnerId is a sequential number of a job in a project. Jobs created from the same file share the same innerId across workflow steps.",
    )
    status: Optional[Status] = None
    providers: Optional[List[ProviderReference]] = None
    sourceLang: Optional[str] = None
    targetLang: Optional[str] = None
    workflowLevel: Optional[int] = None
    workflowStep: Optional[ProjectWorkflowStepReference] = None
    filename: Optional[str] = None
    dateDue: Optional[datetime] = None
    wordsCount: Optional[int] = None
    beginIndex: Optional[int] = None
    endIndex: Optional[int] = None
    isParentJobSplit: Optional[bool] = None
    updateSourceDate: Optional[datetime] = None
    updateTargetDate: Optional[datetime] = None
    dateCreated: Optional[datetime] = None
    jobReference: Optional[JobReference] = None
    project: Optional[ProjectReference] = None
    lastWorkflowLevel: Optional[int] = None
    workUnit: Optional[ObjectReference] = None
    importStatus: Optional[ImportStatusDto] = None
    imported: Optional[bool] = None
    continuous: Optional[bool] = None
    continuousJobInfo: Optional[ContinuousJobInfoDto] = None
    originalFileDirectory: Optional[str] = None


class PseudoTranslateActionDto(BaseModel):
    replacement: Optional[constr(min_length=1, max_length=10)] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    length: Optional[float] = None
    keyHashPrefixLen: Optional[conint(ge=0, le=18)] = None
    substitution: Optional[List[SubstituteDto]] = Field(
        None, max_items=100, min_items=1
    )


class UpdateIgnoredSegment(BaseModel):
    uid: str
    warnings: List[UpdateIgnoredWarning] = Field(..., max_items=100, min_items=1)


class JobSegmentDto(BaseModel):
    id: Optional[str] = None
    source: Optional[str] = None
    translation: Optional[str] = None
    createdAt: Optional[int] = None
    modifiedAt: Optional[int] = None
    createdBy: Optional[UserReference] = None
    modifiedBy: Optional[UserReference] = None
    workflowLevel: Optional[int] = None
    workflowStep: Optional[WorkflowStepDto] = None


class SegmentListDto(BaseModel):
    segments: Optional[List[JobSegmentDto]] = None


class JobListDto(BaseModel):
    unsupportedFiles: Optional[List[str]] = None
    jobs: Optional[List[JobPartReference]] = None
    asyncRequest: Optional[AsyncRequestReference] = None


class ProvidersPerLanguage(BaseModel):
    targetLang: Optional[str] = None
    providers: Optional[List[ProviderReference]] = None
    assignedUsers: Optional[List[User]] = None


class WorkflowStepConfiguration(BaseModel):
    id: Optional[str] = None
    assignments: List[ProvidersPerLanguage]
    due: Optional[datetime] = Field(None, description="Use ISO 8601 date format.")
    notifyProvider: Optional[NotifyProviderDto] = None


class SearchJobsDto(BaseModel):
    jobs: Optional[List[JobPartExtendedDto]] = None


class PreviousWorkflowDto(BaseModel):
    completed: Optional[bool] = None
    counts: Optional[SegmentsCountsDto] = None


class SegmentsCountsResponseDto(BaseModel):
    jobPartUid: Optional[str] = None
    counts: Optional[SegmentsCountsDto] = None
    previousWorkflow: Optional[PreviousWorkflowDto] = None


class SegmentsCountsResponseListDto(BaseModel):
    segmentsCountsResults: Optional[List[SegmentsCountsResponseDto]] = None


class JobPartReferenceV2(BaseModel):
    uid: Optional[str] = None
    innerId: Optional[str] = Field(
        None,
        description="InnerId is a sequential number of a job in a project.\n            Jobs created from the same file share the same innerId across workflow steps",
    )
    status: Optional[Status] = None
    providers: Optional[List[ProviderReference]] = None
    targetLang: Optional[str] = None
    workflowStep: Optional[ProjectWorkflowStepReference] = None
    filename: Optional[str] = None
    originalFileDirectory: Optional[str] = None
    dateDue: Optional[datetime] = None
    dateCreated: Optional[datetime] = None
    importStatus: Optional[ImportStatusDtoV2] = None
    continuous: Optional[bool] = None
    sourceFileUid: Optional[str] = None
    split: Optional[bool] = None
    serverTaskId: Optional[str] = None
    owner: Optional[UserReference] = None
    remoteFile: Optional[JobRemoteFileReference] = None
    imported: Optional[bool] = Field(None, description="Default: false")


class PageDtoJobPartReferenceV2(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[JobPartReferenceV2]] = None


class SearchResponseTbDto(BaseModel):
    termBase: Optional[TermBaseDto] = None
    conceptId: Optional[str] = None
    sourceTerm: Optional[TermDto] = None
    translationTerms: Optional[List[TermDto]] = None


class CreateTermsDto(BaseModel):
    sourceTerm: TermCreateByJobDto
    targetTerm: TermCreateByJobDto


class PageDtoTransMemoryDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[TransMemoryDto]] = None


class ProjectTemplate(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    templateName: Optional[str] = None
    name: Optional[str] = None
    sourceLang: Optional[str] = None
    targetLangs: Optional[List[str]] = None
    note: Optional[str] = None
    useDynamicTitle: Optional[bool] = None
    dynamicTitle: Optional[str] = None
    owner: Optional[UserReference] = None
    client: Optional[ClientReference] = None
    domain: Optional[DomainReference] = None
    subDomain: Optional[SubDomainReference] = None
    vendor: Optional[VendorReference] = None
    createdBy: Optional[UserReference] = None
    dateCreated: Optional[datetime] = None
    modifiedBy: Optional[UserReference] = None
    dateModified: Optional[datetime] = Field(
        None,
        description="Deprecated - use dateTimeModified field instead",
        example='{ "epochSeconds": 1624619701, "nano": 0 }',
    )
    dateTimeModified: Optional[datetime] = None
    workflowSteps: Optional[List[WorkflowStepDto]] = None
    workflowSettings: Optional[List[WorkflowStepSettingsDto]] = None
    projectWorkflowSettings: Optional[ProjectWorkflowSettingsDto] = None
    businessUnit: Optional[BusinessUnitReference] = None
    notifyProviders: Optional[ProjectTemplateNotifyProviderDto] = None
    assignedTo: Optional[List[AssignmentPerTargetLangDto]] = None
    importSettings: Optional[UidReference] = Field(
        None, description="Deprecated - always null"
    )


class ProjectTemplateEditDto(BaseModel):
    name: Optional[constr(min_length=0, max_length=255)] = None
    templateName: constr(min_length=0, max_length=255)
    sourceLang: Optional[str] = None
    targetLangs: Optional[List[str]] = None
    useDynamicTitle: Optional[bool] = None
    dynamicTitle: Optional[constr(min_length=0, max_length=255)] = None
    notifyProvider: Optional[ProjectTemplateNotifyProviderDto] = Field(
        None,
        description="use to notify assigned providers,\n        notificationIntervalInMinutes 0 or empty value means immediate notification to all providers",
    )
    workFlowSettings: Optional[List[WorkflowStepSettingsEditDto]] = None
    projectWorkflowSettings: Optional[ProjectWorkflowSettingsDto] = None
    client: Optional[IdReference] = None
    costCenter: Optional[IdReference] = None
    businessUnit: Optional[IdReference] = None
    domain: Optional[IdReference] = None
    subDomain: Optional[IdReference] = None
    vendor: Optional[IdReference] = None
    importSettings: Optional[UidReference] = None
    note: Optional[constr(min_length=0, max_length=4096)] = None
    fileHandover: Optional[bool] = Field(None, description="Default: false")
    assignedTo: Optional[List[ProjectTemplateWorkflowSettingsAssignedToDto]] = Field(
        None,
        description="only use for projects without workflows; otherwise specify in the workflowSettings object",
    )


class PageDtoProjectTemplateReference(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[ProjectTemplateReference]] = None


class ServiceProviderConfigDto(BaseModel):
    authenticationSchemes: Optional[List[AuthSchema]] = None
    schemas: Optional[List[str]] = None
    patch: Optional[Supported] = None
    bulk: Optional[Supported] = None
    filter: Optional[Supported] = None
    changePassword: Optional[Supported] = None
    sort: Optional[Supported] = None
    etag: Optional[Supported] = None
    xmlDataFormat: Optional[Supported] = None


class PageDtoSegmentationRuleReference(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[SegmentationRuleReference]] = None


class CheckResponse(BaseModel):
    text: Optional[str] = None
    misspelledWords: Optional[List[MisspelledWord]] = None


class SpellCheckResponseDto(BaseModel):
    spellCheckResults: Optional[List[CheckResponse]] = None


class SuggestResponse(BaseModel):
    word: Optional[str] = None
    suggestions: Optional[List[Suggestion]] = None


class SuggestResponseDto(BaseModel):
    suggestResults: Optional[List[SuggestResponse]] = None


class ConceptListResponseDto(BaseModel):
    concepts: Optional[List[ConceptWithMetadataDto]] = None
    totalCount: Optional[int] = None


class MetadataResponse(BaseModel):
    segmentsCount: Optional[int] = None
    deduplicatedSegmentsCount: Optional[int] = None
    metadataByLanguage: Optional[Dict[str, LanguageMetadata1]] = None


class AsyncExportTMByQueryDto(BaseModel):
    asyncRequest: Optional[ObjectReference] = None
    transMemory: Optional[ObjectReference] = None
    exportTargetLangs: Optional[List[str]] = None
    queries: Optional[List[Query]] = None


class TranslationPriceListDto(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    dateCreated: Optional[datetime] = None
    name: str
    currencyCode: Optional[str] = None
    billingUnit: Optional[BillingUnit] = None
    priceSets: Optional[List[TranslationPriceSetDto]] = None


class PageDtoTranslationPriceListDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[TranslationPriceListDto]] = None


class PageDtoWebhookCallDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[WebhookCallDto]] = None


class PageDtoXmlAssistantProfileListDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[XmlAssistantProfileListDto]] = None


class DataDto(BaseModel):
    available: Optional[bool] = None
    estimate: Optional[bool] = None
    all: Optional[CountsDto] = None
    repetitions: Optional[CountsDto] = None
    transMemoryMatches: Optional[MatchCounts101Dto] = None
    machineTranslationMatches: Optional[MatchCountsDto] = None
    nonTranslatablesMatches: Optional[MatchCountsNTDto] = None
    internalFuzzyMatches: Optional[MatchCountsDto] = None


class AsyncResponseV2Dto(BaseModel):
    dateCreated: Optional[datetime] = None
    errorCode: Optional[str] = None
    errorDesc: Optional[str] = None
    errorDetails: Optional[List[ErrorDetailDtoV2]] = None
    warnings: Optional[List[ErrorDetailDtoV2]] = None


class CreateLqaConversationDto(BaseModel):
    lqaDescription: Optional[str] = None
    references: LQAReferences


class AbstractProjectDtoV2(BaseModel):
    uid: Optional[str] = None
    internalId: Optional[int] = None
    id: Optional[str] = None
    name: Optional[str] = None
    dateCreated: Optional[datetime] = None
    domain: Optional[DomainReference] = None
    subDomain: Optional[SubDomainReference] = None
    owner: Optional[UserReference] = None
    sourceLang: Optional[str] = None
    targetLangs: Optional[List[str]] = Field(None, unique_items=True)
    references: Optional[List[ReferenceFileReference]] = None
    mtSettingsPerLanguageList: Optional[List[MTSettingsPerLanguageReference]] = None
    userRole: Optional[str] = Field(
        None, description="Response differs based on user's role"
    )


class AdminProjectManagerV2(AbstractProjectDtoV2):
    shared: Optional[bool] = Field(None, description="Default: false")
    progress: Optional[ProgressDtoV2] = None
    client: Optional[ClientReference] = None
    costCenter: Optional[CostCenterReference] = None
    businessUnit: Optional[BusinessUnitReference] = None
    dateDue: Optional[datetime] = None
    status: Optional[Status2] = None
    purchaseOrder: Optional[str] = None
    isPublishedOnJobBoard: Optional[bool] = Field(None, description="Default: false")
    note: Optional[str] = None
    createdBy: Optional[UserReference] = None
    qualityAssuranceSettings: Optional[ObjectReference] = None
    workflowSteps: Optional[List[ProjectWorkflowStepDtoV2]] = None
    analyseSettings: Optional[ObjectReference] = None
    accessSettings: Optional[ObjectReference] = None
    financialSettings: Optional[ObjectReference] = None
    projectWorkflowSettings: Optional[ProjectWorkflowSettingsReference] = None


class LinguistV2(AbstractProjectDtoV2):
    pass


class ProjectWorkflowStepListDtoV2(BaseModel):
    projectWorkflowSteps: Optional[List[ProjectWorkflowStepDtoV2]] = None


class PseudoTranslateActionDtoV2(BaseModel):
    replacement: Optional[str] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    length: Optional[float] = None
    keyHashPrefixLen: Optional[conint(ge=0, le=18)] = None
    substitution: Optional[List[SubstituteDtoV2]] = Field(
        None, max_items=2147483647, min_items=0
    )


class PseudoTranslateWrapperDto(BaseModel):
    jobParts: JobPartReadyReferences
    pseudoTranslate: PseudoTranslateActionDtoV2


class JobPartReadyDeleteTranslationDto(BaseModel):
    jobs: Optional[List[UidReference]] = Field(None, max_items=100, min_items=1)
    deleteSettings: Optional[TranslationSegmentsReferenceV2] = None
    forAllJobs: Optional[bool] = Field(
        None,
        description="Set true if you want to delete translations for all jobs from project from specific workflow step.\n               Default: false",
    )
    workflowLevel: Optional[int] = Field(
        None, description="Specifies workflow level for all jobs"
    )
    filter: Optional[JobPartReadyDeleteTranslationFilterDto] = Field(
        None, description="Specifies filtering for all jobs"
    )


class UpdateIgnoredJobPartSegment(BaseModel):
    jobPartUid: str
    segments: List[UpdateIgnoredSegment] = Field(..., max_items=500, min_items=1)


class ProjectTemplateTransMemoryListV2Dto(BaseModel):
    transMemories: Optional[List[ProjectTemplateTransMemoryV2Dto]] = None


class SetContextPTTransMemoriesV2Dto(BaseModel):
    transMemories: List[SetProjectTemplateTransMemoryV2Dto]
    targetLang: Optional[str] = Field(
        None,
        description="Set translation memory only for the specific project target language",
    )
    workflowStep: Optional[UidReference] = Field(
        None, description="Set translation memory only for the specific workflow step"
    )
    orderEnabled: Optional[bool] = Field(None, description="Default: false")


class SetProjectTemplateTransMemoriesV2Dto(BaseModel):
    dataPerContext: List[SetContextPTTransMemoriesV2Dto]


class QuoteCreateV2Dto(BaseModel):
    name: constr(min_length=0, max_length=255)
    project: UidReference
    analyse: IdReference
    priceList: IdReference
    netRateScheme: Optional[IdReference] = None
    provider: Optional[ProviderReference] = None
    workflowSettings: Optional[List[QuoteWorkflowSettingDto]] = Field(
        None, unique_items=True
    )
    units: Optional[List[QuoteUnitsDto]] = None
    additionalSteps: Optional[List[str]] = None


class PageDtoWebHookDtoV2(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[WebHookDtoV2]] = None


class SearchInTextResponse2Dto(BaseModel):
    termBase: Optional[TermBaseReference] = None
    sourceTerm: Optional[TermV2Dto] = None
    concept: Optional[ConceptDtov2] = None
    translationTerms: Optional[List[TermV2Dto]] = None
    subTerm: Optional[bool] = None
    matches: Optional[List[Match]] = None


class SearchInTextResponseList2Dto(BaseModel):
    searchResults: Optional[List[SearchInTextResponse2Dto]] = None


class AnalyseLanguagePartV3Dto(BaseModel):
    id: Optional[str] = None
    sourceLang: Optional[str] = None
    targetLang: Optional[str] = None
    data: Optional[DataDto] = None
    discountedData: Optional[DataDto] = None
    jobs: Optional[List[AnalyseJobReference]] = None
    transMemories: Optional[List[TransMemoryReferenceDtoV2]] = None


class AnalyseV3Dto(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    innerId: Optional[int] = None
    type: Optional[AnalysisType] = None
    name: Optional[str] = None
    provider: Optional[ProviderReference] = None
    createdBy: Optional[UserReference] = None
    dateCreated: Optional[datetime] = None
    netRateScheme: Optional[NetRateSchemeReference] = None
    canChangeNetRateScheme: Optional[bool] = None
    analyseLanguageParts: Optional[List[AnalyseLanguagePartV3Dto]] = None
    settings: Optional[AbstractAnalyseSettingsDto] = None
    outdated: Optional[bool] = None
    importStatus: Optional[ImportStatusDto] = None
    pureWarnings: Optional[List[str]] = None
    project: Optional[ProjectReference] = None


class SearchTMSegmentDtoV3(BaseModel):
    id: Optional[str] = None
    text: Optional[str] = None
    lang: Optional[str] = None
    rtl: Optional[bool] = None
    modifiedAt: Optional[int] = None
    createdAt: Optional[int] = None
    modifiedBy: Optional[UserReference] = None
    createdBy: Optional[UserReference] = None
    filename: Optional[str] = None
    project: Optional[SearchTMProjectDtoV3] = None
    client: Optional[SearchTMClientDtoV3] = None
    domain: Optional[SearchTMDomainDtoV3] = None
    subDomain: Optional[SearchTMSubDomainDtoV3] = None
    tagMetadata: Optional[List[TagMetadata]] = None
    previousSegment: Optional[str] = None
    nextSegment: Optional[str] = None
    key: Optional[str] = None
    targetNote: Optional[str] = None


class AbsoluteTranslationLengthWarningDto(SegmentWarning):
    limit: Optional[str] = None


class CustomQAWarningDto(SegmentWarning):
    message: Optional[str] = None
    subType: Optional[str] = None
    srcPosition: Optional[Position] = None
    tgtPosition: Optional[Position] = None


class EmptyPairTagsWarningDto(SegmentWarning):
    pass


class EmptyTagContentWarningDto(EmptyPairTagsWarningDto):
    pass


class EmptyTranslationWarningDto(EmptyPairTagsWarningDto):
    pass


class ExtraNumbersV3WarningDto(SegmentWarning):
    number: Optional[str] = None
    positions: Optional[List[Position]] = None


class ExtraNumbersWarningDto(SegmentWarning):
    extraNumbers: Optional[List[str]] = None


class ForbiddenStringWarningDto(SegmentWarning):
    forbiddenString: Optional[str] = None
    positions: Optional[List[Position]] = None


class ForbiddenTermWarningDto(SegmentWarning):
    term: Optional[str] = None
    positions: Optional[List[Position]] = None
    sourceTerms: Optional[List[Term]] = None


class FormattingWarningDto(EmptyPairTagsWarningDto):
    pass


class FuzzyInconsistencyWarningDto(SegmentWarning):
    segmentIds: Optional[List[str]] = None


class InconsistentTagContentWarningDto(EmptyPairTagsWarningDto):
    pass


class InconsistentTranslationWarningDto(SegmentWarning):
    segmentId: Optional[str] = None


class JoinTagsWarningDto(SegmentWarning):
    sourceTagsCount: Optional[int] = None
    translationTagsCount: Optional[int] = None


class LeadingAndTrailingSpacesWarningDto(SegmentWarning):
    srcPosition: Optional[Position] = None
    srcWhitespaces: Optional[str] = None
    tgtPosition: Optional[Position] = None
    tgtWhitespaces: Optional[str] = None
    suggestion: Optional[Suggestion] = None


class MalformedWarningDto(SegmentWarning):
    message: Optional[str] = None


class MissingNonTranslatableAnnotationWarningDto(SegmentWarning):
    text: Optional[str] = None
    beginIndexes: Optional[List[int]] = None


class MissingNumbersV3WarningDto(ExtraNumbersV3WarningDto):
    pass


class MissingNumbersWarningDto(SegmentWarning):
    missingNumbers: Optional[List[str]] = None


class MoraviaWarningDto(SegmentWarning):
    message: Optional[str] = None
    subType: Optional[str] = None


class MultipleSpacesV3WarningDto(SegmentWarning):
    spaces: Optional[str] = None
    positions: Optional[List[Position]] = None


class MultipleSpacesWarningDto(EmptyPairTagsWarningDto):
    pass


class NestedTagsWarningDto(SegmentWarning):
    misplacedTargetTag: Optional[str] = None


class NewerAtLowerLevelWarningDto(EmptyPairTagsWarningDto):
    pass


class NonConformingTermWarningDto(SegmentWarning):
    term: Optional[str] = None
    positions: Optional[List[Position]] = None
    suggestedTargetTerms: Optional[List[Term]] = None


class NotConfirmedWarningDto(EmptyPairTagsWarningDto):
    pass


class RelativeTranslationLengthWarningDto(AbsoluteTranslationLengthWarningDto):
    pass


class RepeatedWordWarningDto(SegmentWarning):
    word: Optional[str] = None
    positions: Optional[List[Position]] = None


class RepeatedWordsWarningDto(SegmentWarning):
    repeatedWords: Optional[List[str]] = None


class SegmentWarningsDto(BaseModel):
    segmentId: Optional[str] = None
    warnings: Optional[List[SegmentWarning]] = None
    ignoredChecks: Optional[List[str]] = None


class SourceTargetRegexpWarningDto(SegmentWarning):
    description: Optional[str] = None


class SpellCheckWarningDto(SegmentWarning):
    misspelledWords: Optional[List[MisspelledWordDto]] = None


class TargetSourceIdenticalWarningDto(EmptyPairTagsWarningDto):
    pass


class TerminologyWarningDto(SegmentWarning):
    missingTerms: Optional[List[str]] = None
    forbiddenTerms: Optional[List[str]] = None


class TrailingPunctuationWarningDto(SegmentWarning):
    srcPosition: Optional[Position] = None
    srcEndPunctuation: Optional[str] = None
    tgtPosition: Optional[Position] = None
    tgtEndPunctuation: Optional[str] = None
    suggestedTgtEndPunctuation: Optional[str] = None


class TrailingSpaceWarningDto(EmptyPairTagsWarningDto):
    pass


class TranslationLengthWarningDto(EmptyPairTagsWarningDto):
    pass


class UnmodifiedFuzzyTranslationMTNTWarningDto(SegmentWarning):
    transOrigin: Optional[str] = None


class UnmodifiedFuzzyTranslationTMWarningDto(UnmodifiedFuzzyTranslationMTNTWarningDto):
    pass


class UnmodifiedFuzzyTranslationWarningDto(UnmodifiedFuzzyTranslationMTNTWarningDto):
    pass


class UnresolvedCommentWarningDto(EmptyPairTagsWarningDto):
    pass


class UnresolvedConversationWarningDto(EmptyPairTagsWarningDto):
    pass


class QualityAssuranceBatchRunDtoV3(BaseModel):
    jobs: List[UidReference] = Field(..., max_items=500, min_items=1)
    settings: Optional[QualityAssuranceRunDtoV3] = None
    maxQaWarningsCount: Optional[conint(ge=1, le=1000)] = Field(
        None,
        description="Maximum number of QA warnings in result, default: 100. For efficiency reasons QA\nwarnings are processed with minimum segments chunk size 10, therefore slightly more warnings are returned.",
    )


class ProjectTemplateTransMemoryDtoV3(BaseModel):
    targetLocale: Optional[str] = None
    workflowStep: Optional[WorkflowStepReferenceV3] = None
    readMode: Optional[bool] = None
    writeMode: Optional[bool] = None
    transMemory: Optional[TransMemoryDtoV3] = None
    penalty: Optional[float] = None
    applyPenaltyTo101Only: Optional[bool] = None
    order: Optional[int] = None


class ProjectTemplateTransMemoryListDtoV3(BaseModel):
    transMemories: Optional[List[ProjectTemplateTransMemoryDtoV3]] = None


class SetContextTransMemoriesDtoV3Dto(BaseModel):
    transMemories: List[SetProjectTransMemoryV3Dto]
    targetLang: Optional[str] = Field(
        None,
        description="Set translation memory only for the specific project target language",
    )
    workflowStep: Optional[UidReference] = Field(
        None, description="Set translation memory only for the specific workflow step"
    )
    orderEnabled: Optional[bool] = Field(None, description="Default: false")


class SetProjectTransMemoriesV3Dto(BaseModel):
    dataPerContext: List[SetContextTransMemoriesDtoV3Dto]


class ADMINRESPONSE(UserDetailsDtoV3):
    pass


class GUESTRESPONSE(UserDetailsDtoV3):
    client: ClientReference
    enableMT: Optional[bool] = None
    projectViewOther: Optional[bool] = None
    projectViewOtherLinguist: Optional[bool] = None
    projectViewOtherEditor: Optional[bool] = None
    transMemoryViewOther: Optional[bool] = None
    transMemoryEditOther: Optional[bool] = None
    transMemoryExportOther: Optional[bool] = None
    transMemoryImportOther: Optional[bool] = None
    termBaseViewOther: Optional[bool] = None
    termBaseEditOther: Optional[bool] = None
    termBaseExportOther: Optional[bool] = None
    termBaseImportOther: Optional[bool] = None
    termBaseApproveOther: Optional[bool] = None


class LINGUISTRESPONSE(UserDetailsDtoV3):
    editAllTermsInTB: Optional[bool] = None
    editTranslationsInTM: Optional[bool] = None
    enableMT: Optional[bool] = None
    mayRejectJobs: Optional[bool] = None
    sourceLocales: Optional[List[str]] = None
    targetLocales: Optional[List[str]] = None
    workflowSteps: Optional[List[WorkflowStepReferenceV3]] = None
    clients: Optional[List[ClientReference]] = None
    domains: Optional[List[DomainReference]] = None
    subDomains: Optional[List[SubDomainReference]] = None
    netRateScheme: Optional[DiscountSchemeReference] = None
    translationPriceList: Optional[PriceListReference] = None


class PROJECTMANAGERRESPONSE(UserDetailsDtoV3):
    sourceLocales: Optional[List[str]] = None
    targetLocales: Optional[List[str]] = None
    workflowSteps: Optional[List[WorkflowStepReferenceV3]] = None
    clients: Optional[List[ClientReference]] = None
    domains: Optional[List[DomainReference]] = None
    subDomains: Optional[List[SubDomainReference]] = None
    projectCreate: Optional[bool] = None
    projectViewOther: Optional[bool] = None
    projectEditOther: Optional[bool] = None
    projectDeleteOther: Optional[bool] = None
    projectClients: Optional[List[ClientReference]] = None
    projectBusinessUnits: Optional[List[BusinessUnitReference]] = None
    projectTemplateCreate: Optional[bool] = None
    projectTemplateViewOther: Optional[bool] = None
    projectTemplateEditOther: Optional[bool] = None
    projectTemplateDeleteOther: Optional[bool] = None
    projectTemplateClients: Optional[List[ClientReference]] = None
    projectTemplateBusinessUnits: Optional[List[BusinessUnitReference]] = None
    transMemoryCreate: Optional[bool] = None
    transMemoryViewOther: Optional[bool] = None
    transMemoryEditOther: Optional[bool] = None
    transMemoryDeleteOther: Optional[bool] = None
    transMemoryExportOther: Optional[bool] = None
    transMemoryImportOther: Optional[bool] = None
    transMemoryClients: Optional[List[ClientReference]] = None
    transMemoryBusinessUnits: Optional[List[BusinessUnitReference]] = None
    termBaseCreate: Optional[bool] = None
    termBaseViewOther: Optional[bool] = None
    termBaseEditOther: Optional[bool] = None
    termBaseDeleteOther: Optional[bool] = None
    termBaseExportOther: Optional[bool] = None
    termBaseImportOther: Optional[bool] = None
    termBaseApproveOther: Optional[bool] = None
    termBaseClients: Optional[List[ClientReference]] = None
    termBaseBusinessUnits: Optional[List[BusinessUnitReference]] = None
    userCreate: Optional[bool] = None
    userViewOther: Optional[bool] = None
    userEditOther: Optional[bool] = None
    userDeleteOther: Optional[bool] = None
    clientDomainSubDomainCreate: Optional[bool] = None
    clientDomainSubDomainViewOther: Optional[bool] = None
    clientDomainSubDomainEditOther: Optional[bool] = None
    clientDomainSubDomainDeleteOther: Optional[bool] = None
    vendorCreate: Optional[bool] = None
    vendorViewOther: Optional[bool] = None
    vendorEditOther: Optional[bool] = None
    vendorDeleteOther: Optional[bool] = None
    dashboardSetting: Optional[str] = None
    setupServer: Optional[bool] = None


class SUBMITTERRESPONSE(UserDetailsDtoV3):
    automationWidgets: List[IdReference]
    projectViewCreatedByOtherSubmitters: Optional[bool] = None


class ADMIN(AbstractUserCreateDto):
    pass


class ADMINEDIT(AbstractUserEditDto):
    pass


class AnalyseLanguagePartDto(BaseModel):
    id: Optional[str] = None
    sourceLang: Optional[str] = None
    targetLang: Optional[str] = None
    data: Optional[DataDtoV1] = None
    discountedData: Optional[DataDtoV1] = None
    jobs: Optional[List[AnalyseJobReference]] = None


class AsyncRequestDto(BaseModel):
    id: Optional[str] = None
    createdBy: Optional[UserReference] = None
    dateCreated: Optional[datetime] = None
    action: Optional[Action] = None
    asyncResponse: Optional[AsyncResponseDto] = None
    parent: Optional[AsyncRequestDto] = None
    project: Optional[ProjectReference] = None


class PageDtoAsyncRequestDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[AsyncRequestDto]] = None


class JobRoleDto(BaseModel):
    type: UserType
    workflowStep: Optional[ProjectWorkflowStepDtoV2] = Field(
        None,
        description="not null only for `PROVIDER` type and project with defined workflow steps",
    )
    organizationType: Optional[OrganizationType] = Field(
        None, description="not null only for shared projects"
    )


class MentionableUserDto(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    userName: Optional[str] = None
    email: Optional[str] = None
    role: Optional[Role] = None
    id: Optional[str] = None
    uid: Optional[str] = None
    unavailable: Optional[bool] = None
    jobRoles: Optional[List[JobRoleDto]] = None


class StatusDto(BaseModel):
    name: Optional[Name] = None
    by: Optional[MentionableUserDto] = None
    date: Optional[datetime] = None


class CustomFileTypeDto(BaseModel):
    uid: Optional[str] = None
    name: Optional[str] = None
    filenamePattern: Optional[str] = None
    type: Optional[str] = None
    createdBy: Optional[UserReference] = None
    dateCreated: Optional[datetime | str] = None
    fileImportSettings: Optional[FileImportSettingsDto] = None
    supportsContinuousJob: Optional[bool] = None


class PageDtoCustomFileTypeDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[CustomFileTypeDto]] = None


class SearchTMResponseDto(BaseModel):
    segmentId: Optional[str] = None
    source: Optional[SearchTMSegmentDto] = None
    translations: Optional[List[SearchTMSegmentDto]] = None
    transMemory: Optional[SearchTMTransMemoryDto] = None
    grossScore: Optional[float] = None
    score: Optional[float] = None
    subSegment: Optional[bool] = None


class ErrorCategoriesDto(BaseModel):
    accuracy: Optional[AccuracyWeightsDto] = None
    fluency: Optional[FluencyWeightsDto] = None
    terminology: Optional[TerminologyWeightsDto] = None
    style: Optional[StyleWeightsDto] = None
    localeConvention: Optional[LocaleConventionWeightsDto] = None
    verity: Optional[VerityWeightsDto] = None
    design: Optional[DesignWeightsDto] = None
    other: Optional[OtherWeightsDto] = None


class LqaProfileDetailDto(BaseModel):
    uid: str = Field(..., description="UID of the profile", example="string")
    name: str = Field(..., description="Name of the profile")
    errorCategories: ErrorCategoriesDto
    penaltyPoints: PenaltyPointsDto
    passFailThreshold: PassFailThresholdDto
    isDefault: bool = Field(
        ..., description="If profile is set as default for organization"
    )
    createdBy: UserReference
    dateCreated: datetime
    organization: UidReference


class CreateLqaProfileDto(BaseModel):
    name: constr(min_length=1, max_length=255)
    errorCategories: ErrorCategoriesDto
    penaltyPoints: Optional[PenaltyPointsDto] = None
    passFailThreshold: Optional[PassFailThresholdDto] = None


class UpdateLqaProfileDto(CreateLqaProfileDto):
    pass


class AbstractProjectDto(AbstractProjectDtoV2):
    pass


class AdminProjectManager(AbstractProjectDto):
    shared: Optional[bool] = Field(None, description="Default: false")
    progress: Optional[ProgressDto] = None
    client: Optional[ClientReference] = None
    costCenter: Optional[CostCenterReference] = None
    businessUnit: Optional[BusinessUnitReference] = None
    dateDue: Optional[datetime] = None
    status: Optional[Status2] = None
    purchaseOrder: Optional[str] = None
    isPublishedOnJobBoard: Optional[bool] = Field(None, description="Default: false")
    note: Optional[str] = None
    createdBy: Optional[UserReference] = None
    qualityAssuranceSettings: Optional[ObjectReference] = None
    workflowSteps: Optional[List[ProjectWorkflowStepDto]] = None
    analyseSettings: Optional[ObjectReference] = None
    accessSettings: Optional[ObjectReference] = None
    financialSettings: Optional[ObjectReference] = None
    projectWorkflowSettings: Optional[ProjectWorkflowSettingsReference] = None
    archived: Optional[bool] = None


class Buyer(AbstractProjectDto):
    shared: Optional[bool] = Field(None, description="Default: false")
    progress: Optional[ProgressDto] = None
    client: Optional[ClientReference] = None
    costCenter: Optional[CostCenterReference] = None
    businessUnit: Optional[BusinessUnitReference] = None
    dateDue: Optional[datetime] = None
    status: Optional[Status2] = None
    purchaseOrder: Optional[str] = None
    isPublishedOnJobBoard: Optional[bool] = Field(None, description="Default: false")
    note: Optional[str] = None
    createdBy: Optional[UserReference] = None
    qualityAssuranceSettings: Optional[ObjectReference] = None
    workflowSteps: Optional[List[ProjectWorkflowStepDto]] = None
    analyseSettings: Optional[ObjectReference] = None
    accessSettings: Optional[ObjectReference] = None
    financialSettings: Optional[ObjectReference] = None
    projectWorkflowSettings: Optional[ProjectWorkflowSettingsReference] = None
    archived: Optional[bool] = None
    vendorOwner: Optional[USER] = None
    vendor: Optional[VendorReference] = None


class Linguist(AbstractProjectDto):
    pass


class Vendor(AbstractProjectDto):
    shared: Optional[bool] = Field(None, description="Default: false")
    progress: Optional[ProgressDto] = None
    client: Optional[ClientReference] = None
    costCenter: Optional[CostCenterReference] = None
    businessUnit: Optional[BusinessUnitReference] = None
    dateDue: Optional[datetime] = None
    status: Optional[Status2] = None
    purchaseOrder: Optional[str] = None
    isPublishedOnJobBoard: Optional[bool] = Field(None, description="Default: false")
    note: Optional[str] = None
    createdBy: Optional[UserReference] = None
    qualityAssuranceSettings: Optional[ObjectReference] = None
    workflowSteps: Optional[List[ProjectWorkflowStepDto]] = None
    analyseSettings: Optional[ObjectReference] = None
    accessSettings: Optional[ObjectReference] = None
    financialSettings: Optional[ObjectReference] = None
    projectWorkflowSettings: Optional[ProjectWorkflowSettingsReference] = None
    archived: Optional[bool] = None
    buyerOwner: Optional[USER] = None
    buyer: Optional[BuyerReference] = None


class PageDtoAbstractProjectDto(BaseModel):
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    pageSize: Optional[int] = None
    pageNumber: Optional[int] = None
    numberOfElements: Optional[int] = None
    content: Optional[List[AbstractProjectDto]] = None


class AssignableTemplatesDto(BaseModel):
    assignableTemplates: Optional[List[ProjectTemplateDto]] = None


class AsyncRequestWrapperDto(BaseModel):
    asyncRequest: Optional[AsyncRequestDto] = None


class UpdateIgnoredWarningsDto(BaseModel):
    jobParts: List[UpdateIgnoredJobPartSegment] = Field(..., max_items=500, min_items=1)


class JobCreateRequestDto(BaseModel):
    targetLangs: List[str]
    due: Optional[datetime] = Field(
        None,
        description="only use for projects without workflows; otherwise specify in the workflowSettings object. Use ISO 8601 date format.",
    )
    workflowSettings: Optional[List[WorkflowStepConfiguration]] = None
    assignments: Optional[List[ProvidersPerLanguage]] = Field(
        None,
        description="only use for projects without workflows; otherwise specify in the workflowSettings object",
    )
    importSettings: Optional[UidReference] = None
    useProjectFileImportSettings: Optional[bool] = Field(
        None, description="Default: false"
    )
    preTranslate: Optional[bool] = None
    semanticMarkup: Optional[bool] = None
    notifyProvider: Optional[NotifyProviderDto] = Field(
        None,
        description="use to notify assigned providers, notificationIntervalInMinutes 0 or empty value means immediate notification to all providers",
    )
    callbackUrl: Optional[str] = None
    path: Optional[constr(min_length=0, max_length=255)] = None
    remoteFile: Optional[JobCreateRemoteFileDto] = None
    xmlAssistantProfile: Optional[UidReference] = None


class SearchResponseListTbDto(BaseModel):
    searchResults: Optional[List[SearchResponseTbDto]] = None


class BackgroundTasksTbDto(BaseModel):
    status: Optional[str] = None
    finishedDataText: Optional[str] = None
    asyncRequest: Optional[AsyncRequestDto] = None
    lastTaskString: Optional[str] = None
    metadata: Optional[MetadataResponse] = None
    lastTaskOk: Optional[str] = None
    lastTaskError: Optional[str] = None
    lastTaskErrorHtml: Optional[str] = None


class BackgroundTasksTmDto(BackgroundTasksTbDto):
    pass


class AsyncExportTMByQueryResponseDto(BaseModel):
    asyncRequest: Optional[AsyncRequestDto] = None
    asyncExport: Optional[AsyncExportTMByQueryDto] = None


class AnalyseLanguagePartV2Dto(BaseModel):
    id: Optional[str] = None
    sourceLang: Optional[str] = None
    targetLang: Optional[str] = None
    data: Optional[DataDto] = None
    discountedData: Optional[DataDto] = None
    jobs: Optional[List[AnalyseJobReference]] = None


class AnalyseV2Dto(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    type: Optional[AnalysisType] = None
    name: Optional[str] = None
    provider: Optional[ProviderReference] = None
    createdBy: Optional[UserReference] = None
    dateCreated: Optional[datetime] = None
    netRateScheme: Optional[NetRateSchemeReference] = None
    analyseLanguageParts: Optional[List[AnalyseLanguagePartV2Dto]] = None


class AnalysesV2Dto(BaseModel):
    analyses: Optional[List[AnalyseV2Dto]] = None


class AsyncRequestV2Dto(BaseModel):
    id: Optional[str] = None
    createdBy: Optional[UserReference] = None
    dateCreated: Optional[datetime] = None
    action: Optional[Action] = None
    asyncResponse: Optional[AsyncResponseV2Dto] = None
    parent: Optional[AsyncRequestV2Dto] = None
    project: Optional[ProjectReference] = None


class AsyncRequestWrapperV2Dto(BaseModel):
    asyncRequest: Optional[AsyncRequestV2Dto] = None


class AsyncExportTMResponseDto(BaseModel):
    asyncRequest: Optional[AsyncRequestV2Dto] = None
    asyncExport: Optional[AsyncExportTMDto] = None


class SearchTMResponseDtoV3(BaseModel):
    segmentId: Optional[str] = None
    source: Optional[SearchTMSegmentDtoV3] = None
    translations: Optional[List[SearchTMSegmentDtoV3]] = None
    transMemory: Optional[SearchTMTransMemoryDtoV3] = None
    grossScore: Optional[float] = None
    score: Optional[float] = None
    subSegment: Optional[bool] = None


class QualityAssuranceResponseDto(BaseModel):
    segmentWarnings: Optional[List[SegmentWarningsDto]] = None
    finished: Optional[bool] = None


class AsyncAnalyseResponseDto(BaseModel):
    asyncRequest: Optional[AsyncRequestDto] = None
    analyse: Optional[ObjectReference] = None


class AsyncAnalyseListResponseDto(BaseModel):
    analyses: Optional[List[AsyncAnalyseResponseDto]] = None


class AnalyseRecalculateResponseDto(AsyncAnalyseListResponseDto):
    pass


class MentionDto(BaseModel):
    mentionType: MentionType
    mentionGroupType: Optional[MentionGroupType] = None
    uidReference: Optional[UidReference] = None
    userReferences: Optional[List[MentionableUserDto]] = None
    mentionableGroup: Optional[MentionableGroupDto] = None
    tag: Optional[str] = None


class SearchResponseListTmDto(BaseModel):
    searchResults: Optional[List[SearchTMResponseDto]] = None


class AsyncAnalyseResponseV2Dto(BaseModel):
    asyncRequest: Optional[AsyncRequestV2Dto] = None
    analyse: Optional[ObjectReference] = None


class SearchResponseListTmDtoV3(BaseModel):
    searchResults: Optional[List[SearchTMResponseDtoV3]] = None


class CommentDto(BaseModel):
    id: Optional[str] = None
    text: Optional[str] = None
    createdBy: Optional[MentionableUserDto] = None
    dateCreated: Optional[datetime] = None
    dateModified: Optional[datetime] = None
    mentions: Optional[List[MentionDto]] = None


class CommonConversationDto(BaseModel):
    id: Optional[str] = None
    type: Optional[str] = Field(
        None, description="Field references differs based on the Conversation Type."
    )
    dateCreated: Optional[datetime] = None
    dateModified: Optional[datetime] = None
    dateEdited: Optional[datetime] = None
    createdBy: Optional[MentionableUserDto] = None
    comments: Optional[List[CommentDto]] = None
    status: Optional[StatusDto] = None
    deleted: Optional[bool] = None


class ConversationListDto(BaseModel):
    conversations: Optional[List[CommonConversationDto]] = None


class LQA(CommonConversationDto):
    references: Optional[LQAReferences] = None
    lqaDescription: Optional[str] = None


class SEGMENTTARGET(CommonConversationDto):
    references: Optional[PlainReferences] = None


class LQAConversationDto(BaseModel):
    id: Optional[str] = None
    type: Optional[str] = Field(None, description="LQA")
    dateCreated: Optional[datetime] = None
    dateModified: Optional[datetime] = None
    dateEdited: Optional[datetime] = None
    createdBy: Optional[MentionableUserDto] = None
    comments: Optional[List[CommentDto]] = None
    status: Optional[StatusDto] = None
    deleted: Optional[bool] = None
    references: Optional[LQAReferences] = None
    lqaDescription: Optional[str] = None


class LQAConversationsListDto(BaseModel):
    conversations: Optional[List[LQAConversationDto]] = None


class PlainConversationDto(BaseModel):
    id: Optional[str] = None
    type: Optional[str] = Field(None, description="SEGMENT_TARGET")
    dateCreated: Optional[datetime] = None
    dateModified: Optional[datetime] = None
    dateEdited: Optional[datetime] = None
    createdBy: Optional[MentionableUserDto] = None
    comments: Optional[List[CommentDto]] = None
    status: Optional[StatusDto] = None
    deleted: Optional[bool] = None
    references: Optional[PlainReferences] = None


class PlainConversationsListDto(BaseModel):
    conversations: Optional[List[PlainConversationDto]] = None


class AsyncAnalyseListResponseV2Dto(BaseModel):
    asyncRequests: Optional[List[AsyncAnalyseResponseV2Dto]] = None


class AddLqaCommentResultDto(BaseModel):
    id: Optional[str] = Field(None, description="ID of created comment")
    conversation: Optional[LQAConversationDto] = Field(
        None, description="LQA Conversation"
    )


class AddPlainCommentResultDto(BaseModel):
    id: Optional[str] = Field(None, description="ID of created comment")
    conversation: Optional[PlainConversationDto] = Field(
        None, description="Conversation"
    )


LqaErrorCategoryDto.update_forward_refs()
Attribute.update_forward_refs()
AsyncRequestDto.update_forward_refs()
AsyncRequestV2Dto.update_forward_refs()
