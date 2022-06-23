import time
from locust import HttpUser, task, between


class NimbusUser(HttpUser):
    # TODO Randomize request interval?
    # TODO Weight the tasks (requests)? (i.e. should one request occur more frequently than another)
    # TODO Should we add a config file with things like log levels
    # TODO Add environment variable for slug?
    # TODO Update Make file?
    # TODO Update README or other documentation?

    wait_time = between(30, 60)

    @task
    def query_landing_page(self):
        endpoint = "/api/v5/graphql"
        body = {
            "operationName": "getAllExperiments",
            "variables": {},
            "query": "query getAllExperiments { experiments { isArchived name owner { username __typename } "
                     "featureConfigs { id slug name description application ownerEmail schema __typename } slug "
                     "application firefoxMinVersion firefoxMaxVersion startDate isEnrollmentPausePending "
                     "isEnrollmentPaused proposedDuration proposedEnrollment computedEndDate status statusNext "
                     "publishStatus monitoringDashboardUrl resultsReady featureConfig { slug name __typename } "
                     "__typename } } "
        }

        with self.client.get(endpoint, verify=False, catch_response=True, json=body) as response:
            print("RESPONSE:" + response.text)

        time.sleep(30)

    @task
    def query_detail_page(self):
        endpoint = "/api/v5/graphql"
        body = {
            "operationName": "getExperiment",
            "variables": {
                "slug": "multi-layered-well-modulated-functionalities",
            },
            "query": "query getExperiment($slug: String!) { experimentBySlug(slug: $slug) { id isRollout isArchived "
                     "canEdit canArchive name slug status statusNext publishStatus monitoringDashboardUrl "
                     "resultsReady hypothesis application publicDescription conclusionRecommendation takeawaysSummary "
                     "owner { email __typename } parent { name slug __typename } warnFeatureSchema referenceBranch { "
                     "id name slug description ratio featureValue featureEnabled screenshots { id description image "
                     "__typename } __typename } treatmentBranches { id name slug description ratio featureValue "
                     "featureEnabled screenshots { id description image __typename } __typename } featureConfigs { id "
                     "slug name description application ownerEmail schema __typename } primaryOutcomes "
                     "secondaryOutcomes channel firefoxMinVersion firefoxMaxVersion targetingConfigSlug "
                     "jexlTargetingExpression populationPercent totalEnrolledClients proposedEnrollment "
                     "proposedDuration readyForReview { ready message warnings __typename } startDate computedEndDate "
                     "computedEnrollmentDays computedDurationDays riskMitigationLink riskRevenue riskBrand "
                     "riskPartnerRelated signoffRecommendations { qaSignoff vpSignoff legalSignoff __typename } "
                     "documentationLinks { title link __typename } isEnrollmentPausePending isEnrollmentPaused "
                     "enrollmentEndDate canReview reviewRequest { changedOn changedBy { email __typename } __typename "
                     "} rejection { message oldStatus oldStatusNext changedOn changedBy { email __typename } "
                     "__typename } timeout { changedOn changedBy { email __typename } __typename } recipeJson "
                     "reviewUrl locales { id name __typename } countries { id name __typename } __typename } } "
        }

        with self.client.get(endpoint, verify=False, catch_response=True, json=body) as response:
            print("RESPONSE:" + response.text)

        time.sleep(30)
