import grpc

from proto.rtaa.classification.accounts.v1.accounts_pb2 import TwitterAccount, TwitterAccountList
from proto.rtaa.classification.accounts.v1.accounts_pb2_grpc import AccountServiceStub
from proto.rtaa.classification.comments.v1.comments_pb2 import Comment, CommentList
from proto.rtaa.classification.comments.v1.comments_pb2_grpc import CommentServiceStub
from proto.rtaa.classification.common.v1.predictions_pb2 import Prediction
from proto.rtaa.classification.common.v1.meta_pb2 import Meta

from google.protobuf.timestamp_pb2 import Timestamp


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel(
        "0.0.0.0:50052", options=(("grpc.enable_http_proxy", 0),)
    ) as channel:
        account_stub = AccountServiceStub(channel)
        comment_stub = CommentServiceStub(channel)

        print("getUser---------------------------------")
        res = account_stub.ClassifyTwitterAccount(
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
        print(res)
        print("----------------------------------------")
        
        print("getUsers---------------------------------")
        res = account_stub.ClassifyTwitterAccounts(
            TwitterAccountList(
                accounts=[
                    TwitterAccount(
                        followers=1,
                        following=2,
                        tweets=3,
                        favorites=4,
                        listed=5,
                        default_profile=True,
                        verified=True,
                        created_at=Timestamp(seconds=1527292217)
                    ),
                    TwitterAccount(
                        followers=100,
                        following=2000,
                        tweets=30000,
                        favorites=40000,
                        listed=500000,
                        default_profile=True,
                        verified=True,
                        created_at=Timestamp(seconds=1527292217)
                    )
                ]   
            )
        )
        print(res)
        print("----------------------------------------")

        print("getComment------------------------------")
        res = comment_stub.ClassifyToxic(
            Comment(
                text="@AdonisGeorgiadi @ArisPortosalte Αφήστε επιτέλους τις πολιτικές μεσαίου χώρου και κέντρου και ασκείστε δεξιά πολιτική επιτέλους ,του Κούλη θα του γυρίσει μπούμερανγκ η πολιτική του κέντρου.Αφήσατε τους λαθρομετανάστες  να αλωνίζον ,δεν αγγίξατε κανέναν στο δημόσιο ,οι μπαχαλάκηδες κάνουν βόλτες.Είστε ξεφτίλες. ",
                meta=Meta(
                    lang="el"
                )
            )
        )
        print(res)
        print("----------------------------------------")
        print("getComment------------------------------")
        res = comment_stub.ClassifyToxic(
            Comment(
                text="@AdonisGeorgiadi @ArisPortosalte Αφήστε επιτέλους τις πολιτικές μεσαίου χώρου και κέντρου και ασκείστε δεξιά πολιτική επιτέλους ,του Κούλη θα του γυρίσει μπούμερανγκ η πολιτική του κέντρου.Αφήσατε τους λαθρομετανάστες  να αλωνίζον ,δεν αγγίξατε κανέναν στο δημόσιο ,οι μπαχαλάκηδες κάνουν βόλτες.Είστε ξεφτίλες. ",
                meta=Meta(
                    lang="el"
                )
            )
        )
        print(res)
        print("----------------------------------------")

        print("getComments------------------------------")
        res = comment_stub.ClassifyToxicList(
            CommentList(
                comments=[
                    Comment(
                        text="@AdonisGeorgiadi @ArisPortosalte Αφήστε επιτέλους τις πολιτικές μεσαίου χώρου και κέντρου και ασκείστε δεξιά πολιτική επιτέλους ,του Κούλη θα του γυρίσει μπούμερανγκ η πολιτική του κέντρου.Αφήσατε τους λαθρομετανάστες  να αλωνίζον ,δεν αγγίξατε κανέναν στο δημόσιο ,οι μπαχαλάκηδες κάνουν βόλτες.Είστε ξεφτίλες. ",
                        meta=Meta(
                            lang="el"
                        )
                    ),
                    Comment(
                        text="@AdonisGeorgiadi @ArisPortosalte Αφήστε επιτέλους τις πολιτικές μεσαίου χώρου και κέντρου και ασκείστε δεξιά πολιτική επιτέλους ,του Κούλη θα του γυρίσει μπούμερανγκ η πολιτική του κέντρου.Αφήσατε τους λαθρομετανάστες  να αλωνίζον ,δεν αγγίξατε κανέναν στο δημόσιο ,οι μπαχαλάκηδες κάνουν βόλτες.Είστε ξεφτίλες. ",
                    ),
                    Comment(
                        text="@AdonisGeorgiadi @ArisPortosalte Αφήστε επιτέλους τις πολιτικές μεσαίου χώρου και κέντρου και ασκείστε δεξιά πολιτική επιτέλους ,του Κούλη θα του γυρίσει μπούμερανγκ η πολιτική του κέντρου.Αφήσατε τους λαθρομετανάστες  να αλωνίζον ,δεν αγγίξατε κανέναν στο δημόσιο ,οι μπαχαλάκηδες κάνουν βόλτες.Είστε ξεφτίλες. ",
                    ),
                    Comment(
                        text="#Russian spy pretending to be a \"Rothschild\" totally and completely infiltrated #Trump's inner circle & had access to #MarALago.",
                        meta=Meta(
                            lang="en"
                        )
                    ),
                    Comment(
                        text="Die you fucker.",
                        meta=Meta(
                            lang="en"
                        )
                    )
                ]
            )
        )
        print(res)
        print("----------------------------------------")
        
        print("getComment------------------------------")
        res = comment_stub.ClassifyToxic(
            Comment(
                text="@AdonisGeorgiadi @ArisPortosalte Αφήστε επιτέλους τις πολιτικές μεσαίου χώρου και κέντρου και ασκείστε δεξιά πολιτική επιτέλους ,του Κούλη θα του γυρίσει μπούμερανγκ η πολιτική του κέντρου.Αφήσατε τους λαθρομετανάστες  να αλωνίζον ,δεν αγγίξατε κανέναν στο δημόσιο ,οι μπαχαλάκηδες κάνουν βόλτες.Είστε ξεφτίλες. ",
                meta=Meta(
                    lang="und"
                )
            )
        )
        print(res)
        print("----------------------------------------")


if __name__ == "__main__":
    run()
