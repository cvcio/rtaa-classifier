import logging
from internal.cvcio.classification.comments_pb2_grpc import CommentServiceServicer
from internal.cvcio.classification.comments_pb2 import ResponseToxic
from internal.cvcio.common.predictions_pb2 import Prediction
from services.service import Service
from transformers import (
    pipeline,
    RobertaTokenizer,
    RobertaForSequenceClassification,
)


class CommentClassifier(CommentServiceServicer):
    def __init__(self, model):
        self.model = model[0]
        self.tokenizer = RobertaTokenizer.from_pretrained(
            self.model.tokenizer, cace_dir="./cache"
        )
        self.classifier = RobertaForSequenceClassification.from_pretrained(
            "/media/andefined/data/andefined/data/ai-models/roberta-el-uncased-twitter-toxic/6-5e5",
            num_labels=8,
        )

        self.pipeline_text_classification = pipeline(
            "text-classification",
            model=self.classifier,
            tokenizer=self.tokenizer,
            return_all_scores=True,
        )

    def DetectToxic(self, request, context):
        doc = self.pipeline_text_classification(request.text)
        predict = [
            Prediction(
                label=prediction["label"],
                score=prediction["score"],
                prediction=1 if prediction["score"] > 0.6 else 0,
            )
            for prediction in doc[0]
        ]
        logging.debug(predict)
        return ResponseToxic(predictions=predict)
