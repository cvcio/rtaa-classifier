PROTO_PATH=$(GOPATH)/src/github.com/cvcio/proto/proto

protocols: google tagger cvcio fix-grpc-paths

cvcio:
	python -m grpc_tools.protoc -I$(PROTO_PATH) --python_out=./server/internal --grpc_python_out=./server/internal $(PROTO_PATH)/cvcio/**/*.proto

tagger:
	python -m grpc_tools.protoc -I$(PROTO_PATH) --python_out=./server/internal --grpc_python_out=./server/internal $(PROTO_PATH)/tagger/*.proto

google:
	python -m grpc_tools.protoc -I$(PROTO_PATH) --python_out=./server/internal --grpc_python_out=./server/internal $(PROTO_PATH)/google/**/*.proto

serce:
	uvicorn server.main:app --reload

fix-grpc-paths:
	grep -rl --include="*.py" "from cvcio" . | xargs sed -i 's/from cvcio/from internal.cvcio/g'
	grep -rl --include="*.py" "from google.api" . | xargs sed -i 's/from google.api/from internal.google.api/g'
	grep -rl --include="*.py" "from tagger" . | xargs sed -i 's/from tagger/from internal.tagger/g'