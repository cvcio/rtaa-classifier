import grpc

from internal.cvcio.classification.accounts_pb2 import TwitterAccount
from internal.cvcio.common.predictions_pb2 import Prediction
from internal.cvcio.classification.accounts_pb2_grpc import AccountServiceStub

from internal.cvcio.classification.comments_pb2 import Comment
from internal.cvcio.classification.comments_pb2_grpc import CommentServiceStub


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel(
        "0.0.0.0:50051", options=(("grpc.enable_http_proxy", 0),)
    ) as channel:
        account_stub = AccountServiceStub(channel)
        comment_stub = CommentServiceStub(channel)

        print("getUser---------------------------------")
        res = account_stub.DetectTwitterAccount(
            TwitterAccount(
                followers=1,
                friends=2,
                statuses=3,
                favorites=4,
                lists=5,
                ffr=6.0,
                stfv=7.0,
                fstfv=8.0,
                dates=9.0,
                actions=10.0,
            )
        )
        print(res)
        print("----------------------------------------")
        print("getComment------------------------------")
        res = comment_stub.DetectToxic(
            Comment(
                text="@AdonisGeorgiadi @ArisPortosalte Αφήστε επιτέλους τις πολιτικές μεσαίου χώρου και κέντρου και ασκείστε δεξιά πολιτική επιτέλους ,του Κούλη θα του γυρίσει μπούμερανγκ η πολιτική του κέντρου.Αφήσατε τους λαθρομετανάστες  να αλωνίζον ,δεν αγγίξατε κανέναν στο δημόσιο ,οι μπαχαλάκηδες κάνουν βόλτες.Είστε ξεφτίλες. "
            )
        )
        print(res)
        print("----------------------------------------")


if __name__ == "__main__":
    run()
