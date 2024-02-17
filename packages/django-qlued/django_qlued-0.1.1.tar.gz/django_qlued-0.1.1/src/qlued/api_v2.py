"""
Module that defines the user api v2 which goes through django-ninja.
"""

import json

from ninja import NinjaAPI
from ninja.responses import codes_4xx

from decouple import config

from dropbox.exceptions import ApiError, AuthError

from sqooler.schemes import (
    BackendConfigSchemaOut,
    BackendStatusSchemaOut,
    StatusMsgDict,
)

from .schemas import (
    JobSchemaWithTokenIn,
)

from .models import Token, StorageProviderDb
from .storage_providers import get_storage_provider, get_storage_provider_from_entry

from .storage_providers import get_short_backend_name


api = NinjaAPI(version="2.0.0")


@api.get(
    "{backend_name}/get_config",
    response={200: BackendConfigSchemaOut, codes_4xx: StatusMsgDict},
    tags=["Backend"],
    url_name="get_config",
)
def get_config(request, backend_name: str):
    """
    Returns the configuration of the backend. This is an API implementation of the class
    `qiskit.providers.models.BackendConfiguration`

    Args:
        request: The request object.
        backend_name: The name of the backend.

    Returns:
        The configuration of the backend.

    Raises:
        404: If the backend is not found.
    """
    # pylint: disable=W0613

    # we have to split the name into several parts by `_`. If there is only one part, then we
    # assume that the user has given the short name of the backend. If there are more parts, then
    # we assume that the user has given the full name of the backend.
    short_backend = get_short_backend_name(backend_name)
    if not short_backend:
        job_response_dict = {
            "job_id": "None",
            "status": "ERROR",
            "detail": "Unknown back-end! The string should have 1 or three parts separated by `_`!",
            "error_message": "Unknown back-end!",
        }
        return 404, job_response_dict

    storage_provider = get_storage_provider(backend_name)
    config_info = storage_provider.get_backend_dict(short_backend)
    # we have to add the URL to the backend configuration
    base_url = config("BASE_URL")

    if config_info.simulator:
        full_backend_name = f"{storage_provider.name}_{short_backend}_simulator"
    else:
        full_backend_name = f"{storage_provider.name}_{short_backend}_hardware"

    config_info.url = base_url + "/api/v2/" + full_backend_name + "/"

    return config_info


@api.get(
    "{backend_name}/get_backend_status",
    response={200: BackendStatusSchemaOut, codes_4xx: StatusMsgDict},
    tags=["Backend"],
    url_name="get_backend_status",
)
def get_backend_status(request, backend_name: str):
    """
    Returns the status of the backend. This is an API implementation of the class
    `qiskit.providers.models.BackendStatus`

    Args:
        request: The request object.
        backend_name: The name of the backend.

    Returns:
        The status of the backend.

    Raises:
        404: If the backend is not found.
    """
    # pylint: disable=W0613

    # we have to split the name into several parts by `_`. If there is only one part, then we
    # assume that the user has given the short name of the backend. If there are more parts, then
    # we assume that the user has given the full name of the backend.
    short_backend = get_short_backend_name(backend_name)
    if not short_backend:
        job_response_dict = {
            "job_id": "None",
            "status": "ERROR",
            "detail": "Unknown back-end! The string should have 1 or three parts separated by `_`!",
            "error_message": "Unknown back-end!",
        }
        return 404, job_response_dict

    try:
        storage_provider = get_storage_provider(backend_name)
    except FileNotFoundError:
        job_response_dict = {
            "job_id": "None",
            "status": "ERROR",
            "detail": "Unknown back-end! The string should have 1 or three parts separated by `_`!",
            "error_message": "Unknown back-end!",
        }
        return 404, job_response_dict
    return storage_provider.get_backend_status(short_backend)


@api.post(
    "{backend_name}/post_job",
    response={200: StatusMsgDict, codes_4xx: StatusMsgDict},
    tags=["Backend"],
    url_name="post_job",
)
def post_job(request, data: JobSchemaWithTokenIn, backend_name: str):
    """
    A view to submit the job to the backend.
    """
    # pylint: disable=R0914, W0613
    job_response_dict = {
        "job_id": "None",
        "status": "None",
        "detail": "None",
        "error_message": "None",
    }

    # first we need to validate the token and make sure that the user is allowed to submit jobs
    api_key = data.token

    try:
        token = Token.objects.get(key=api_key)
    except Token.DoesNotExist:
        job_response_dict["status"] = "ERROR"
        job_response_dict["error_message"] = "Invalid credentials!"
        job_response_dict["detail"] = "Invalid credentials!"
        return 401, job_response_dict

    username = token.user.username
    # get the proper backend name
    short_backend = get_short_backend_name(backend_name)
    # now it is time to look for the backend
    storage_provider = get_storage_provider(backend_name)
    backend_names = storage_provider.get_backends()
    if short_backend not in backend_names:
        job_response_dict["status"] = "ERROR"
        job_response_dict["detail"] = "Unknown back-end!"
        job_response_dict["error_message"] = "Unknown back-end!"
        return 404, job_response_dict

    # as the backend is known, we can now try to submit the job
    try:
        job_dict = json.loads(data.job)
    except json.decoder.JSONDecodeError:
        job_response_dict["status"] = "ERROR"
        job_response_dict["detail"] = "The encoding of your json seems not work out!"
        job_response_dict["error_message"] = (
            "The encoding of your json seems not work out!"
        )
        return 406, job_response_dict
    try:
        storage_provider = get_storage_provider(backend_name)

        # upload the job to the backend via the storage provider
        job_id = storage_provider.upload_job(
            job_dict=job_dict, display_name=short_backend, username=username
        )

        # now we upload the status json to the backend. this is the same status json
        # that is returned to the user
        job_response_dict = storage_provider.upload_status(
            display_name=short_backend,
            username=username,
            job_id=job_id,
        )
        return job_response_dict
    except (AuthError, ApiError):
        job_response_dict["status"] = "ERROR"
        job_response_dict["detail"] = "Error saving json data to database!"
        job_response_dict["error_message"] = "Error saving json data to database!"
        return 406, job_response_dict


@api.get(
    "{backend_name}/get_job_status",
    response={200: StatusMsgDict, codes_4xx: StatusMsgDict},
    tags=["Backend"],
    url_name="get_job_status",
)
def get_job_status(request, backend_name: str, job_id: str, token: str):
    """
    A view to check the job status that was previously submitted to the backend.
    """
    # pylint: disable=W0613
    job_response_dict = {
        "job_id": "None",
        "status": "None",
        "detail": "None",
        "error_message": "None",
    }
    # first we need to validate the token and make sure that the user is allowed to look for the job
    try:
        token_object = Token.objects.get(key=token)
    except Token.DoesNotExist:
        job_response_dict["status"] = "ERROR"
        job_response_dict["error_message"] = "Invalid credentials!"
        job_response_dict["detail"] = "Invalid credentials!"
        return 401, job_response_dict

    username = token_object.user.username
    storage_provider = get_storage_provider(backend_name)
    backend_names = storage_provider.get_backends()
    short_backend = get_short_backend_name(backend_name)
    if short_backend not in backend_names:
        job_response_dict["status"] = "ERROR"
        job_response_dict["detail"] = "Unknown back-end!"
        job_response_dict["error_message"] = "Unknown back-end!"
        return 404, job_response_dict

    # complicated right now
    # pylint: disable=W0702
    try:
        job_response_dict["job_id"] = job_id
    except:
        job_response_dict["status"] = "ERROR"
        job_response_dict["detail"] = "Error loading json data from input request!"
        job_response_dict["error_message"] = (
            "Error loading json data from input request!"
        )
        return 406, job_response_dict
    try:
        # now we download the status json from the backend
        # this is currently very much backend specific
        storage_provider = get_storage_provider(backend_name)

        job_response_dict = storage_provider.get_status(
            display_name=short_backend, username=username, job_id=job_id
        )

        return 200, job_response_dict
    except:
        job_response_dict["status"] = "ERROR"
        job_response_dict["detail"] = (
            "Error getting status from database. Maybe invalid JOB ID!"
        )
        job_response_dict["error_message"] = (
            "Error getting status from database. Maybe invalid JOB ID!"
        )
        return 406, job_response_dict


@api.get(
    "{backend_name}/get_job_result",
    response={200: dict, codes_4xx: StatusMsgDict},
    tags=["Backend"],
    url_name="get_job_result",
)
def get_job_result(request, backend_name: str, job_id: str, token: str):
    """
    A view to obtain the results of job that was previously submitted to the backend.
    """
    # pylint: disable=W0613, R0914, R0911
    status_msg_draft = {
        "job_id": "None",
        "status": "None",
        "detail": "None",
        "error_message": "None",
    }

    try:
        token_object = Token.objects.get(key=token)
    except Token.DoesNotExist:
        status_msg_draft["status"] = "ERROR"
        status_msg_draft["error_message"] = "Invalid credentials!"
        status_msg_draft["detail"] = "Invalid credentials!"
        return 401, status_msg_draft

    username = token_object.user.username
    short_backend = get_short_backend_name(backend_name)
    storage_provider = get_storage_provider(backend_name)
    backend_names = storage_provider.get_backends()
    if short_backend not in backend_names:
        status_msg_draft["status"] = "ERROR"
        status_msg_draft["detail"] = "Unknown back-end!"
        status_msg_draft["error_message"] = "Unknown back-end!"
        return 404, status_msg_draft

    status_msg_draft["job_id"] = job_id
    # pylint: disable=W0702
    # request the data from the queue
    try:
        status_msg_dict = storage_provider.get_status(
            display_name=short_backend, username=username, job_id=job_id
        )
        status_msg_draft = status_msg_dict.model_dump()
        if status_msg_draft["status"] != "DONE":
            return 200, status_msg_draft
    except:
        status_msg_draft["detail"] = (
            "Error getting status from database. Maybe invalid JOB ID!"
        )
        status_msg_draft["error_message"] = (
            "Error getting status from database. Maybe invalid JOB ID!"
        )
        return 406, status_msg_draft
    # and if the status is switched to done, we can also obtain the result
    try:
        result_dict = storage_provider.get_result(
            display_name=short_backend, username=username, job_id=job_id
        )

        return 200, result_dict
    except:
        status_msg_draft["detail"] = "Error getting result from database!"
        status_msg_draft["error_message"] = "Error getting result from database!"
        return 406, status_msg_draft


@api.get(
    "/backends",
    response=list[BackendConfigSchemaOut],
    tags=["Backend"],
    url_name="get_backends",
)
def list_backends(request):
    """
    Returns the list of backends, excluding any device called "dummy_" as they are test systems.
    """
    # pylint: disable=W0613, E1101

    backend_list = []

    # obtain all the available storage providers from the database
    storage_provider_entries = StorageProviderDb.objects.all()

    # now loop through them and obtain the backends
    for storage_provider_entry in storage_provider_entries:
        if not storage_provider_entry.is_active:
            continue
        storage_provider = get_storage_provider_from_entry(storage_provider_entry)

        backend_names = storage_provider.get_backends()
        for backend in backend_names:
            # for testing we created dummy devices. We should ignore them in any other cases.
            if not "dummy" in backend:
                config_dict = storage_provider.get_backend_dict(backend)
                backend_list.append(config_dict)
    return backend_list
