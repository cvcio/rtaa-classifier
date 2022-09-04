# RTAA &mdash; Classifier

Comments & Twitter accounts gRPC classification service.

There are two distinct classification services a) account classification and b) comment classification.

AccouncClassifier uses a pre-trained model created by the [Civic Information Office](https://cvcio.org) from 2016 until 17/07/2021, with almost 12,000 handpicked accounts in the open-source version and more than 25,000 users in the production version, of which 7,000 (fake/genuine) accounts from [Botometer](https://botometer.osome.iu.edu/bot-repository/datasets.html).

In our approach we investigated the behavioural characteristics that differentiates normal accounts with "amplifiers" without addressing the binary logic -bot or not- instead, classifing accounts as Influencers, Active, Amplifier, and Unknown. We use the [CatBoost](https://catboost.ai/) Classifier to predict user classes Refer to [Twitter Accounts - CatBoost Classifier](notebooks/twitter-accounts-catboost-classifier.ipynb) notebook for more details.

CommentsClassifier uses multiple pre-trained models and can be extented with any fintuned model supported by [Huggingface](https://huggingface.co/)'s [transformers](https://huggingface.co/docs/transformers/index) module. By default we use [detoxify-original](https://github.com/unitaryai/detoxify) for english comments, [detoxify-multilingual](https://github.com/unitaryai/detoxify) for italian, french, russian, portuguese, spanish and turkish and out own [comments-el-toxic](https://huggingface.co/cvcio/comments-el-toxic) for greek comments.

## How to use

```bash
docker run --rm -it --name rtaa-classifier -p 50052:50052 cvcio/rtaa-72-rtaa-classifier:latest
```

## Development

```bash
# clone the repo
git clone git@github.com:cvcio/rtaa-classifier.git
cd rtaa-classifier

# create the virtual environment (ex. with cobda)
conda create --name rtaa-classifier python=3.9

# install poetry package manager
pip install poetry
# install dependencies
poetry install

# run the service
make serve
```

### Protos

It is recommented not to re-generate thh stubs if you want to have the latest version. Alternatevely you must clone the [rtaa-72](https://github.com/cvcio/rtaa-72) repo and set the `PROTO_PATH` environment variable to that path. To build the protos, we use [buf](https://buf.build). Please refer to buf's documentation on how to install it, alternatevely you can run:

```bash
# install buf
make buf-install

# build protocol buffers
# the command will download the latest version of github.com/cvcio/proto,
# generate the stubs, and finally clean up the leftovers.
make proto 
```

## Contribution

If you're new to contributing to Open Source on Github, [this guide](https://opensource.guide/how-to-contribute/) can help you get started. Please check out the contribution guide for more details on how issues and pull requests work. Before contributing be sure to review the [code of conduct](https://github.com/cvcio/rtaa-classifier/blob/main/CODE_OF_CONDUCT.md).

<a href="https://github.com/cvcio/rtaa-classifier/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=cvcio/rtaa-classifier" />
</a>

## License and Attribution

In general, we are making this software publicly available for broad, noncommercial public use, including academics, journalists, policymakers, researchers and the public in general.

If you use this service, please let us know at [info@cvcio.org](mailto:info@cvcio.org).

See our [LICENSE](https://github.com/cvcio/covid-19-api/blob/main/LICENSE.md) for the full terms of use for this software.