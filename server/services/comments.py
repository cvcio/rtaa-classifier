import grpc
import logging
from typing import Any, List, Union

from google.rpc import code_pb2
from google.rpc import status_pb2
from grpc_status import rpc_status

from proto.rtaa.classification.comments.v1.comments_pb2_grpc import CommentServiceServicer
from proto.rtaa.classification.comments.v1.comments_pb2 import ResponseToxic, ResponseToxicList
from proto.rtaa.classification.common.v1.predictions_pb2 import Prediction

from utils.helper import Model, ModelMeta
from utils.strings import normalize_tweet


class CommentClassifier(CommentServiceServicer):
    """
    CommentClassifier
    """

    def __init__(self, model_meta) -> None:
        # load pre-trained models
        self.model_meta = {}
        self.models = {}
        
        for k in model_meta[0]:
            m = ModelMeta(k)
            self.model_meta[m.lang] = m
            
        for k, v in self.model_meta.items():
            if v.enabled:
                self.models[k] = Model(v)
        
        if len(self.models) == 1:
            self.model_meta[list(self.model_meta.keys())[0]].primary = True
            
        if len(self.models) == 0:
            self.models = None


    def __getModelFallback(self) -> Union[Model, None]:
        return next(
            (self.models[v.lang] for v in self.model_meta.values() if v.primary), None
        )

    def __getModel(self, lang: str) -> Union[Model, None]:
        return next(
            (self.models[k] for k, v in self.model_meta.items() if lang in v.supported_languages),
            None # self.__getModelFallback(),
        )

    def __mapListPredictions(
        self, doc: Any, threshold: float = 0.6
    ) -> List[Prediction]:
        return [
            Prediction(
                label=prediction["label"].upper(),
                score=prediction["score"],
                prediction=1 if prediction["score"] > threshold else 0,
            )
            for prediction in doc[0]
        ]

    def __mapKVPredictions(self, doc: Any, threshold: float) -> List[Prediction]:
        return [
            Prediction(
                label=k.upper(),
                score=v,
                prediction=1 if v > threshold else 0,
            )
            for k, v in doc.items()
        ]
        
    def __mapLabel(self, label: str) -> str:
        """
        Deprecated (used only with random forest classifier): Map Class from
        int (as returned by classifier) to string.
        """
        
        switcher = {
            "toxicity": "toxicity",
            "insult": "insult",
            "severe_toxicity": "severe_toxicity",
            "severe_toxic": "severe_toxicity",
            "identity_attack": "identity_attack",
            "identity_hate": "identity_attack",
            "obscene": "obscene",
            "threat": "threat",
        }

        return switcher.get(label, "")

    def ClassifyToxic(self, request, context: grpc.ServicerContext) -> ResponseToxic:
        # metadata = dict(context.invocation_metadata())
        # logging.debug("metadata: %s", metadata)
        
        if self.models == None:
            return context.abort_with_status(
                rpc_status.to_status(
                    status_pb2.Status(
                        code=code_pb2.INTERNAL,
                        message="Model Not Found or Not Implemented yet.",
                    )
                )
            )

        model = self.__getModel(request.meta.lang)
        if model == None:
            return context.abort_with_status(
                rpc_status.to_status(
                    status_pb2.Status(
                        code=code_pb2.INTERNAL,
                        message="Model Not Found or Not Implemented yet.",
                    )
                )
            )

        # normalize input string
        text = normalize_tweet(request.text)
        # run pipeline
        doc = model.model(text)

        # set threshold
        threshold = request.meta.threshold if request.meta.threshold > 0 else 0.6
        # create the predictions list
        predictions = (
            self.__mapListPredictions(doc, threshold)
            if isinstance(doc, list)
            else self.__mapKVPredictions(doc, threshold)
        )

        logging.debug(
            "(ClassifyToxic) Prediction -- %s",
            " - ".join(
                [
                    "CLASS: {} | SCORE: {:.2f}".format(x.label, x.score)
                    for x in predictions
                ]
            ),
        )
        # return response
        return ResponseToxic(predictions=predictions, meta=request.meta)

    def ClassifyToxicList(self, request, context: grpc.ServicerContext) -> ResponseToxicList:
        metadata = dict(context.invocation_metadata())
        logging.debug("metadata: %s", metadata)
        
        if self.models == None:
            return context.abort_with_status(
                rpc_status.to_status(
                    status_pb2.Status(
                        code=code_pb2.INTERNAL,
                        message="Model Not Found or Not Implemented yet.",
                    )
                )
            )
        
        if len(request.comments) > 100:
            return context.abort_with_status(
                rpc_status.to_status(
                    status_pb2.Status(
                        code=code_pb2.PERMISSION_DENIED,
                        message=f"Limit you request to MAX 10 comments.",
                    )
                )
            )

        comments = []
        logging.debug(
            "(ClassifyToxicList) Comments Length -- %d", len(request.comments)
        )
        for d in request.comments:
            model = self.__getModel(d.meta.lang)
            if model == None:
                comments.append(ResponseToxic(predictions=[], meta=d.meta))
                continue
            
            # normalize input string
            text = normalize_tweet(d.text)
            # run pipeline
            doc = model.model(text)
            # set threshold
            threshold = d.meta.threshold if d.meta.threshold > 0 else 0.6
            # create the predictions list
            predictions = (
                self.__mapListPredictions(doc, threshold)
                if isinstance(doc, list)
                else self.__mapKVPredictions(doc, threshold)
            )

            logging.debug(
                "(ClassifyToxic) Prediction -- %s",
                " - ".join(
                    [
                        "CLASS: {} | SCORE: {:.2f}".format(x.label, x.score)
                        for x in predictions
                    ]
                ),
            )
            # append predictions to list
            comments.append(ResponseToxic(predictions=predictions, meta=d.meta))
        # return response
        return ResponseToxicList(comments=comments)
