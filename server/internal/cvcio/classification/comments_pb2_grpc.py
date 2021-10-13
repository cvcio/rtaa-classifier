# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from internal.cvcio.classification import comments_pb2 as cvcio_dot_classification_dot_comments__pb2


class CommentServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ClassifyToxic = channel.unary_unary(
                '/classification.CommentService/ClassifyToxic',
                request_serializer=cvcio_dot_classification_dot_comments__pb2.Comment.SerializeToString,
                response_deserializer=cvcio_dot_classification_dot_comments__pb2.ResponseToxic.FromString,
                )
        self.ClassifyToxicList = channel.unary_unary(
                '/classification.CommentService/ClassifyToxicList',
                request_serializer=cvcio_dot_classification_dot_comments__pb2.CommentList.SerializeToString,
                response_deserializer=cvcio_dot_classification_dot_comments__pb2.ResponseToxicList.FromString,
                )


class CommentServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ClassifyToxic(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClassifyToxicList(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CommentServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ClassifyToxic': grpc.unary_unary_rpc_method_handler(
                    servicer.ClassifyToxic,
                    request_deserializer=cvcio_dot_classification_dot_comments__pb2.Comment.FromString,
                    response_serializer=cvcio_dot_classification_dot_comments__pb2.ResponseToxic.SerializeToString,
            ),
            'ClassifyToxicList': grpc.unary_unary_rpc_method_handler(
                    servicer.ClassifyToxicList,
                    request_deserializer=cvcio_dot_classification_dot_comments__pb2.CommentList.FromString,
                    response_serializer=cvcio_dot_classification_dot_comments__pb2.ResponseToxicList.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'classification.CommentService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CommentService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ClassifyToxic(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/classification.CommentService/ClassifyToxic',
            cvcio_dot_classification_dot_comments__pb2.Comment.SerializeToString,
            cvcio_dot_classification_dot_comments__pb2.ResponseToxic.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ClassifyToxicList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/classification.CommentService/ClassifyToxicList',
            cvcio_dot_classification_dot_comments__pb2.CommentList.SerializeToString,
            cvcio_dot_classification_dot_comments__pb2.ResponseToxicList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
