#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from os import environ

import pytest

from ibm_watson_machine_learning import APIClient
from ibm_watson_machine_learning.tests.utils import get_wml_credentials, get_cos_credentials
from ibm_watson_machine_learning.tests.foundation_models.tests_steps.data_storage import DataStorage
from ibm_watson_machine_learning.tests.foundation_models.tests_steps.prompt_tuning_steps import PromptTuningSteps
from ibm_watson_machine_learning.tests.foundation_models.tests_steps.universal_steps import UniversalSteps
from ibm_watson_machine_learning.tests.foundation_models.tests_steps.prompt_template_steps import PromptTemplateSteps

pytest_plugins = [
    "ibm_watson_machine_learning.tests.foundation_models.conftest_foundation_models"
]


def pytest_collection_modifyitems(items):
    """
    Because UnitTest do not like to cooperate with fixtures other than with param `autouse=True`
    there is a need to enumerate test BY MODEL and then ALPHANUMERICAL, which this function does.
    """
    for i, item in enumerate(items):
        if 'foundation_models' in item.nodeid:
            timeout = 35 * 60 if 'prompt_tuning' in item.name else 2 * 60  # 35 minutes for prompt tuning, 2 mins for other tests
            item.add_marker(pytest.mark.timeout(timeout))


@pytest.fixture(scope="session", name="credentials")
def fixture_credentials():
    """
    Fixture responsible for getting credentials from `config.ini` file
        return:
            dict: Credentials for WML
    """
    credentials = get_wml_credentials()
    return credentials


@pytest.fixture(scope="session", name="project_id")
def fixture_project_id(credentials):
    """
    Fixture responsible for returning project ID
        Args:
            credentials:

        return:
            str: Project ID
    """
    project_id = credentials.get('project_id')
    return project_id


@pytest.fixture(scope="session", name="space_id")
def fixture_space_id(credentials):
    """
    Fixture responsible for returning space ID
        Args:
            credentials:

        return:
            str: Space ID
    """
    space_id = credentials.get('space_id')
    return space_id


@pytest.fixture(scope="session", name="api_client")
def fixture_api_client(credentials):
    """
    Fixture responsible for setup API Client with given credentials.
        Args:
            credentials:

        return:
            APIClient Object:
    """
    api_client = APIClient(credentials)
    return api_client


@pytest.fixture(scope="session", name="cos_credentials")
def fixture_cos_credentials():
    """
    Fixture responsible for getting COS credentials
        return:
            dict: COS Credentials
    """
    cos_credentials = get_cos_credentials()
    return cos_credentials


@pytest.fixture(scope="session", name="cos_endpoint")
def fixture_cos_endpoint(cos_credentials):
    """
    Fixture responsible for getting COS endpoint.
        Args:
            cos_credentials:

        return:
            str: COS Endpoint
    """
    cos_endpoint = cos_credentials['endpoint_url']
    return cos_endpoint


@pytest.fixture(scope="session", name="cos_resource_instance_id")
def fixture_cos_resource_instance_id(cos_credentials):
    """
    Fixture responsible for getting COS Instance ID from cos_credentials part of config.ini file
        Args:
            cos_credentials:

        return:
            str: COS resource instance ID
    """
    cos_resource_instance_id = cos_credentials['resource_instance_id']
    return cos_resource_instance_id


space_name = environ.get('SPACE_NAME', 'regression_tests_sdk_space')


# @pytest.fixture(name="space_cleanup")
# def fixture_space_clean_up(api_client, cos_resource_instance_id, project_id, request):
#     print('cleanUP')
#     space_checked = False
#     while not space_checked:
#         space_cleanup(api_client,
#                       get_space_id(api_client, space_name,
#                                    cos_resource_instance_id=cos_resource_instance_id),
#                       days_old=7)
#         space_id = get_space_id(api_client, space_name,
#                                 cos_resource_instance_id=cos_resource_instance_id)
#         try:
#             assert space_id is not None, "space_id is None"
#             api_client.spaces.get_details(space_id)
#             space_checked = True
#         except AssertionError or ApiRequestFailure:
#             space_checked = False
#
#     request.cls.space_id = space_id
#
#     print('cleanUP x 2')
#
#     if request.cls.SPACE_ONLY:
#         api_client.set.default_space(space_id)
#     else:
#         api_client.set.default_project(project_id)


@pytest.fixture(scope="function", name="data_storage")
def fixture_data_storage_init():
    return DataStorage()


@pytest.fixture(scope="function", name="universal_step")
def fixture_universal_step_init(data_storage):
    return UniversalSteps(data_storage)


@pytest.fixture(scope="function", name="prompt_tuning_step")
def fixture_prompt_tuning_step_init(data_storage):
    return PromptTuningSteps(data_storage)


@pytest.fixture(scope="function", name="prompt_template_step")
def fixture_prompt_template_step_init(data_storage):
    return PromptTemplateSteps(data_storage)
