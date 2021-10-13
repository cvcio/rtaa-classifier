import logging
import pickle
from numpy import argmax, max

from internal.cvcio.classification.accounts_pb2_grpc import AccountServiceServicer
from internal.cvcio.classification.accounts_pb2 import ResponseAccount
from internal.cvcio.common.predictions_pb2 import Prediction


class AccountClassifier(AccountServiceServicer):
    """
    AccouncClassifier uses a predifined model created by
    Civic Information Office from 2016 until today (17/07/2021),
    with 5000 handpicked users in the open-source version and more than
    25000 users in the production version.
    We use the CatBoost Classifier to predict user classes
    """

    def __init__(self, model):
        """
        Load Trained Model
        """
        self.model_meta = model[0]

        if self.model_meta.type == "random_forest":
            self.model = pickle.load(open(self.model_meta.path, "rb"))
            self.model.set_params(n_jobs=1)
            logging.debug("Random Forest {} Loaded".format(self.model_meta.version))

        if self.model_meta.type == "catboost":
            from catboost import CatBoostClassifier

            self.model = CatBoostClassifier(task_type="CPU")
            self.model.load_model(self.model_meta.path)
            logging.debug("CatBoost {} Loaded".format(self.model_meta.version))

        """
        Set Output Classes
        """
        self.classes = self.model.classes_
        logging.debug("Model Classes %s", self.classes)

    def mapClass(self, intClass):
        """
        Map Class from int (as returned by classifier) to string
        """
        switcher = {
            1.0: "INFLUENCER",
            2.0: "NORMAL",
            3.0: "AMPLIFIER",
            4.0: "UNKNOWN",
            5.0: "NEW",
        }

        return switcher.get(intClass, "UNKNOWN")

    def ClassifyTwitterAccount(self, request, context):
        """
        ClassifyTwitterAccount gRPC endpoint
        UserFeatures:
            Followers, Friends, Statuses,
            Favorites, Lists, Dates
        UserClass:
            Label: INFLUENCER, NORMAL, AMPLIFIER, UNKNOWN, NEW
            Score: double
        Runs the classifier (random forest) with UserFeatures
        Returns UserClass
        """

        """
        Calculate Parameteres
        """
        FFR = request.followers / request.friends if request.friends > 0 else 0
        STFV = request.statuses / request.favorites if request.favorites > 0 else 0
        ACTIONS = request.statuses + request.favorites
        ACTIONS = ACTIONS / request.dates if request.dates > 0 else 0
        STF = request.statuses / request.followers if request.followers > 0 else 0
        FVFR = request.favorites / request.friends if request.friends > 0 else 0
        FL = request.followers / request.lists if request.lists > 0 else 0

        """
        Set Features
        Order: 
            Followers, Friends, Statuses, Favorites, 
            Lists, FFR, STFV, Actions, STF, FVFR, FL
        """
        features = [
            request.followers,
            request.friends,
            request.statuses,
            request.favorites,
            request.lists,
            FFR,
            STFV,
            ACTIONS,
            STF,
            FVFR,
            FL,
        ]

        """
        Get Probability
        """
        proba = self.model.predict_proba([features])
        """
        Select Class with Higher Probability
        """
        predict = [
            Prediction(
                label=self.mapClass(self.classes[i])
                if self.model_meta.type == "random_forest"
                else self.classes[i],
                score=x,
                prediction=1 if x > 0.5 else 0,
            )
            for i, x in enumerate(proba[0])
        ]
        logging.debug(
            "(ClassifyTwitterAccount) Prediction -- CLASS: %s | SCORE: %.2f",
            self.classes[argmax(proba)],
            max(proba[0]),
        )
        return ResponseAccount(predictions=predict)

    def ClassifyTwitterAccountList(self, request, context):
        return None
