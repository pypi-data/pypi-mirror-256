from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuthReq(_message.Message):
    __slots__ = ("username", "password", "database", "schema")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    database: str
    schema: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ..., database: _Optional[str] = ..., schema: _Optional[str] = ...) -> None: ...

class AuthCtx(_message.Message):
    __slots__ = ("database", "schema", "token", "token_system_version")
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_SYSTEM_VERSION_FIELD_NUMBER: _ClassVar[int]
    database: str
    schema: str
    token: str
    token_system_version: int
    def __init__(self, database: _Optional[str] = ..., schema: _Optional[str] = ..., token: _Optional[str] = ..., token_system_version: _Optional[int] = ...) -> None: ...

class SqlRequest(_message.Message):
    __slots__ = ("request_id", "auth", "query", "numeric", "named")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    AUTH_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    NUMERIC_FIELD_NUMBER: _ClassVar[int]
    NAMED_FIELD_NUMBER: _ClassVar[int]
    request_id: int
    auth: AuthCtx
    query: str
    numeric: NumericQueryPlaceholder
    named: NamedQueryPlaceHolder
    def __init__(self, request_id: _Optional[int] = ..., auth: _Optional[_Union[AuthCtx, _Mapping]] = ..., query: _Optional[str] = ..., numeric: _Optional[_Union[NumericQueryPlaceholder, _Mapping]] = ..., named: _Optional[_Union[NamedQueryPlaceHolder, _Mapping]] = ...) -> None: ...

class PlaceholderValue(_message.Message):
    __slots__ = ("i32_t", "i64_t", "float_t", "double_t", "bool_t", "str_t", "binary_t", "timestamp_millis")
    I32_T_FIELD_NUMBER: _ClassVar[int]
    I64_T_FIELD_NUMBER: _ClassVar[int]
    FLOAT_T_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_T_FIELD_NUMBER: _ClassVar[int]
    BOOL_T_FIELD_NUMBER: _ClassVar[int]
    STR_T_FIELD_NUMBER: _ClassVar[int]
    BINARY_T_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_MILLIS_FIELD_NUMBER: _ClassVar[int]
    i32_t: int
    i64_t: int
    float_t: float
    double_t: float
    bool_t: bool
    str_t: str
    binary_t: bytes
    timestamp_millis: int
    def __init__(self, i32_t: _Optional[int] = ..., i64_t: _Optional[int] = ..., float_t: _Optional[float] = ..., double_t: _Optional[float] = ..., bool_t: bool = ..., str_t: _Optional[str] = ..., binary_t: _Optional[bytes] = ..., timestamp_millis: _Optional[int] = ...) -> None: ...

class NumericQueryPlaceholder(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _containers.RepeatedCompositeFieldContainer[PlaceholderValue]
    def __init__(self, value: _Optional[_Iterable[_Union[PlaceholderValue, _Mapping]]] = ...) -> None: ...

class PlaceholderPair(_message.Message):
    __slots__ = ("name", "value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: PlaceholderValue
    def __init__(self, name: _Optional[str] = ..., value: _Optional[_Union[PlaceholderValue, _Mapping]] = ...) -> None: ...

class NamedQueryPlaceHolder(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[PlaceholderPair]
    def __init__(self, values: _Optional[_Iterable[_Union[PlaceholderPair, _Mapping]]] = ...) -> None: ...

class SqlResponse(_message.Message):
    __slots__ = ("request_id", "response", "error")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    request_id: int
    response: str
    error: SqlResponseError
    def __init__(self, request_id: _Optional[int] = ..., response: _Optional[str] = ..., error: _Optional[_Union[SqlResponseError, _Mapping]] = ...) -> None: ...

class SqlResponseError(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: int
    message: str
    def __init__(self, code: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...
