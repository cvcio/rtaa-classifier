import grpc
import logging

from datetime import datetime

from google.rpc import code_pb2
from google.rpc import status_pb2
from grpc_status import rpc_status

from numpy import argmax, max
from typing import List
from utils.calculations import division

from proto.rtaa.classification.accounts.v1.accounts_pb2_grpc import AccountServiceServicer
from proto.rtaa.classification.accounts.v1.accounts_pb2 import (
    TwitterAccount,
    TwitterAccountList,
    ResponseAccount,
    ResponseAccountList,
)
from proto.rtaa.classification.common.v1.predictions_pb2 import Prediction
from utils.helper import Model, ModelMeta


class AccountClassifier(AccountServiceServicer):
    """
    AccouncClassifier uses a predifined model created by
    Civic Information Office from 2016 until (17/07/2021),
    with 5000 handpicked users in the open-source version and more than
    25000 users in the production version.
    We use the CatBoost Classifier to predict user classes
    """

    def __init__(self, model_meta) -> None:
        # load pre-trained model
        self.model_meta = ModelMeta(model_meta[0])
        self.model = Model(self.model_meta).model

    def mapClass(self, c) -> str:
        """
        Deprecated (used only with random forest classifier): Map Class from
        int (as returned by classifier) to string.
        """

        switcher = {
            1: "INFLUENCER",
            2: "NORMAL",
            3: "AMPLIFIER",
            4: "UNKNOWN",
            5: "NEW",
        }

        return switcher.get(c, "UNKNOWN")

    def buildFeatures(self, request: TwitterAccount) -> List:
        """_summary_

        Args:
            request (TwitterAccount): _description_

        Returns:
            List: _description_
        """

        created_at = request.created_at.ToDatetime()
        observed_at = datetime.now()
        dates_since = (observed_at - created_at).days

        actions_frequency = division(request.tweets + request.favorites, dates_since)
        tweets_frequency = division(request.tweets, dates_since)
        reputation = division(request.followers, request.followers + request.following)
        credibility = division(request.listed, request.listed + request.followers)
        followers_growth_rate = division(request.followers, dates_since)
        following_growth_rate = division(request.following, dates_since)
        favorites_growth_rate = division(request.favorites, dates_since)
        listed_growth_rate = division(request.listed, dates_since)
        followers_following_ratio = division(request.followers, request.following)
        tweets_favorites_ratio = division(
            request.tweets, request.tweets + request.favorites
        )
        """
        Features Order:
            tweets, followers, following, favorites, listed,
            default_profile, verified,
            actions_frequency, tweets_frequency, reputation,
            followers_growth_rate, following_growth_rate, favorites_growth_rate, listed_growth_rate,
            followers_following_ratio, credibility, tweets_favorites_ratio
        """
        return [
            request.followers,
            request.following,
            request.tweets,
            request.favorites,
            request.listed,
            int(request.default_profile == True),
            int(request.verified == True),
            actions_frequency,
            tweets_frequency,
            reputation,
            followers_growth_rate,
            following_growth_rate,
            favorites_growth_rate,
            listed_growth_rate,
            followers_following_ratio,
            credibility,
            tweets_favorites_ratio,
        ]

    def predicWithCatboost(self, features: List) -> List[Prediction]:
        """
        Runs the classifier on a pre-trained catboost model. Supported account
        features:
            tweets, followers, following, favorites, listed,
            default_profile, verified, actions_frequency,
            tweets_frequency, reputation, followers_growth_rate,
            following_growth_rate, favorites_growth_rate, listed_growth_rate,
            followers_following_ratio, credibility, tweets_favorites_ratio

        Args:
            features (List): A list with features: [
                tweets, followers, following, favorites, listed,
                default_profile, verified, actions_frequency,
                tweets_frequency, reputation, followers_growth_rate,
                following_growth_rate, favorites_growth_rate, listed_growth_rate,
                followers_following_ratio, credibility, tweets_favorites_ratio
            ].

        Returns:
            List[Prediction]: A list with predictions. Each prediction contains
            a label (str) with valus [INFLUENCER, NORMAL, AMPLIFIER, UNKNOWN],
            score (double) with values from 0.0-1.0 and prediction (int) with values
            either 0 or 1.
        """

        if len(features) == 1:
            # single prediction
            if len(features[0]) != 17:
                return [Prediction(label="UNKNOWN", score=1.0, prediction=1)]
        else:
            # multiple predictions
            pass

        # get probability
        probabilities = self.model.predict_proba(features)
        predict = []
        for i, x in enumerate(probabilities):
            p = []
            for j, y in enumerate(x):
                p.append(
                    Prediction(
                        label=self.model.classes_[j],
                        score=y,
                        prediction=1 if y > 0.5 else 0,
                    )
                )
            predict.append(sorted(p, key=lambda s: s.score, reverse=True))
            logging.info(
                "(ClassifyTwitterAccount) Prediction -- CLASS: %s | SCORE: %.2f",
                self.model.classes_[argmax(x)],
                max(probabilities[i]),
            )

        return predict[0] if len(features) == 1 else predict

    def ClassifyTwitterAccount(
        self, request: TwitterAccount, context: grpc.ServicerContext
    ) -> ResponseAccount:
        """ClassifyTwitterAccount gRPC endpoint.

        Args:
            request (TwitterAccount): Request Account Proto.
            context (grpc.ServicerContext)

        Returns:
            ResponseAccount
        """

        metadata = dict(context.invocation_metadata())
        logging.debug("metadata: %s", metadata)

        if self.model == None:
            return context.abort_with_status(
                rpc_status.to_status(
                    status_pb2.Status(
                        code=code_pb2.INTERNAL,
                        message="Model Not Found or Not Implemented yet.",
                    )
                )
            )

        try:
            features = self.buildFeatures(request)
        except (ValueError, KeyError) as error:
            return context.abort_with_status(
                rpc_status.to_status(
                    status_pb2.Status(
                        code=code_pb2.INTERNAL,
                        message=f"Unable to transform input data, error: {error.message}",
                    )
                )
            )

        # execute the pipeline
        predict = self.predicWithCatboost([features])

        # return response
        return ResponseAccount(predictions=predict)

    def ClassifyTwitterAccounts(
        self, request: TwitterAccountList, context: grpc.ServicerContext
    ) -> ResponseAccountList:
        """_summary_

        Args:
            request (TwitterAccountList): _description_
            context (grpc.ServicerContext)

        Returns:
            ResponseAccountList: _description_
        """

        metadata = dict(context.invocation_metadata())
        logging.debug("metadata: %s", metadata)

        if self.model == None:
            return context.abort_with_status(
                rpc_status.to_status(
                    status_pb2.Status(
                        code=code_pb2.INTERNAL,
                        message="Model is disabled",
                    )
                )
            )

        if len(request.accounts) > 100:
            return context.abort_with_status(
                rpc_status.to_status(
                    status_pb2.Status(
                        code=code_pb2.PERMISSION_DENIED,
                        message=f"Limit you request to MAX 100 accounts.",
                    )
                )
            )

        try:
            features = [self.buildFeatures(r) for r in request.accounts]
        except (ValueError, KeyError) as error:
            return context.abort_with_status(
                rpc_status.to_status(
                    status_pb2.Status(
                        code=code_pb2.INTERNAL,
                        message=f"Unable to transform input data, error: {error.message}",
                    )
                )
            )

        # execute the pipeline
        predict = self.predicWithCatboost(features)

        # return response
        return ResponseAccountList(
            accounts=[ResponseAccount(predictions=p) for p in predict]
        )
