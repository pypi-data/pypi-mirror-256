from datetime import datetime
import logging
from typing import Union

from google.protobuf.timestamp_pb2 import \
    Timestamp  # pylint: disable=no-name-in-module

from truera.client.private.communicator.rot_service_communicator import \
    RotServiceCommunicator
from truera.client.private.communicator.rot_service_http_communicator import \
    HttpRotServiceCommunicator
from truera.client.public.auth_details import AuthDetails
from truera.protobuf.public.read_optimized_table_service import \
    read_optimized_table_service_pb2 as rot_pb


def _datetime_to_timestamp(dt: datetime) -> Timestamp:
    timestamp = Timestamp()
    timestamp.FromDatetime(dt)
    return timestamp


class RotServiceClient:

    def __init__(
        self, communicator: RotServiceCommunicator, logger=None
    ) -> None:
        self.logger = logger if logger else logging.getLogger(__name__)
        self.communicator = communicator

    @classmethod
    def create(
        cls,
        connection_string: str = None,
        logger=None,
        auth_details: AuthDetails = None,
        use_http: bool = False,
        *,
        verify_cert: Union[bool, str] = True
    ):
        if use_http:
            communicator = HttpRotServiceCommunicator(
                connection_string,
                auth_details,
                logger,
                verify_cert=verify_cert
            )
        else:
            from truera.client.private.communicator.rot_service_grpc_communicator import \
                GrpcRotServiceCommunicator
            communicator = GrpcRotServiceCommunicator(
                connection_string, auth_details, logger
            )
        return RotServiceClient(communicator, logger)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.communicator.close()

    def create_rot(
        self, project_id: str, data_collection_id: str, split_id: str,
        model_id: str, start_timestamp: Union[datetime, Timestamp],
        end_timestamp: Union[datetime, Timestamp]
    ) -> rot_pb.CreateRotResponse:
        req = rot_pb.CreateRotRequest(
            project_id=project_id,
            data_collection_id=data_collection_id,
            split_id=split_id,
            model_id=model_id,
            start_timestamp=_datetime_to_timestamp(start_timestamp)
            if isinstance(start_timestamp, datetime) else start_timestamp,
            end_timestamp=_datetime_to_timestamp(end_timestamp)
            if isinstance(end_timestamp, datetime) else end_timestamp
        )
        return self.communicator.create_rot(req)
