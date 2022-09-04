"""
Reverse Target Audience Analysis (RTAA-72) 
GRPC Multi Classification Server
"""
import os
import logging

from config.config import AppConfig
from dotenv import load_dotenv

from grpcserver.server import GRPCServer

from services.accounts import AccountClassifier
from services.comments import CommentClassifier

from proto.rtaa.classification.accounts.v1.accounts_pb2_grpc import (
    add_AccountServiceServicer_to_server,
)
from proto.rtaa.classification.comments.v1.comments_pb2_grpc import (
    add_CommentServiceServicer_to_server,
)

from utils.helper import read_model


def main():
    load_dotenv()  # take environment variables from .env.

    # load conf from
    conf = AppConfig(os.environ)

    # set log format and level
    logging.basicConfig(level=conf.LOG_LEVEL, format=conf.LOG_FORMAT)

    # start the server
    server = GRPCServer(host=conf.HOSTNAME, port=conf.PORT)
    
    # register available services
    # service account classification
    server.RegisterService(
        AccountClassifier,
        add_AccountServiceServicer_to_server,
        read_model("conf/account_classifier.json"),
    )

    # service comment classification
    server.RegisterService(
        CommentClassifier,
        add_CommentServiceServicer_to_server,
        read_model("conf/comment_classifier.json"),
    )
    # start the server
    server.Serve()


if __name__ == "__main__":
    main()
