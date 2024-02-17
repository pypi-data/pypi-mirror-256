from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    AbstractAnalyseSettingsDto,
    CreateCustomFieldInstancesDto,
    CustomFieldInstanceDto,
    CustomFieldInstancesDto,
    EditAnalyseSettingsDto,
    EditProjectSecuritySettingsDtoV2,
    EditQASettingsDtoV2,
    FileImportSettingsCreateDto,
    FileImportSettingsDto,
    MTSettingsPerLanguageListDto,
    PageDtoCustomFieldInstanceDto,
    PageDtoProjectTemplateReference,
    PageDtoTransMemoryDto,
    PreTranslateSettingsV4Dto,
    ProjectSecuritySettingsDtoV2,
    ProjectTemplate,
    ProjectTemplateCreateActionDto,
    ProjectTemplateEditDto,
    ProjectTemplateTermBaseListDto,
    ProjectTemplateTransMemoryListDtoV3,
    ProjectTemplateTransMemoryListV2Dto,
    QASettingsDtoV2,
    SetProjectTemplateTermBaseDto,
    SetProjectTemplateTransMemoriesV2Dto,
    UpdateCustomFieldInstanceDto,
    UpdateCustomFieldInstancesDto,
)


class ProjectTemplateOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getProjectTemplateQASettings(
        self, projectTemplateUid: str, phrase_token: Optional[str] = None
    ) -> QASettingsDtoV2:
        """
        Get quality assurance settings

        :param projectTemplateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: QASettingsDtoV2
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/qaSettings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return QASettingsDtoV2(**r)

    async def setProjectTemplateQASettings(
        self,
        projectTemplateUid: str,
        body: EditQASettingsDtoV2,
        phrase_token: Optional[str] = None,
    ) -> QASettingsDtoV2:
        """
        Edit quality assurance settings

        :param projectTemplateUid: string (required), path.
        :param body: EditQASettingsDtoV2 (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: QASettingsDtoV2
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/qaSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return QASettingsDtoV2(**r)

    async def relevantTransMemories(
        self,
        projectTemplateUid: str,
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
        List project template relevant translation memories

        :param projectTemplateUid: string (required), path.
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
        endpoint = (
            f"/api2/v1/projectTemplates/{projectTemplateUid}/transMemories/relevant"
        )
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

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoTransMemoryDto(**r)

    async def getProjectTemplates(
        self,
        businessUnitName: str = None,
        costCenterName: str = None,
        costCenterId: int = None,
        subDomainName: str = None,
        domainName: str = None,
        ownerUid: str = None,
        clientName: str = None,
        clientId: int = None,
        name: str = None,
        sort: str = "dateCreated",
        direction: str = "desc",
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoProjectTemplateReference:
        """
                List project templates
                API call to list [project templates](https://support.phrase.com/hc/en-us/articles/5709647439772-Project-Templates-TMS-).

        Use the query parameters below to refine your search criteria for project templates:

        - **name** - The full project template name or a portion of it. For example, using `name=GUI` or `name=02`
        will locate project templates named `GUI02`.
        - **clientId** - The client's ID within the system, not interchangeable with its UID.
        - **clientName** - The complete or partial name of the client. For instance, using `clientName=GUI` or `clientName=02`
        will find project templates associated with the client `GUI02`.
        - **ownerUid** - The user UID who owns the project template within the system, interchangeable with its ID.
        - **domainName** - The complete or partial name of the domain. Using `domainName=GUI` or `domainName=02` will find
        project templates associated with the domain `GUI02`.
        - **subDomainName** - The complete or partial name of the subdomain. For instance, using `subDomainName=GUI` or
        `subDomainName=02` will locate project templates linked to the subdomain `GUI02`.
        - **costCenterId** - The cost center's ID within the system, not interchangeable with its UID.
        - **costCenterName** - The complete or partial name of the cost center. For example, using `costCenterName=GUI` or
        `costCenterName=02` will find project templates associated with the cost center `GUI02`.
        - **businessUnitName** - The complete or partial name of the business unit. For instance, using `businessUnitName=GUI`
        or `businessUnitName=02` will locate project templates linked to the business unit `GUI02`.
        - **sort** - Determines if the resulting list of project templates should be sorted by their names or the date they
        were created. This field supports either `dateCreated` or `templateName` as values.
        - **direction** - Indicates the sorting order for the resulting list by using either `asc` (ascending) or `desc`
        (descending) values.
        - **pageNumber** - Indicates the desired page number (zero-based) to retrieve. The total number of pages is returned in
        the `totalPages` field within each response.
        - **pageSize** - Indicates the page size, affecting the `totalPages` retrieved in each response and potentially
        impacting the number of iterations needed to obtain all project templates.
                :param businessUnitName: string (optional), query.
                :param costCenterName: string (optional), query.
                :param costCenterId: integer (optional), query.
                :param subDomainName: string (optional), query.
                :param domainName: string (optional), query.
                :param ownerUid: string (optional), query.
                :param clientName: string (optional), query.
                :param clientId: integer (optional), query.
                :param name: string (optional), query.
                :param sort: string (optional), query.
                :param direction: string (optional), query.
                :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
                :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: PageDtoProjectTemplateReference
        """
        endpoint = "/api2/v1/projectTemplates"
        params = {
            "name": name,
            "clientId": clientId,
            "clientName": clientName,
            "ownerUid": ownerUid,
            "domainName": domainName,
            "subDomainName": subDomainName,
            "costCenterId": costCenterId,
            "costCenterName": costCenterName,
            "businessUnitName": businessUnitName,
            "sort": sort,
            "direction": direction,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoProjectTemplateReference(**r)

    async def createProjectTemplate(
        self, body: ProjectTemplateCreateActionDto, phrase_token: Optional[str] = None
    ) -> ProjectTemplate:
        """
        Create project template

        :param body: ProjectTemplateCreateActionDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTemplate
        """
        endpoint = "/api2/v1/projectTemplates"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTemplate(**r)

    async def getProjectTemplate(
        self, projectTemplateUid: str, phrase_token: Optional[str] = None
    ) -> ProjectTemplate:
        """
        Get project template
        Note: importSettings in response is deprecated and will be always null
        :param projectTemplateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTemplate
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTemplate(**r)

    async def editProjectTemplate(
        self,
        projectTemplateUid: str,
        body: ProjectTemplateEditDto,
        phrase_token: Optional[str] = None,
    ) -> ProjectTemplate:
        """
        Edit project template

        :param projectTemplateUid: string (required), path.
        :param body: ProjectTemplateEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTemplate
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTemplate(**r)

    async def deleteProjectTemplate(
        self, projectTemplateUid: str, phrase_token: Optional[str] = None
    ) -> None:
        """
        Delete project template

        :param projectTemplateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def getAnalyseSettingsForProjectTemplate(
        self, projectTemplateUid: str, phrase_token: Optional[str] = None
    ) -> AbstractAnalyseSettingsDto:
        """
        Get analyse settings

        :param projectTemplateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AbstractAnalyseSettingsDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/analyseSettings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AbstractAnalyseSettingsDto(**r)

    async def updateAnalyseSettingsForProjectTemplate(
        self,
        projectTemplateUid: str,
        body: EditAnalyseSettingsDto,
        phrase_token: Optional[str] = None,
    ) -> AbstractAnalyseSettingsDto:
        """
        Edit analyse settings

        :param projectTemplateUid: string (required), path.
        :param body: EditAnalyseSettingsDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AbstractAnalyseSettingsDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/analyseSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AbstractAnalyseSettingsDto(**r)

    async def getImportSettingsForProjectTemplate(
        self, projectTemplateUid: str, phrase_token: Optional[str] = None
    ) -> FileImportSettingsDto:
        """
        Get import settings

        :param projectTemplateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: FileImportSettingsDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/importSettings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return FileImportSettingsDto(**r)

    async def editProjectTemplateImportSettings(
        self,
        projectTemplateUid: str,
        body: FileImportSettingsCreateDto,
        phrase_token: Optional[str] = None,
    ) -> FileImportSettingsDto:
        """
        Edit project template import settings

        :param projectTemplateUid: string (required), path.
        :param body: FileImportSettingsCreateDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: FileImportSettingsDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/importSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return FileImportSettingsDto(**r)

    async def getMachineTranslateSettingsForProjectTemplate(
        self, projectTemplateUid: str, phrase_token: Optional[str] = None
    ) -> MTSettingsPerLanguageListDto:
        """
        Get project template machine translate settings

        :param projectTemplateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: MTSettingsPerLanguageListDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/mtSettings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return MTSettingsPerLanguageListDto(**r)

    async def getProjectTemplateTermBases(
        self, projectTemplateUid: str, phrase_token: Optional[str] = None
    ) -> ProjectTemplateTermBaseListDto:
        """
        Get term bases

        :param projectTemplateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTemplateTermBaseListDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/termBases"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTemplateTermBaseListDto(**r)

    async def setProjectTemplateTermBases(
        self,
        projectTemplateUid: str,
        body: SetProjectTemplateTermBaseDto,
        phrase_token: Optional[str] = None,
    ) -> ProjectTemplateTermBaseListDto:
        """
        Edit term bases in project template

        :param projectTemplateUid: string (required), path.
        :param body: SetProjectTemplateTermBaseDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTemplateTermBaseListDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/termBases"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTemplateTermBaseListDto(**r)

    async def getProjectTemplateAccessSettings(
        self, projectTemplateUid: str, phrase_token: Optional[str] = None
    ) -> ProjectSecuritySettingsDtoV2:
        """
        Get project template access and security settings

        :param projectTemplateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectSecuritySettingsDtoV2
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/accessSettings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectSecuritySettingsDtoV2(**r)

    async def editProjectTemplateAccessSettings(
        self,
        projectTemplateUid: str,
        body: EditProjectSecuritySettingsDtoV2,
        phrase_token: Optional[str] = None,
    ) -> ProjectSecuritySettingsDtoV2:
        """
        Edit project template access and security settings

        :param projectTemplateUid: string (required), path.
        :param body: EditProjectSecuritySettingsDtoV2 (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectSecuritySettingsDtoV2
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/accessSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectSecuritySettingsDtoV2(**r)

    async def getCustomFieldsPage_1(
        self,
        projectTemplateUid: str,
        sortField: str = None,
        modifiedBy: List[str] = None,
        createdBy: List[str] = None,
        pageNumber: int = "0",
        pageSize: int = "20",
        sortTrend: str = "ASC",
        phrase_token: Optional[str] = None,
    ) -> PageDtoCustomFieldInstanceDto:
        """
        Get custom fields of project template (page)

        :param projectTemplateUid: string (required), path.
        :param sortField: string (optional), query. Sort by this field.
        :param modifiedBy: array (optional), query. Filter by webhook updaters UIDs.
        :param createdBy: array (optional), query. Filter by webhook creators UIDs.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 20.
        :param sortTrend: string (optional), query. Sort direction.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoCustomFieldInstanceDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/customFields"
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

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoCustomFieldInstanceDto(**r)

    async def createCustomFields_1(
        self,
        projectTemplateUid: str,
        body: CreateCustomFieldInstancesDto,
        phrase_token: Optional[str] = None,
    ) -> CustomFieldInstancesDto:
        """
        Create custom field instances

        :param projectTemplateUid: string (required), path.
        :param body: CreateCustomFieldInstancesDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: CustomFieldInstancesDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/customFields"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return CustomFieldInstancesDto(**r)

    async def editCustomFields_1(
        self,
        projectTemplateUid: str,
        body: UpdateCustomFieldInstancesDto,
        phrase_token: Optional[str] = None,
    ) -> CustomFieldInstancesDto:
        """
        Edit custom fields of the project template (batch)

        :param projectTemplateUid: string (required), path.
        :param body: UpdateCustomFieldInstancesDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: CustomFieldInstancesDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/customFields"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return CustomFieldInstancesDto(**r)

    async def getCustomField_2(
        self,
        fieldInstanceUid: str,
        projectTemplateUid: str,
        phrase_token: Optional[str] = None,
    ) -> CustomFieldInstanceDto:
        """
        Get custom field of project template

        :param fieldInstanceUid: string (required), path.
        :param projectTemplateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: CustomFieldInstanceDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/customFields/{fieldInstanceUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return CustomFieldInstanceDto(**r)

    async def editCustomField_1(
        self,
        fieldInstanceUid: str,
        projectTemplateUid: str,
        body: UpdateCustomFieldInstanceDto,
        phrase_token: Optional[str] = None,
    ) -> CustomFieldInstanceDto:
        """
        Edit custom field of project template

        :param fieldInstanceUid: string (required), path.
        :param projectTemplateUid: string (required), path.
        :param body: UpdateCustomFieldInstanceDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: CustomFieldInstanceDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/customFields/{fieldInstanceUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return CustomFieldInstanceDto(**r)

    async def deleteCustomField_2(
        self,
        fieldInstanceUid: str,
        projectTemplateUid: str,
        phrase_token: Optional[str] = None,
    ) -> dict:
        """
        Delete custom field of project template

        :param fieldInstanceUid: string (required), path.
        :param projectTemplateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return:
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/customFields/{fieldInstanceUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    async def setProjectTemplateTransMemoriesV2(
        self,
        projectTemplateUid: str,
        body: SetProjectTemplateTransMemoriesV2Dto,
        phrase_token: Optional[str] = None,
    ) -> ProjectTemplateTransMemoryListV2Dto:
        """
        Edit translation memories
        If user wants to edit “All target languages” or "All workflow steps”,
                       but there are already varied TM settings for individual languages or steps,
                       then the user risks to overwrite these individual choices.
        :param projectTemplateUid: string (required), path.
        :param body: SetProjectTemplateTransMemoriesV2Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTemplateTransMemoryListV2Dto
        """
        endpoint = f"/api2/v2/projectTemplates/{projectTemplateUid}/transMemories"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTemplateTransMemoryListV2Dto(**r)

    async def getProjectTemplateTransMemories_2(
        self,
        projectTemplateUid: str,
        wfStepUid: str = None,
        targetLang: str = None,
        phrase_token: Optional[str] = None,
    ) -> ProjectTemplateTransMemoryListDtoV3:
        """
        Get translation memories

        :param projectTemplateUid: string (required), path.
        :param wfStepUid: string (optional), query. Filter project translation memories by workflow step.
        :param targetLang: string (optional), query. Filter project translation memories by target language.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectTemplateTransMemoryListDtoV3
        """
        endpoint = f"/api2/v3/projectTemplates/{projectTemplateUid}/transMemories"
        params = {"targetLang": targetLang, "wfStepUid": wfStepUid}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectTemplateTransMemoryListDtoV3(**r)

    async def getProjectTemplatePreTranslateSettingsV4(
        self, projectTemplateUid: str, phrase_token: Optional[str] = None
    ) -> PreTranslateSettingsV4Dto:
        """
        Get project template pre-translate settings

        :param projectTemplateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PreTranslateSettingsV4Dto
        """
        endpoint = (
            f"/api2/v4/projectTemplates/{projectTemplateUid}/preTranslateSettings"
        )
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PreTranslateSettingsV4Dto(**r)

    async def updateProjectTemplatePreTranslateSettingsV4(
        self,
        projectTemplateUid: str,
        body: PreTranslateSettingsV4Dto,
        phrase_token: Optional[str] = None,
    ) -> PreTranslateSettingsV4Dto:
        """
        Update project template pre-translate settings

        :param projectTemplateUid: string (required), path.
        :param body: PreTranslateSettingsV4Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PreTranslateSettingsV4Dto
        """
        endpoint = (
            f"/api2/v4/projectTemplates/{projectTemplateUid}/preTranslateSettings"
        )
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PreTranslateSettingsV4Dto(**r)
