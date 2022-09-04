import unittest
import grpc

from proto.rtaa.classification.accounts.v1.accounts_pb2 import TwitterAccount, ResponseAccount
from proto.rtaa.classification.accounts.v1.accounts_pb2_grpc import AccountServiceStub
from proto.rtaa.classification.comments.v1.comments_pb2 import Comment, ResponseToxic
from proto.rtaa.classification.comments.v1.comments_pb2_grpc import CommentServiceStub


from google.protobuf.timestamp_pb2 import Timestamp


class TestChannel(unittest.TestCase):
    channel = grpc.insecure_channel(
        "0.0.0.0:50052", options=(("grpc.enable_http_proxy", 0),)
    )

    def test_0(self):
        self.assertEqual(type(self.channel), grpc._channel.Channel)
        self.channel.close()


class TestClassifyTwitterAccount(unittest.TestCase):
    channel = grpc.insecure_channel(
        "0.0.0.0:50052", options=(("grpc.enable_http_proxy", 0),)
    )

    account_stub = AccountServiceStub(channel)

    def test_0(self):
        res = self.account_stub.ClassifyTwitterAccount(
            TwitterAccount(
                followers=1,
                following=2,
                tweets=3,
                favorites=4,
                listed=5,
                default_profile=True,
                verified=True,
                created_at=Timestamp(seconds=1527292217)
            )
        )
        self.assertEqual(type(res), ResponseAccount)
        self.assertEqual(len(res.predictions), 4)
        self.channel.close()


class TestClassifyToxic(unittest.TestCase):
    channel = grpc.insecure_channel(
        "0.0.0.0:50052", options=(("grpc.enable_http_proxy", 0),)
    )

    comment_stub = CommentServiceStub(channel)

    def test_0(self):
        res = self.comment_stub.ClassifyToxic(
            Comment(
                text="@AdonisGeorgiadi @ArisPortosalte Αφήστε επιτέλους τις πολιτικές μεσαίου χώρου και κέντρου και ασκείστε δεξιά πολιτική επιτέλους ,του Κούλη θα του γυρίσει μπούμερανγκ η πολιτική του κέντρου.Αφήσατε τους λαθρομετανάστες  να αλωνίζον ,δεν αγγίξατε κανέναν στο δημόσιο ,οι μπαχαλάκηδες κάνουν βόλτες.Είστε ξεφτίλες. ",
            )
        )
        self.assertEqual(type(res), ResponseToxic)
        self.assertEqual(len(res.predictions), 7)
        self.channel.close()


if __name__ == "__main__":
    unittest.main()
