import io
import os
import json
import pickle

from collections import namedtuple


def read_model(filename):
    with io.open(os.path.join(filename), encoding="utf-8") as f:
        return json.loads(
            f.read(), object_hook=lambda d: namedtuple("MODEL", d.keys())(*d.values())
        )


def read_pickle(filename):
    with open(path, "rb") as file:
        try:
            while True:
                yield pickle.load(file)
        except EOFError:
            pass


def write_pickle(filename, data):
    with open(filename, "wb") as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


class Model:
    """Model Class"""

    def __init__(self, model):
        self.model = model
        self.path = model.path
        self.type = model.type
        self.tokenizer = model.tokenizer if model.tokenizer else ""
        self.classifier = model.classifier if model.classifier else ""
