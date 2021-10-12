"""
Reverse Target Audience Analysis (RTAA-72) 
GRPC Multi Classification Server
"""
import os
import logging
from dotenv import load_dotenv
from config.config import AppConfig

from grpcserver.server import GRPCServer
from internal.cvcio.classification.accounts_pb2_grpc import (
    add_AccountServiceServicer_to_server,
)
from internal.cvcio.classification.comments_pb2_grpc import (
    add_CommentServiceServicer_to_server,
)
from services.accounts import AccountClassifier
from services.comments import CommentClassifier

from utils.helper import read_model, Model


def main():
    try:
        env = os.environ["ENV"]
    except KeyError:
        env = "development"

    load_dotenv(f".env.{env}")  # take environment variables from .env.

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
        Model(read_model("conf/account_classifier.json")),
    )

    # service comment classification
    server.RegisterService(
        CommentClassifier,
        add_CommentServiceServicer_to_server,
        Model(read_model("conf/comment_classifier.json")),
    )
    # start the server
    server.Serve()


if __name__ == "__main__":
    main()
