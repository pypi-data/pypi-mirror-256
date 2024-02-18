import requests

from ergondata_executions.v1.auth.controller import AuthController
from ergondata_executions.v1.worker.interfaces import *
from ergondata_executions.v1.decorators import *


class WorkerController:

    CREATE_WORKER_URL = "processes/{0}/workers"
    GET_WORKERS_URL = "processes/{0}/workers"
    DELETE_WORKER_URL = "processes/{0}/workers/{1}"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    @api_request(log_message="Creating worker", out_schema=CreateWorkerResponsePayload)
    def create_worker(self, process_id: StrictStr, friendly_name: StrictStr) -> CreateWorkerResponsePayload:
        res: Any = requests.post(
            url=f"{self.api_client.ROOT_URL}{self.CREATE_WORKER_URL.format(process_id)}",
            json={"first_name": friendly_name},
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Deleting worker", out_schema=DeleteWorkerResponsePayload)
    def delete_worker(self, process_id: StrictStr, worker_id: StrictStr) -> DeleteWorkerResponsePayload:
        res: Any = requests.delete(
            url=f"{self.api_client.ROOT_URL}{self.DELETE_WORKER_URL.format(process_id, worker_id)}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Getting workers", out_schema=GetWorkersResponsePayload)
    def get_workers(self, process_id: StrictStr) -> GetWorkersResponsePayload:
        res: Any = requests.get(
            url=f"{self.api_client.ROOT_URL}{self.GET_WORKERS_URL.format(process_id)}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res
