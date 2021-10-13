import logging

from internal.cvcio.classification.comments_pb2_grpc import CommentServiceServicer
from internal.cvcio.classification.comments_pb2 import ResponseToxic
from internal.cvcio.common.predictions_pb2 import Prediction

from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForSequenceClassification,
)

from utils.strings import normalize_tweet


class CommentClassifier(CommentServiceServicer):
    """
    CommentClassifier
    """

    def __init__(self, model):
        """
        Load Trained Model
        """
        self.model_meta = model[0]
        # load the tokenizer
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_meta.tokenizer, use_fast=False
            )
        except OSError as err:
            self.tokenizer = None
            logging.error(err)
        # load the model
        try:
            self.classifier = AutoModelForSequenceClassification.from_pretrained(
                self.model_meta.classifier
            )
        except OSError as err:
            self.classifier = None
            logging.error(err)

        # set text-classification pipeline
        self.pipeline_text_classification = (
            pipeline(
                "text-classification",
                model=self.classifier,
                tokenizer=self.tokenizer,
                return_all_scores=True,
            )
            if self.tokenizer and self.classifier
            else None
        )

    def ClassifyToxic(self, request, context):
        if self.pipeline_text_classification == None:
            return ResponseToxic(predictions=[])
        # normalize input string
        text = normalize_tweet(request.text)
        # run pipeline
        doc = self.pipeline_text_classification(text)
        # create the predictions list
        predict = [
            Prediction(
                label=prediction["label"],
                score=prediction["score"],
                prediction=1 if prediction["score"] > 0.6 else 0,
            )
            for prediction in doc[0]
        ]
        logging.debug(
            "(ClassifyToxic) Prediction -- %s",
            " - ".join(
                ["CLASS: {} | SCORE: {:.2f}".format(x.label, x.score) for x in predict]
            ),
        )
        return ResponseToxic(predictions=predict)

    def ClassifyToxicList(self, request, context):
        return None
