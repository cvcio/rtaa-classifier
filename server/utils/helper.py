import io
import os
import json
import pickle
import logging

from catboost import CatBoostClassifier
from collections import namedtuple
from detoxify import Detoxify
from typing import NamedTuple
from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForSequenceClassification,
)


def read_model(filename):
    with io.open(os.path.join(filename), encoding="utf-8") as f:
        return json.loads(
            f.read(), object_hook=lambda d: namedtuple("MODEL", d.keys())(*d.values())
        )


def read_pickle(filename):
    with open(filename, "rb") as file:
        try:
            while True:
                yield pickle.load(file)
        except EOFError:
            pass


def write_pickle(filename, data):
    with open(filename, "wb") as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


class ModelMeta:
    """ModelMeta Class"""

    def __init__(self, model_meta: NamedTuple):
        self.model_name = getattr(model_meta, "model_name", "")
        self.type = getattr(model_meta, "type", "")
        self.path = getattr(model_meta, "path", "")
        self.tokenizer = getattr(model_meta, "tokenizer", "")
        self.version = getattr(model_meta, "version", "v1")
        self.lang = getattr(model_meta, "lang", "")
        self.enabled = getattr(model_meta, "enabled", False)
        self.primary = getattr(model_meta, "primary", False)
        self.supported_languages = getattr(model_meta, "supported_languages", [])


class Model:
    """Model Class"""

    def __init__(self, model_meta: ModelMeta):
        self.model_meta = model_meta
        self.model = None

        if self.model_meta.type == "catboost" and self.model_meta.enabled:
            self.model = self.loadCatboostModel()

        if self.model_meta.type == "transformers" and self.model_meta.enabled:
            self.model = self.loadTransformersModel()

        if self.model_meta.type == "detoxify" and self.model_meta.enabled:
            self.model = self.loadDetoxifyModel().predict

        logging.debug(f"{self.model_meta.model_name} ({self.model_meta.type}) Loaded")

    def loadCatboostModel(self):
        model = CatBoostClassifier(task_type="CPU")
        model.load_model(self.model_meta.path)
        return model

    def loadDetoxifyModel(self):
        return Detoxify(self.model_meta.path)

    def loadTransformersModel(self):
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_meta.tokenizer, use_fast=False
        )
        model = AutoModelForSequenceClassification.from_pretrained(self.model_meta.path)
        pipe = (
            pipeline(
                "text-classification",
                model=model,
                tokenizer=tokenizer,
                top_k=-1,
                device=-1,
            )
            if tokenizer and model
            else None
        )

        return pipe
