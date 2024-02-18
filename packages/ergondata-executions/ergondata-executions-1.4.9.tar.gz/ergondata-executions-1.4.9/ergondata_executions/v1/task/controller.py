import requests
from ergondata_executions.v1.auth.controller import AuthController
from ergondata_executions.v1.task.interfaces import *
from ergondata_executions.v1.decorators import *

class TaskController:

    CREATE_TASK_URL = "processes/{0}/tasks"
    GET_TASKS_URL = "processes/{0}/tasks"
    DELETE_TASK_URL = "processes/{0}/tasks/{1}"
    UPDATE_TASK_URL = "processes/{0}/tasks/{1}"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    @api_request(log_message="Creating task {name}", out_schema=CreateTaskResponsePayload)
    def create_task(
        self,
        process_id: StrictStr,
        name: StrictStr,
        description: StrictStr,
        task_type_id: Literal["dispatcher", "performer", "performer-and-dispatcher", "linear", "reporter"],
        cron_schedule_expression: StrictStr,
        timezone: StrictStr,
        cron_schedule_expression_description: StrictStr = None,
        reset_ongoing_execution: StrictBool = False,
        release_ongoing_execution: StrictBool = False,
    ) -> CreateTaskResponsePayload:
        res: Any = requests.post(
            url=f"{self.api_client.ROOT_URL}{self.CREATE_TASK_URL.format(process_id)}",
            json=CreateTaskRequestPayload(
                name=name,
                description=description,
                task_type_id=task_type_id,
                cron_schedule_expression_description=cron_schedule_expression_description,
                cron_schedule_expression=cron_schedule_expression,
                reset_ongoing_execution=reset_ongoing_execution,
                release_ongoing_execution=release_ongoing_execution,
                timezone=timezone
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Deleting task {task_id}", out_schema=DeleteTaskResponsePayload)
    def delete_task(
        self,
        process_id: StrictStr,
        task_id: StrictStr
    ) -> DeleteTaskResponsePayload:
        res: Any = requests.delete(
            url=f"{self.api_client.ROOT_URL}{self.DELETE_TASK_URL.format(process_id, task_id)}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Getting tasks", out_schema=GetTasksResponsePayload)
    def get_tasks(self, process_id: StrictStr) -> GetTasksResponsePayload:
        res: Any = requests.get(
            url=f"{self.api_client.ROOT_URL}{self.GET_TASKS_URL.format(process_id)}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Updating task {name}", out_schema=UpdateTaskResponsePayload)
    def update_task(
        self,
        task_id: StrictStr,
        process_id: StrictStr,
        name: StrictStr,
        description: StrictStr,
        task_type_id: Literal["dispatcher", "performer", "performer-and-dispatcher"],
        cron_schedule_expression: StrictStr,
        timezone: StrictStr,
        reset_ongoing_execution: StrictBool = False,
        release_ongoing_execution: StrictBool = False,
    ) -> UpdateTaskResponsePayload:
        res: Any = requests.put(
            url=f"{self.api_client.ROOT_URL}{self.UPDATE_TASK_URL.format(process_id, task_id)}",
            json=UpdateTaskRequestPayload(
                name=name,
                description=description,
                task_type_id=task_type_id,
                cron_schedule_expression=cron_schedule_expression,
                timezone=timezone,
                reset_ongoing_execution=reset_ongoing_execution,
                release_ongoing_execution=release_ongoing_execution,
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res
