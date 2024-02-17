from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    AbstractProjectDto,
    AbstractProjectDtoV2,
    AddTargetLangDto,
    AddWorkflowStepsDto,
    AdminProjectManager,
    AnalyseSettingsDto,
    AssignableTemplatesDto,
    AssignVendorDto,
    AsyncRequestWrapperV2Dto,
    Buyer,
    CloneProjectDto,
    CreateCustomFieldInstancesDto,
    CreateProjectFromTemplateAsyncV2Dto,
    CreateProjectFromTemplateV2Dto,
    CreateProjectV3Dto,
    CustomFieldInstanceDto,
    CustomFieldInstancesDto,
    EditProjectMTSettingsDto,
    EditProjectMTSettPerLangListDto,
    EditProjectSecuritySettingsDtoV2,
    EditProjectV2Dto,
    EditQASettingsDtoV2,
    EnabledQualityChecksDto,
    FileImportSettingsCreateDto,
    FileImportSettingsDto,
    FileNamingSettingsDto,
    FinancialSettingsDto,
    JobPartReferences,
    JobPartsDto,
    LqaSettingsDto,
    MTSettingsPerLanguageListDto,
    PageDtoAbstractProjectDto,
    PageDtoAnalyseReference,
    PageDtoCustomFieldInstanceDto,
    PageDtoProviderReference,
    PageDtoQuoteDto,
    PageDtoTermBaseDto,
    PageDtoTransMemoryDto,
    PatchProjectDto,
    PreTranslateSettingsV4Dto,
    ProjectSecuritySettingsDtoV2,
    ProjectTermBaseListDto,
    ProjectTransMemoryListDtoV3,
    ProjectWorkflowStepListDtoV2,
    ProviderListDtoV2,
    QASettingsDtoV2,
    SearchResponseListTmDto,
    SearchTMRequestDto,
    SetFinancialSettingsDto,
    SetProjectStatusDto,
    SetProjectTransMemoriesV3Dto,
    SetTermBaseDto,
    UpdateCustomFieldInstanceDto,
    UpdateCustomFieldInstancesDto,
)


class ProjectOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def addWorkflowSteps(
        self,
        projectUid: str,
        body: AddWorkflowStepsDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Add workflow steps

        :param projectUid: string (required), path.
        :param body: AddWorkflowStepsDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/workflowSteps"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def getProject(
        self,
        projectUid: str,
        phrase_token: Optional[str] = None,
    ) -> AdminProjectManager | Buyer | AbstractProjectDto:
        """
                Get project
                This API call retrieves information specific to a project.

        The level of detail in the response varies based on the user's role. Admins, Project Managers, Vendors, Buyers, and
        Linguists receive different responses, detailed below.

        - Details about predefined system metadata, such as client, domain, subdomain, cost center, business unit, or status.
        Note that [Custom Fields](#operation/getCustomField_1), if added to projects, are not included here and require
        retrieval via a dedicated Custom Fields API call. Metadata exposed to Linguists or Vendors might differ from what's
        visible to Admins or Project Managers.
        - [Workflow Step](https://support.phrase.com/hc/en-us/articles/5709717879324-Workflow-TMS-) information, crucial for
        user or vendor assignments through APIs. When projects are created, each workflow step's global ID instantiates into a
        project-specific workflow step ID necessary for user assignments. Attempting to assign the global workflow step ID
        (found under Settings or via Workflow Step APIs) results in an error, as only the project-specific step can be assigned.
        - Progress information indicating the total number of jobs across all workflow steps in the project, alongside the
        proportion of completed and overdue jobs.
                :param projectUid: string (required), path.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: AbstractProjectDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )
        user_role = r.get("userRole")
        match user_role:
            case "PROJECT_MANAGER":
                return AdminProjectManager(**r)
            case "BUYER":
                return Buyer(**r)
            case _:
                return AbstractProjectDto(**r)

    def deleteProject(
        self,
        projectUid: str,
        purge: bool = "False",
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete project

        :param projectUid: string (required), path.
        :param purge: boolean (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}"
        params = {"purge": purge}

        files = None
        payload = None

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def patchProject(
        self,
        projectUid: str,
        body: PatchProjectDto,
        phrase_token: Optional[str] = None,
    ) -> AbstractProjectDto:
        """
        Edit project

        :param projectUid: string (required), path.
        :param body: PatchProjectDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AbstractProjectDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}"
        params = {}

        files = None
        payload = body

        r = self.client.patch(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AbstractProjectDto(**r)

    def listProjects(
        self,
        nameOrInternalId: str = None,
        buyerId: int = None,
        jobStatusGroup: str = None,
        jobStatuses: List[str] = None,
        ownerId: int = None,
        sourceLangs: List[str] = None,
        createdInLastHours: int = None,
        dueInHours: int = None,
        costCenterName: str = None,
        costCenterId: int = None,
        subDomainName: str = None,
        subDomainId: int = None,
        domainName: str = None,
        domainId: int = None,
        targetLangs: List[str] = None,
        statuses: List[str] = None,
        businessUnitName: str = None,
        businessUnitId: int = None,
        clientName: str = None,
        clientId: int = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        includeArchived: bool = "False",
        archivedOnly: bool = "False",
        phrase_token: Optional[str] = None,
    ) -> PageDtoAbstractProjectDto:
        """
                List projects
                API call to retrieve a paginated list of projects. Contains a subset of information contained in
        [Get project](#operation/getProject) API call.

        Utilize the query parameters below to refine the search criteria:

        - **name** - The full project name or a portion of it. For instance, using `name=GUI` or `name=02` will find projects
        named `GUI02`.
        - **clientId** - The client's ID within the system, not interchangeable with its UID.
        - **clientName** - The complete or partial name of the client. For example, using `clientName=GUI` or `clientName=02`
        will find projects associated with the client `GUI02`.
        - **businessUnitId** - The business unit's ID within the system, not interchangeable with its UID.
        - **businessUnitName** - The complete or partial name of the business unit. For instance, using `businessUnitName=GUI`
        or `businessUnitName=02` will find projects linked to the business unit `GUI02`.
        - **statuses** - A list of project statuses. When adding multiple statuses, include each as a dedicated query
        parameter, e.g., `statuses=ASSIGNED&statuses=COMPLETED`.
        - **domainId** - The domain's ID within the system, not interchangeable with its UID.
        - **domainName** - The complete or partial name of the domain. Using `domainName=GUI` or `domainName=02` will find
        projects associated with the domain `GUI02`.
        - **subDomainId** - The subdomain's ID within the system, not interchangeable with its UID.
        - **subDomainName** - The complete or partial name of the subdomain. For example, using `subDomainName=GUI` or
        `subDomainName=02` will find projects linked to the subdomain `GUI02`.
        - **costCenterId** - The cost center's ID within the system, not interchangeable with its UID.
        - **costCenterName** - The complete or partial name of the cost center. For instance, using `costCenterName=GUI` or
        `costCenterName=02` will find projects associated with the cost center `GUI02`.
        - **dueInHours** - Filter for jobs with due dates less than or equal to the specified number of hours.
        - **createdInLastHours** - Filter for jobs created within the specified number of hours.
        - **ownerId** - The user ID who owns the project within the system, not interchangeable with its UID.
        - **jobStatuses** - A list of statuses for jobs within the projects. Include each status as a dedicated query parameter,
        e.g., `jobStatuses=ASSIGNED&jobStatuses=COMPLETED`.
        - **jobStatusGroup** - The name of the status group used to filter projects containing at least one job with the
        specified status, similar to the status filter in the Projects list for a Linguist user.
        - **buyerId** - The Buyer's ID.
        - **pageNumber** - Indicates the desired page number (zero-based) to retrieve. The total number of pages is returned in
        the `totalPages` field within each response.
        - **pageSize** - Indicates the page size, affecting the `totalPages` retrieved in each response and potentially
        influencing the number of iterations needed to obtain all projects.
        - **nameOrInternalId** - Specify either the project name or Internal ID (the sequence number in the project list
        displayed in the UI).
        - **includeArchived** - A boolean parameter to include archived projects in the search.
        - **archivedOnly** - A boolean search indicating whether only archived projects should be searched.
                :param nameOrInternalId: string (optional), query. Name or internal ID of project.
                :param buyerId: integer (optional), query.
                :param jobStatusGroup: string (optional), query. Allowed for linguists only.
                :param jobStatuses: array (optional), query. Allowed for linguists only.
                :param ownerId: integer (optional), query.
                :param sourceLangs: array (optional), query.
                :param createdInLastHours: integer (optional), query.
                :param dueInHours: integer (optional), query. -1 for projects that are overdue.
                :param costCenterName: string (optional), query.
                :param costCenterId: integer (optional), query.
                :param subDomainName: string (optional), query.
                :param subDomainId: integer (optional), query.
                :param domainName: string (optional), query.
                :param domainId: integer (optional), query.
                :param targetLangs: array (optional), query.
                :param statuses: array (optional), query.
                :param businessUnitName: string (optional), query.
                :param businessUnitId: integer (optional), query.
                :param clientName: string (optional), query.
                :param clientId: integer (optional), query.
                :param name: string (optional), query.
                :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
                :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.
                :param includeArchived: boolean (optional), query. List also archived projects.
                :param archivedOnly: boolean (optional), query. List only archived projects, regardless of `includeArchived`.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: PageDtoAbstractProjectDto
        """
        endpoint = "/api2/v1/projects"
        params = {
            "name": name,
            "clientId": clientId,
            "clientName": clientName,
            "businessUnitId": businessUnitId,
            "businessUnitName": businessUnitName,
            "statuses": statuses,
            "targetLangs": targetLangs,
            "domainId": domainId,
            "domainName": domainName,
            "subDomainId": subDomainId,
            "subDomainName": subDomainName,
            "costCenterId": costCenterId,
            "costCenterName": costCenterName,
            "dueInHours": dueInHours,
            "createdInLastHours": createdInLastHours,
            "sourceLangs": sourceLangs,
            "ownerId": ownerId,
            "jobStatuses": jobStatuses,
            "jobStatusGroup": jobStatusGroup,
            "buyerId": buyerId,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "nameOrInternalId": nameOrInternalId,
            "includeArchived": includeArchived,
            "archivedOnly": archivedOnly,
        }

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoAbstractProjectDto(**r)

    def assignableTemplates(
        self,
        projectUid: str,
        phrase_token: Optional[str] = None,
    ) -> AssignableTemplatesDto:
        """
        List assignable templates

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AssignableTemplatesDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/assignableTemplates"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AssignableTemplatesDto(**r)

    def assignLinguistsFromTemplate(
        self,
        projectUid: str,
        templateUid: str,
        phrase_token: Optional[str] = None,
    ) -> JobPartsDto:
        """
        Assigns providers from template

        :param projectUid: string (required), path.
        :param templateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: JobPartsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/applyTemplate/{templateUid}/assignProviders"
        params = {}

        files = None
        payload = None

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return JobPartsDto(**r)

    def assignLinguistsFromTemplateToJobParts(
        self,
        projectUid: str,
        templateUid: str,
        body: JobPartReferences,
        phrase_token: Optional[str] = None,
    ) -> JobPartsDto:
        """
        Assigns providers from template (specific jobs)

        :param projectUid: string (required), path.
        :param templateUid: string (required), path.
        :param body: JobPartReferences (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: JobPartsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/applyTemplate/{templateUid}/assignProviders/forJobParts"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return JobPartsDto(**r)

    def addTargetLanguageToProject(
        self,
        projectUid: str,
        body: AddTargetLangDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Add target languages
        Add target languages to project
        :param projectUid: string (required), path.
        :param body: AddTargetLangDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/targetLangs"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def assignVendorToProject(
        self,
        projectUid: str,
        body: AssignVendorDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
                Assign vendor
                To unassign Vendor from Project, use empty body:
        ```
        {}
        ```
                :param projectUid: string (required), path.
                :param body: AssignVendorDto (required), body.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/assignVendor"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def cloneProject(
        self,
        projectUid: str,
        body: CloneProjectDto,
        phrase_token: Optional[str] = None,
    ) -> AbstractProjectDto:
        """
        Clone project

        :param projectUid: string (required), path.
        :param body: CloneProjectDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AbstractProjectDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/clone"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AbstractProjectDto(**r)

    def getProjectAssignments(
        self,
        projectUid: str,
        providerName: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoProviderReference:
        """
        List project providers

        :param projectUid: string (required), path.
        :param providerName: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoProviderReference
        """
        endpoint = f"/api2/v1/projects/{projectUid}/providers"
        params = {
            "providerName": providerName,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoProviderReference(**r)

    def setProjectStatus(
        self,
        projectUid: str,
        body: SetProjectStatusDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Edit project status

        :param projectUid: string (required), path.
        :param body: SetProjectStatusDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/setStatus"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def getFinancialSettings(
        self,
        projectUid: str,
        phrase_token: Optional[str] = None,
    ) -> FinancialSettingsDto:
        """
        Get financial settings

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: FinancialSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/financialSettings"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return FinancialSettingsDto(**r)

    def setFinancialSettings(
        self,
        projectUid: str,
        body: SetFinancialSettingsDto,
        phrase_token: Optional[str] = None,
    ) -> FinancialSettingsDto:
        """
        Edit financial settings

        :param projectUid: string (required), path.
        :param body: SetFinancialSettingsDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: FinancialSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/financialSettings"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return FinancialSettingsDto(**r)

    def enabledQualityChecks(
        self,
        projectUid: str,
        phrase_token: Optional[str] = None,
    ) -> EnabledQualityChecksDto:
        """
        Get QA checks
        Returns enabled quality assurance settings.
        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: EnabledQualityChecksDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/qaSettingsChecks"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return EnabledQualityChecksDto(**r)

    def getProjectSettings(
        self,
        projectUid: str,
        workflowLevel: int = "1",
        phrase_token: Optional[str] = None,
    ) -> LqaSettingsDto:
        """
        Get LQA settings

        :param projectUid: string (required), path.
        :param workflowLevel: integer (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LqaSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/lqaSettings"
        params = {"workflowLevel": workflowLevel}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LqaSettingsDto(**r)

    def getMtSettingsForProject(
        self,
        projectUid: str,
        phrase_token: Optional[str] = None,
    ) -> MTSettingsPerLanguageListDto:
        """
        Get project machine translate settings

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: MTSettingsPerLanguageListDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/mtSettings"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return MTSettingsPerLanguageListDto(**r)

    def setMtSettingsForProject(
        self,
        projectUid: str,
        body: EditProjectMTSettingsDto,
        phrase_token: Optional[str] = None,
    ) -> MTSettingsPerLanguageListDto:
        """
        Edit machine translate settings
        This will erase all mtSettings per language for project.
        To remove all machine translate settings from project call without a machineTranslateSettings parameter.
        :param projectUid: string (required), path.
        :param body: EditProjectMTSettingsDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: MTSettingsPerLanguageListDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/mtSettings"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return MTSettingsPerLanguageListDto(**r)

    def getQuotesForProject(
        self,
        projectUid: str,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoQuoteDto:
        """
        List quotes

        :param projectUid: string (required), path.
        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoQuoteDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/quotes"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoQuoteDto(**r)

    def setMtSettingsPerLanguageForProject(
        self,
        projectUid: str,
        body: EditProjectMTSettPerLangListDto,
        phrase_token: Optional[str] = None,
    ) -> MTSettingsPerLanguageListDto:
        """
        Edit machine translate settings per language
        This will erase mtSettings for project
        :param projectUid: string (required), path.
        :param body: EditProjectMTSettPerLangListDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: MTSettingsPerLanguageListDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/mtSettingsPerLanguage"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return MTSettingsPerLanguageListDto(**r)

    def getAnalyseSettingsForProject(
        self,
        projectUid: str,
        phrase_token: Optional[str] = None,
    ) -> AnalyseSettingsDto:
        """
        Get analyse settings

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AnalyseSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/analyseSettings"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AnalyseSettingsDto(**r)

    def getImportSettings_2(
        self,
        projectUid: str,
        phrase_token: Optional[str] = None,
    ) -> FileImportSettingsDto:
        """
        Get projects's default import settings

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: FileImportSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/importSettings"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return FileImportSettingsDto(**r)

    def editImportSettings_1(
        self,
        projectUid: str,
        body: FileImportSettingsCreateDto,
        phrase_token: Optional[str] = None,
    ) -> FileImportSettingsDto:
        """
        Edit project import settings

        :param projectUid: string (required), path.
        :param body: FileImportSettingsCreateDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: FileImportSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/importSettings"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return FileImportSettingsDto(**r)

    def getFileNamingSettings(
        self,
        projectUid: str,
        phrase_token: Optional[str] = None,
    ) -> FileNamingSettingsDto:
        """
        Get file naming settings for project

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: FileNamingSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/fileNamingSettings"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return FileNamingSettingsDto(**r)

    def updateFileNamingSettings(
        self,
        projectUid: str,
        body: FileNamingSettingsDto,
        phrase_token: Optional[str] = None,
    ) -> FileNamingSettingsDto:
        """
        Update file naming settings for project

        :param projectUid: string (required), path.
        :param body: FileNamingSettingsDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: FileNamingSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/fileNamingSettings"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return FileNamingSettingsDto(**r)

    def getCustomFieldsPage(
        self,
        projectUid: str,
        sortField: str = None,
        modifiedBy: List[str] = None,
        createdBy: List[str] = None,
        pageNumber: int = "0",
        pageSize: int = "20",
        sortTrend: str = "ASC",
        phrase_token: Optional[str] = None,
    ) -> PageDtoCustomFieldInstanceDto:
        """
        Get custom fields of project (page)

        :param projectUid: string (required), path.
        :param sortField: string (optional), query. Sort by this field.
        :param modifiedBy: array (optional), query. Filter by webhook updaters UIDs.
        :param createdBy: array (optional), query. Filter by webhook creators UIDs.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 20.
        :param sortTrend: string (optional), query. Sort direction.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoCustomFieldInstanceDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/customFields"
        params = {
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "createdBy": createdBy,
            "modifiedBy": modifiedBy,
            "sortField": sortField,
            "sortTrend": sortTrend,
        }

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoCustomFieldInstanceDto(**r)

    def createCustomFields(
        self,
        projectUid: str,
        body: CreateCustomFieldInstancesDto,
        phrase_token: Optional[str] = None,
    ) -> CustomFieldInstancesDto:
        """
        Create custom field instances

        :param projectUid: string (required), path.
        :param body: CreateCustomFieldInstancesDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: CustomFieldInstancesDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/customFields"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return CustomFieldInstancesDto(**r)

    def editCustomFields(
        self,
        projectUid: str,
        body: UpdateCustomFieldInstancesDto,
        phrase_token: Optional[str] = None,
    ) -> CustomFieldInstancesDto:
        """
        Edit custom fields of the project (batch)

        :param projectUid: string (required), path.
        :param body: UpdateCustomFieldInstancesDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: CustomFieldInstancesDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/customFields"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return CustomFieldInstancesDto(**r)

    def getCustomField_1(
        self,
        fieldInstanceUid: str,
        projectUid: str,
        phrase_token: Optional[str] = None,
    ) -> CustomFieldInstanceDto:
        """
        Get custom field of project

        :param fieldInstanceUid: string (required), path.
        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: CustomFieldInstanceDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/customFields/{fieldInstanceUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return CustomFieldInstanceDto(**r)

    def editCustomField(
        self,
        fieldInstanceUid: str,
        projectUid: str,
        body: UpdateCustomFieldInstanceDto,
        phrase_token: Optional[str] = None,
    ) -> CustomFieldInstanceDto:
        """
        Edit custom field of project

        :param fieldInstanceUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: UpdateCustomFieldInstanceDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: CustomFieldInstanceDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/customFields/{fieldInstanceUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return CustomFieldInstanceDto(**r)

    def deleteCustomField_1(
        self,
        fieldInstanceUid: str,
        projectUid: str,
        phrase_token: Optional[str] = None,
    ) -> dict:
        """
        Delete custom field of project

        :param fieldInstanceUid: string (required), path.
        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return:
        """
        endpoint = f"/api2/v1/projects/{projectUid}/customFields/{fieldInstanceUid}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    def getProjectTermBases(
        self,
        projectUid: str,
        phrase_token: Optional[str] = None,
    ) -> ProjectTermBaseListDto:
        """
        Get term bases

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTermBaseListDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/termBases"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTermBaseListDto(**r)

    def setProjectTermBases(
        self,
        projectUid: str,
        body: SetTermBaseDto,
        phrase_token: Optional[str] = None,
    ) -> ProjectTermBaseListDto:
        """
        Edit term bases

        :param projectUid: string (required), path.
        :param body: SetTermBaseDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTermBaseListDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/termBases"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTermBaseListDto(**r)

    def relevantTermBases(
        self,
        projectUid: str,
        targetLangs: List[str] = None,
        subDomainName: str = None,
        clientName: str = None,
        domainName: str = None,
        name: str = None,
        strictLangMatching: bool = "False",
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoTermBaseDto:
        """
        List project relevant term bases

        :param projectUid: string (required), path.
        :param targetLangs: array (optional), query.
        :param subDomainName: string (optional), query.
        :param clientName: string (optional), query.
        :param domainName: string (optional), query.
        :param name: string (optional), query.
        :param strictLangMatching: boolean (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoTermBaseDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/termBases/relevant"
        params = {
            "name": name,
            "domainName": domainName,
            "clientName": clientName,
            "subDomainName": subDomainName,
            "targetLangs": targetLangs,
            "strictLangMatching": strictLangMatching,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoTermBaseDto(**r)

    def relevantTransMemories_1(
        self,
        projectUid: str,
        targetLangs: List[str] = None,
        subDomainName: str = None,
        clientName: str = None,
        domainName: str = None,
        name: str = None,
        strictLangMatching: bool = "False",
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoTransMemoryDto:
        """
        List project relevant translation memories

        :param projectUid: string (required), path.
        :param targetLangs: array (optional), query.
        :param subDomainName: string (optional), query.
        :param clientName: string (optional), query.
        :param domainName: string (optional), query.
        :param name: string (optional), query.
        :param strictLangMatching: boolean (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoTransMemoryDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/transMemories/relevant"
        params = {
            "name": name,
            "domainName": domainName,
            "clientName": clientName,
            "subDomainName": subDomainName,
            "targetLangs": targetLangs,
            "strictLangMatching": strictLangMatching,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoTransMemoryDto(**r)

    def searchSegment_1(
        self,
        projectUid: str,
        body: SearchTMRequestDto,
        phrase_token: Optional[str] = None,
    ) -> SearchResponseListTmDto:
        """
        Search translation memory for segment in the project
        Returns at most <i>maxSegments</i>
            records with <i>score >= scoreThreshold</i> and at most <i>maxSubsegments</i> records which are subsegment,
            i.e. the source text is substring of the query text.
        :param projectUid: string (required), path.
        :param body: SearchTMRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SearchResponseListTmDto
        """
        endpoint = (
            f"/api2/v1/projects/{projectUid}/transMemories/searchSegmentInProject"
        )
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SearchResponseListTmDto(**r)

    def getProjectAccessSettingsV2(
        self,
        projectUid: str,
        phrase_token: Optional[str] = None,
    ) -> ProjectSecuritySettingsDtoV2:
        """
        Get access and security settings

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectSecuritySettingsDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/accessSettings"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectSecuritySettingsDtoV2(**r)

    def editProjectAccessSettingsV2(
        self,
        projectUid: str,
        body: EditProjectSecuritySettingsDtoV2,
        phrase_token: Optional[str] = None,
    ) -> ProjectSecuritySettingsDtoV2:
        """
        Edit access and security settings

        :param projectUid: string (required), path.
        :param body: EditProjectSecuritySettingsDtoV2 (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectSecuritySettingsDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/accessSettings"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectSecuritySettingsDtoV2(**r)

    def getProjectWorkflowStepsV2(
        self,
        projectUid: str,
        withAssignedJobs: bool = "False",
        phrase_token: Optional[str] = None,
    ) -> ProjectWorkflowStepListDtoV2:
        """
        Get workflow steps

        :param projectUid: string (required), path.
        :param withAssignedJobs: boolean (optional), query. Return only steps containing jobs assigned to the calling linguist..

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectWorkflowStepListDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/workflowSteps"
        params = {"withAssignedJobs": withAssignedJobs}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectWorkflowStepListDtoV2(**r)

    def editProjectV2(
        self,
        projectUid: str,
        body: EditProjectV2Dto,
        phrase_token: Optional[str] = None,
    ) -> AbstractProjectDtoV2:
        """
        Edit project

        :param projectUid: string (required), path.
        :param body: EditProjectV2Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AbstractProjectDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AbstractProjectDtoV2(**r)

    def setProjectQASettingsV2(
        self,
        projectUid: str,
        body: EditQASettingsDtoV2,
        phrase_token: Optional[str] = None,
    ) -> QASettingsDtoV2:
        """
        Edit quality assurance settings

        :param projectUid: string (required), path.
        :param body: EditQASettingsDtoV2 (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: QASettingsDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/qaSettings"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return QASettingsDtoV2(**r)

    def createProjectFromTemplateV2(
        self,
        templateUid: str,
        body: CreateProjectFromTemplateV2Dto,
        phrase_token: Optional[str] = None,
    ) -> AbstractProjectDtoV2:
        """
        Create project from template

        :param templateUid: string (required), path.
        :param body: CreateProjectFromTemplateV2Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AbstractProjectDtoV2
        """
        endpoint = f"/api2/v2/projects/applyTemplate/{templateUid}"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AbstractProjectDtoV2(**r)

    def createProjectFromTemplateV2Async(
        self,
        templateUid: str,
        body: CreateProjectFromTemplateAsyncV2Dto,
        phrase_token: Optional[str] = None,
    ) -> AsyncRequestWrapperV2Dto:
        """
        Create project from template (async)

        :param templateUid: string (required), path.
        :param body: CreateProjectFromTemplateAsyncV2Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AsyncRequestWrapperV2Dto
        """
        endpoint = f"/api2/v2/projects/applyTemplate/async/{templateUid}"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AsyncRequestWrapperV2Dto(**r)

    def listProviders_3(
        self,
        projectUid: str,
        phrase_token: Optional[str] = None,
    ) -> ProviderListDtoV2:
        """
        Get suggested providers

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProviderListDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/providers/suggest"
        params = {}

        files = None
        payload = None

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProviderListDtoV2(**r)

    def listByProjectV3(
        self,
        projectUid: str,
        onlyOwnerOrg: bool = None,
        uid: str = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        sort: str = "DATE_CREATED",
        order: str = "desc",
        phrase_token: Optional[str] = None,
    ) -> PageDtoAnalyseReference:
        """
        List analyses by project

        :param projectUid: string (required), path.
        :param onlyOwnerOrg: boolean (optional), query.
        :param uid: string (optional), query. Uid to search by.
        :param name: string (optional), query. Name to search by.
        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.
        :param sort: string (optional), query. Sorting field.
        :param order: string (optional), query. Sorting order.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoAnalyseReference
        """
        endpoint = f"/api2/v3/projects/{projectUid}/analyses"
        params = {
            "name": name,
            "uid": uid,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "sort": sort,
            "order": order,
            "onlyOwnerOrg": onlyOwnerOrg,
        }

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoAnalyseReference(**r)

    def createProjectV3(
        self,
        body: CreateProjectV3Dto,
        phrase_token: Optional[str] = None,
    ) -> AbstractProjectDtoV2:
        """
        Create project

        :param body: CreateProjectV3Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AbstractProjectDtoV2
        """
        endpoint = "/api2/v3/projects"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AbstractProjectDtoV2(**r)

    def getProjectTransMemories_1(
        self,
        projectUid: str,
        wfStepUid: str = None,
        targetLang: str = None,
        phrase_token: Optional[str] = None,
    ) -> ProjectTransMemoryListDtoV3:
        """
        Get translation memories

        :param projectUid: string (required), path.
        :param wfStepUid: string (optional), query. Filter project translation memories by workflow step.
        :param targetLang: string (optional), query. Filter project translation memories by target language.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTransMemoryListDtoV3
        """
        endpoint = f"/api2/v3/projects/{projectUid}/transMemories"
        params = {"targetLang": targetLang, "wfStepUid": wfStepUid}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTransMemoryListDtoV3(**r)

    def setProjectTransMemoriesV3(
        self,
        projectUid: str,
        body: SetProjectTransMemoriesV3Dto,
        phrase_token: Optional[str] = None,
    ) -> ProjectTransMemoryListDtoV3:
        """
        Edit translation memories
        If user wants to edit “All target languages” or "All workflow steps”,
                       but there are already varied TM settings for individual languages or steps,
                       then the user risks to overwrite these individual choices.
        :param projectUid: string (required), path.
        :param body: SetProjectTransMemoriesV3Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTransMemoryListDtoV3
        """
        endpoint = f"/api2/v3/projects/{projectUid}/transMemories"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTransMemoryListDtoV3(**r)

    def getProjectPreTranslateSettingsV4(
        self,
        projectUid: str,
        phrase_token: Optional[str] = None,
    ) -> PreTranslateSettingsV4Dto:
        """
        Get project pre-translate settings

        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PreTranslateSettingsV4Dto
        """
        endpoint = f"/api2/v4/projects/{projectUid}/preTranslateSettings"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PreTranslateSettingsV4Dto(**r)

    def updateProjectPreTranslateSettingsV4(
        self,
        projectUid: str,
        body: PreTranslateSettingsV4Dto,
        phrase_token: Optional[str] = None,
    ) -> PreTranslateSettingsV4Dto:
        """
        Update project pre-translate settings

        :param projectUid: string (required), path.
        :param body: PreTranslateSettingsV4Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PreTranslateSettingsV4Dto
        """
        endpoint = f"/api2/v4/projects/{projectUid}/preTranslateSettings"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PreTranslateSettingsV4Dto(**r)
