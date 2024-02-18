from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DefectType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    ELECTRICITY: _ClassVar[DefectType]
    PLUMB: _ClassVar[DefectType]
    COMMON: _ClassVar[DefectType]

class DefectStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    CREATED: _ClassVar[DefectStatus]
    ACCEPTED: _ClassVar[DefectStatus]
    RESOLVED: _ClassVar[DefectStatus]
ELECTRICITY: DefectType
PLUMB: DefectType
COMMON: DefectType
CREATED: DefectStatus
ACCEPTED: DefectStatus
RESOLVED: DefectStatus

class DormybobaRole(_message.Message):
    __slots__ = ["role_id", "role_name"]
    ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    role_id: int
    role_name: str
    def __init__(self, role_id: _Optional[int] = ..., role_name: _Optional[str] = ...) -> None: ...

class Institute(_message.Message):
    __slots__ = ["institute_id", "institute_name"]
    INSTITUTE_ID_FIELD_NUMBER: _ClassVar[int]
    INSTITUTE_NAME_FIELD_NUMBER: _ClassVar[int]
    institute_id: int
    institute_name: str
    def __init__(self, institute_id: _Optional[int] = ..., institute_name: _Optional[str] = ...) -> None: ...

class AcademicType(_message.Message):
    __slots__ = ["type_id", "type_name"]
    TYPE_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    type_id: int
    type_name: str
    def __init__(self, type_id: _Optional[int] = ..., type_name: _Optional[str] = ...) -> None: ...

class GenerateVerificationCodeRequest(_message.Message):
    __slots__ = ["role_name"]
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    role_name: str
    def __init__(self, role_name: _Optional[str] = ...) -> None: ...

class GenerateVerificationCodeResponse(_message.Message):
    __slots__ = ["verification_code"]
    VERIFICATION_CODE_FIELD_NUMBER: _ClassVar[int]
    verification_code: int
    def __init__(self, verification_code: _Optional[int] = ...) -> None: ...

class GetRoleByVerificationCodeRequest(_message.Message):
    __slots__ = ["verification_code"]
    VERIFICATION_CODE_FIELD_NUMBER: _ClassVar[int]
    verification_code: int
    def __init__(self, verification_code: _Optional[int] = ...) -> None: ...

class GetRoleByVerificationCodeResponse(_message.Message):
    __slots__ = ["role"]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role: DormybobaRole
    def __init__(self, role: _Optional[_Union[DormybobaRole, _Mapping]] = ...) -> None: ...

class DormybobaUser(_message.Message):
    __slots__ = ["user_id", "institute", "role", "academic_type", "year", "group"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTITUTE_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    ACADEMIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    institute: Institute
    role: DormybobaRole
    academic_type: AcademicType
    year: int
    group: str
    def __init__(self, user_id: _Optional[int] = ..., institute: _Optional[_Union[Institute, _Mapping]] = ..., role: _Optional[_Union[DormybobaRole, _Mapping]] = ..., academic_type: _Optional[_Union[AcademicType, _Mapping]] = ..., year: _Optional[int] = ..., group: _Optional[str] = ...) -> None: ...

class CreateUserRequest(_message.Message):
    __slots__ = ["user", "verification_code"]
    USER_FIELD_NUMBER: _ClassVar[int]
    VERIFICATION_CODE_FIELD_NUMBER: _ClassVar[int]
    user: DormybobaUser
    verification_code: int
    def __init__(self, user: _Optional[_Union[DormybobaUser, _Mapping]] = ..., verification_code: _Optional[int] = ...) -> None: ...

class CreateUserResponse(_message.Message):
    __slots__ = ["user"]
    USER_FIELD_NUMBER: _ClassVar[int]
    user: DormybobaUser
    def __init__(self, user: _Optional[_Union[DormybobaUser, _Mapping]] = ...) -> None: ...

class GetUserByIdRequest(_message.Message):
    __slots__ = ["user_id"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    def __init__(self, user_id: _Optional[int] = ...) -> None: ...

class GetUserByIdResponse(_message.Message):
    __slots__ = ["user"]
    USER_FIELD_NUMBER: _ClassVar[int]
    user: DormybobaUser
    def __init__(self, user: _Optional[_Union[DormybobaUser, _Mapping]] = ...) -> None: ...

class GetAllInstitutesResponse(_message.Message):
    __slots__ = ["institutes"]
    INSTITUTES_FIELD_NUMBER: _ClassVar[int]
    institutes: _containers.RepeatedCompositeFieldContainer[Institute]
    def __init__(self, institutes: _Optional[_Iterable[_Union[Institute, _Mapping]]] = ...) -> None: ...

class GetInstituteByNameRequest(_message.Message):
    __slots__ = ["institute_name"]
    INSTITUTE_NAME_FIELD_NUMBER: _ClassVar[int]
    institute_name: str
    def __init__(self, institute_name: _Optional[str] = ...) -> None: ...

class GetInstituteByNameResponse(_message.Message):
    __slots__ = ["institute"]
    INSTITUTE_FIELD_NUMBER: _ClassVar[int]
    institute: Institute
    def __init__(self, institute: _Optional[_Union[Institute, _Mapping]] = ...) -> None: ...

class GetAllAcademicTypesResponse(_message.Message):
    __slots__ = ["academic_types"]
    ACADEMIC_TYPES_FIELD_NUMBER: _ClassVar[int]
    academic_types: _containers.RepeatedCompositeFieldContainer[AcademicType]
    def __init__(self, academic_types: _Optional[_Iterable[_Union[AcademicType, _Mapping]]] = ...) -> None: ...

class GetAcademicTypeByNameRequest(_message.Message):
    __slots__ = ["type_name"]
    TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    type_name: str
    def __init__(self, type_name: _Optional[str] = ...) -> None: ...

class GetAcademicTypeByNameResponse(_message.Message):
    __slots__ = ["academic_type"]
    ACADEMIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    academic_type: AcademicType
    def __init__(self, academic_type: _Optional[_Union[AcademicType, _Mapping]] = ...) -> None: ...

class Mailing(_message.Message):
    __slots__ = ["mailing_id", "theme", "mailing_text", "at", "institute_id", "academic_type_id", "year"]
    MAILING_ID_FIELD_NUMBER: _ClassVar[int]
    THEME_FIELD_NUMBER: _ClassVar[int]
    MAILING_TEXT_FIELD_NUMBER: _ClassVar[int]
    AT_FIELD_NUMBER: _ClassVar[int]
    INSTITUTE_ID_FIELD_NUMBER: _ClassVar[int]
    ACADEMIC_TYPE_ID_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    mailing_id: int
    theme: str
    mailing_text: str
    at: _timestamp_pb2.Timestamp
    institute_id: int
    academic_type_id: int
    year: int
    def __init__(self, mailing_id: _Optional[int] = ..., theme: _Optional[str] = ..., mailing_text: _Optional[str] = ..., at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., institute_id: _Optional[int] = ..., academic_type_id: _Optional[int] = ..., year: _Optional[int] = ...) -> None: ...

class CreateMailingRequest(_message.Message):
    __slots__ = ["mailing"]
    MAILING_FIELD_NUMBER: _ClassVar[int]
    mailing: Mailing
    def __init__(self, mailing: _Optional[_Union[Mailing, _Mapping]] = ...) -> None: ...

class CreateMailingResponse(_message.Message):
    __slots__ = ["mailing"]
    MAILING_FIELD_NUMBER: _ClassVar[int]
    mailing: Mailing
    def __init__(self, mailing: _Optional[_Union[Mailing, _Mapping]] = ...) -> None: ...

class Queue(_message.Message):
    __slots__ = ["queue_id", "title", "description", "open", "close"]
    QUEUE_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OPEN_FIELD_NUMBER: _ClassVar[int]
    CLOSE_FIELD_NUMBER: _ClassVar[int]
    queue_id: int
    title: str
    description: str
    open: _timestamp_pb2.Timestamp
    close: _timestamp_pb2.Timestamp
    def __init__(self, queue_id: _Optional[int] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., open: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., close: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CreateQueueRequest(_message.Message):
    __slots__ = ["queue"]
    QUEUE_FIELD_NUMBER: _ClassVar[int]
    queue: Queue
    def __init__(self, queue: _Optional[_Union[Queue, _Mapping]] = ...) -> None: ...

class CreateQueueResponse(_message.Message):
    __slots__ = ["queue"]
    QUEUE_FIELD_NUMBER: _ClassVar[int]
    queue: Queue
    def __init__(self, queue: _Optional[_Union[Queue, _Mapping]] = ...) -> None: ...

class AddPersonToQueueRequest(_message.Message):
    __slots__ = ["queue_id", "user_id"]
    QUEUE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    queue_id: int
    user_id: int
    def __init__(self, queue_id: _Optional[int] = ..., user_id: _Optional[int] = ...) -> None: ...

class AddPersonToQueueResponse(_message.Message):
    __slots__ = ["is_active"]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    is_active: bool
    def __init__(self, is_active: bool = ...) -> None: ...

class RemovePersonFromQueueRequest(_message.Message):
    __slots__ = ["queue_id", "user_id"]
    QUEUE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    queue_id: int
    user_id: int
    def __init__(self, queue_id: _Optional[int] = ..., user_id: _Optional[int] = ...) -> None: ...

class PersonCompleteQueueRequest(_message.Message):
    __slots__ = ["queue_id", "user_id"]
    QUEUE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    queue_id: int
    user_id: int
    def __init__(self, queue_id: _Optional[int] = ..., user_id: _Optional[int] = ...) -> None: ...

class PersonCompleteQueueResponse(_message.Message):
    __slots__ = ["is_queue_empty", "active_user_id"]
    IS_QUEUE_EMPTY_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_USER_ID_FIELD_NUMBER: _ClassVar[int]
    is_queue_empty: bool
    active_user_id: int
    def __init__(self, is_queue_empty: bool = ..., active_user_id: _Optional[int] = ...) -> None: ...

class Defect(_message.Message):
    __slots__ = ["defect_id", "user_id", "defect_type", "description", "defect_status"]
    DEFECT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    DEFECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DEFECT_STATUS_FIELD_NUMBER: _ClassVar[int]
    defect_id: str
    user_id: int
    defect_type: DefectType
    description: str
    defect_status: DefectStatus
    def __init__(self, defect_id: _Optional[str] = ..., user_id: _Optional[int] = ..., defect_type: _Optional[_Union[DefectType, str]] = ..., description: _Optional[str] = ..., defect_status: _Optional[_Union[DefectStatus, str]] = ...) -> None: ...

class CreateDefectRequest(_message.Message):
    __slots__ = ["defect"]
    DEFECT_FIELD_NUMBER: _ClassVar[int]
    defect: Defect
    def __init__(self, defect: _Optional[_Union[Defect, _Mapping]] = ...) -> None: ...

class CreateDefectResponse(_message.Message):
    __slots__ = ["defect"]
    DEFECT_FIELD_NUMBER: _ClassVar[int]
    defect: Defect
    def __init__(self, defect: _Optional[_Union[Defect, _Mapping]] = ...) -> None: ...

class GetDefectByIdRequest(_message.Message):
    __slots__ = ["defect_id"]
    DEFECT_ID_FIELD_NUMBER: _ClassVar[int]
    defect_id: str
    def __init__(self, defect_id: _Optional[str] = ...) -> None: ...

class GetDefectByIdResponse(_message.Message):
    __slots__ = ["defect"]
    DEFECT_FIELD_NUMBER: _ClassVar[int]
    defect: Defect
    def __init__(self, defect: _Optional[_Union[Defect, _Mapping]] = ...) -> None: ...

class UpdateDefectRequest(_message.Message):
    __slots__ = ["defect"]
    DEFECT_FIELD_NUMBER: _ClassVar[int]
    defect: Defect
    def __init__(self, defect: _Optional[_Union[Defect, _Mapping]] = ...) -> None: ...

class AssignDefectRequest(_message.Message):
    __slots__ = ["defect_id"]
    DEFECT_ID_FIELD_NUMBER: _ClassVar[int]
    defect_id: str
    def __init__(self, defect_id: _Optional[str] = ...) -> None: ...

class AssignDefectResponse(_message.Message):
    __slots__ = ["assigned_user_id"]
    ASSIGNED_USER_ID_FIELD_NUMBER: _ClassVar[int]
    assigned_user_id: int
    def __init__(self, assigned_user_id: _Optional[int] = ...) -> None: ...

class MailingEvent(_message.Message):
    __slots__ = ["mailing", "users"]
    MAILING_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    mailing: Mailing
    users: _containers.RepeatedCompositeFieldContainer[DormybobaUser]
    def __init__(self, mailing: _Optional[_Union[Mailing, _Mapping]] = ..., users: _Optional[_Iterable[_Union[DormybobaUser, _Mapping]]] = ...) -> None: ...

class MailingEventResponse(_message.Message):
    __slots__ = ["event"]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    event: MailingEvent
    def __init__(self, event: _Optional[_Union[MailingEvent, _Mapping]] = ...) -> None: ...

class QueueEvent(_message.Message):
    __slots__ = ["queue", "users"]
    QUEUE_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    queue: Queue
    users: _containers.RepeatedCompositeFieldContainer[DormybobaUser]
    def __init__(self, queue: _Optional[_Union[Queue, _Mapping]] = ..., users: _Optional[_Iterable[_Union[DormybobaUser, _Mapping]]] = ...) -> None: ...

class QueueEventResponse(_message.Message):
    __slots__ = ["event"]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    event: QueueEvent
    def __init__(self, event: _Optional[_Union[QueueEvent, _Mapping]] = ...) -> None: ...
