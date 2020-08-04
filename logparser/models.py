from dataclasses import dataclass
import datetime
import typing
import enum

@dataclass(frozen=True)
class Host():
    ip: str
    port: int


@dataclass(frozen=True)
class HttpRequest:
    method: str
    url: str
    query: dict
    protocol: str

@dataclass(frozen=True, unsafe_hash=True)
class ElbLogEntity():
    type: str
    time: datetime.datetime
    elb: str
    client: Host
    target: Host
    request_processing_time: float
    target_processing_time: float
    response_processing_time: float
    elb_status_code: str
    target_status_code: str
    received_bytes: int
    sent_bytes: int
    http_request: HttpRequest
    user_agent: str
    ssl_cipher: str
    ssl_protocol: str
    target_group_arn: str
    trace_id: str
    domain_name: str
    chosen_cert_arn: str
    matched_rule_priority: int
    request_creation_time: datetime.datetime
    actions_executed: typing.List[str]
    redirect_url: str
    error_reason: str

    def __getitem__(self, item):
        return getattr(self, item)


