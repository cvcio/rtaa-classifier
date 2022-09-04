REGISTRY=cvcio
PROJECT=rtaa-72
TAG=`cat VERSION`
MODULE=rtaa-classifier
BUF_VERSION=1.7.0
PROTO_PATH:=$(GOPATH)/src/github.com/cvcio/rtaa-72/proto
PROTO_VERSION=1.0.0
CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
REG_PROJ=$(REGISTRY)/$(PROJECT)-$(MODULE)
REG_TAG=$(REGISTRY)/$(PROJECT)-$(MODULE):$(TAG)

buf-install: ## Install buf (buf.build)
	curl -sSL \
    	"https://github.com/bufbuild/buf/releases/download/v${BUF_VERSION}/buf-$(shell uname -s)-$(shell uname -m)" \
    	-o "$(shell go env GOPATH)/bin/buf" && \
  	chmod +x "$(shell go env GOPATH)/bin/buf"

proto-cp: ## Copy proto from root folder
	cp -r $(PROTO_PATH) .

proto-rm: ## Remove any leftovers
	rm -rf proto* rtaa-72

proto: proto-get buf-generate proto-rm ## Get and generate protocol buffers 

buf-generate: ## Generate protocol buffers 
	buf generate --template buf.gen.yaml

dev: ## Serve the service with nodemon
	nodemon -e *.py --exec python server/app.py

serve: ## Serve the service
	python server/app.py

docker-serve: ## Serve with docker
	python server/app.py

docker: ## Build the docker image
	docker build -f Dockerfile --rm -t $(REG_TAG) .
	docker tag $(REG_TAG) $(REG_PROJ):latest

docker-push: ## Push the docker image
	docker push $(REG_TAG)
	docker push $(REG_PROJ):latest

deployment: ## Update the deployment
	kubectl -n default set image deployment/${MODULE} ${MODULE}=$(REG_TAG)

prod: docker docker-push deployment ## Publish to production

help: ## Print Help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help
.PHONY: help buf-install proto-get proto-rm proto buf-generate dev serve docker docker-push deployment prod

proto-get: ## Get the protocol buffers from github.com/cvcio/proto
	curl -sSL \
    	https://github.com/cvcio/rtaa-72/archive/$(PROTO_VERSION).tar.gz | tar xz && \
    	mv raa-72-$(PROTO_VERSION)/proto proto && rm -rf rtaa-72