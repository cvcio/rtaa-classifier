import unittest
import grpc

from internal.cvcio.classification.accounts_pb2 import TwitterAccount, ResponseAccount
from internal.cvcio.classification.accounts_pb2_grpc import AccountServiceStub

from internal.cvcio.classification.comments_pb2 import Comment, ResponseToxic
from internal.cvcio.classification.comments_pb2_grpc import CommentServiceStub


class TestChannel(unittest.TestCase):
    channel = grpc.insecure_channel(
        "0.0.0.0:50051", options=(("grpc.enable_http_proxy", 0),)
    )

    def test_0(self):
        self.assertEqual(type(self.channel), grpc._channel.Channel)
        self.channel.close()


class TestClassifyTwitterAccount(unittest.TestCase):
    channel = grpc.insecure_channel(
        "0.0.0.0:50051", options=(("grpc.enable_http_proxy", 0),)
    )

    account_stub = AccountServiceStub(channel)

    def test_0(self):
        res = self.account_stub.ClassifyTwitterAccount(
            TwitterAccount(
                followers=1,
                friends=2,
                statuses=3,
                favorites=4,
                lists=5,
                ffr=6.0,
                stfv=7.0,
                stf=8.0,
                fvfr=9.0,
                fl=10.0,
                dates=11.0,
                actions=12.0,
            )
        )
        self.assertEqual(type(res), ResponseAccount)
        self.assertEqual(len(res.predictions), 4)
        self.channel.close()


class TestClassifyToxic(unittest.TestCase):
    channel = grpc.insecure_channel(
        "0.0.0.0:50051", options=(("grpc.enable_http_proxy", 0),)
    )

    comment_stub = CommentServiceStub(channel)

    def test_0(self):
        res = self.comment_stub.ClassifyToxic(
            Comment(
                text="@AdonisGeorgiadi @ArisPortosalte Αφήστε επιτέλους τις πολιτικές μεσαίου χώρου και κέντρου και ασκείστε δεξιά πολιτική επιτέλους ,του Κούλη θα του γυρίσει μπούμερανγκ η πολιτική του κέντρου.Αφήσατε τους λαθρομετανάστες  να αλωνίζον ,δεν αγγίξατε κανέναν στο δημόσιο ,οι μπαχαλάκηδες κάνουν βόλτες.Είστε ξεφτίλες. "
            )
        )
        self.assertEqual(type(res), ResponseToxic)
        self.assertEqual(len(res.predictions), 8)
        self.channel.close()


if __name__ == "__main__":
    unittest.main()
