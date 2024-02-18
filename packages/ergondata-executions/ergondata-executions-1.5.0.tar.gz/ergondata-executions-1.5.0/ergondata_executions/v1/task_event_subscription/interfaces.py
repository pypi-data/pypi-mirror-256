from ergondata_executions.interfaces import *
from ergondata_executions.v1.task.interfaces import Task
from pydantic import StrictFloat


class TaskHighDurationEvent(BaseModel):
    duration_metric: Literal["absolute", "mean", "median"]
    duration_value: Union[StrictInt, StrictFloat]


class TaskDelayedEvent(BaseModel):
    delay_tolerance: Union[StrictInt, StrictFloat]


class TaskEventSubscription(BaseModel):
    id: StrictStr
    event: Any
    whatsapp_integration: StrictBool
    whatsapp_recipients: Optional[Union[List[WhatsappRecipient], None]] = None
    email_integration: StrictBool
    email_recipients: Optional[Union[List[StrictStr], None]] = None
    webhook_integration: StrictBool
    webhook_url: Optional[Union[StrictStr, None]] = None
    task_exception_id: Optional[StrictStr] = None
    task: Task
    payload: Union[TaskHighDurationEvent, TaskDelayedEvent, None] = None
    created_at: datetime
    updated_at: datetime


class CreateTaskEventSubscriptionRequestPayload(BaseModel):
    event_id: StrictStr
    whatsapp_integration: StrictBool = False
    whatsapp_recipients: Optional[Union[List[WhatsappRecipient], None]] = None
    email_integration: StrictBool = False
    email_recipients: Optional[Union[List[StrictStr], None]] = None
    webhook_integration: StrictBool = False
    webhook_url: Optional[Union[StrictStr, None]] = None
    task_exception_id: Optional[StrictStr] = None
    payload: Union[TaskHighDurationEvent, TaskDelayedEvent, None] = None


class UpdateTaskEventSubscriptionRequestPayload(CreateTaskEventSubscriptionRequestPayload):
    pass


class CreateTaskEventSubscriptionResponsePayload(APIBaseResponse):
    data: Optional[TaskEventSubscription] = None


class DeleteTaskEventSubscriptionResponsePayload(APIBaseResponse):
    process_id: Optional[StrictStr] = None


class GetTaskEventSubscriptionsResponsePayload(APIBaseResponse):
    data: List[TaskEventSubscription]


class UpdateTaskEventSubscriptionResponsePayload(CreateTaskEventSubscriptionResponsePayload):
    data: Optional[TaskEventSubscription] = None

