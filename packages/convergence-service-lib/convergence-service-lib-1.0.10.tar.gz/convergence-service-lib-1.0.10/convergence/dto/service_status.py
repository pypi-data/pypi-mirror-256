from typing import List, Dict
from convergence.dto.base_dto import ApiResponseBody


class ServiceEndpointDTO:
    def __init__(self):
        self.url = ''
        self.method = ''
        self.exposed_through_gateway = False
        self.expected_authorization = ''
        self.max_payload_size = 200 * 1024
        self.timeout = 10000
        self.rate_limiting_policy = []
        self.maintenance_mode = 'restrict'
        self.accepts = ['application/json']


class ServiceStatusInfoDTO(ApiResponseBody):
    def __init__(self):
        self.service_name = ''
        self.version_hash = ''
        self.version = ''
        self.status = ''
        self.endpoints: List[ServiceEndpointDTO] = []
        self.extra: Dict[str, str] = {}

    def get_response_body_type(self) -> str:
        return 'service_status'
