# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/rtaa/classification/accounts/v1/accounts.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from proto.rtaa.classification.common.v1 import meta_pb2 as proto_dot_rtaa_dot_classification_dot_common_dot_v1_dot_meta__pb2
from proto.rtaa.classification.common.v1 import predictions_pb2 as proto_dot_rtaa_dot_classification_dot_common_dot_v1_dot_predictions__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n4proto/rtaa/classification/accounts/v1/accounts.proto\x12%proto.rtaa.classification.accounts.v1\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a.proto/rtaa/classification/common/v1/meta.proto\x1a\x35proto/rtaa/classification/common/v1/predictions.proto\"\xd9\x02\n\x0eTwitterAccount\x12\x1c\n\tfollowers\x18\x01 \x01(\x03R\tfollowers\x12\x1c\n\tfollowing\x18\x02 \x01(\x03R\tfollowing\x12\x16\n\x06tweets\x18\x03 \x01(\x03R\x06tweets\x12\x1c\n\tfavorites\x18\x04 \x01(\x03R\tfavorites\x12\x16\n\x06listed\x18\x05 \x01(\x03R\x06listed\x12\'\n\x0f\x64\x65\x66\x61ult_profile\x18\x06 \x01(\x08R\x0e\x64\x65\x66\x61ultProfile\x12\x1a\n\x08verified\x18\x07 \x01(\x08R\x08verified\x12\x39\n\ncreated_at\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tcreatedAt\x12=\n\x04meta\x18\t \x01(\x0b\x32).proto.rtaa.classification.common.v1.MetaR\x04meta\"g\n\x12TwitterAccountList\x12Q\n\x08\x61\x63\x63ounts\x18\x01 \x03(\x0b\x32\x35.proto.rtaa.classification.accounts.v1.TwitterAccountR\x08\x61\x63\x63ounts\"d\n\x0fResponseAccount\x12Q\n\x0bpredictions\x18\x01 \x03(\x0b\x32/.proto.rtaa.classification.common.v1.PredictionR\x0bpredictions\"i\n\x13ResponseAccountList\x12R\n\x08\x61\x63\x63ounts\x18\x01 \x03(\x0b\x32\x36.proto.rtaa.classification.accounts.v1.ResponseAccountR\x08\x61\x63\x63ounts2\x80\x03\n\x0e\x41\x63\x63ountService\x12\xb0\x01\n\x16\x43lassifyTwitterAccount\x12\x35.proto.rtaa.classification.accounts.v1.TwitterAccount\x1a\x36.proto.rtaa.classification.accounts.v1.ResponseAccount\"\'\x82\xd3\xe4\x93\x02!:\x01*\"\x1c/v1/classify/account/twitter\x12\xba\x01\n\x17\x43lassifyTwitterAccounts\x12\x39.proto.rtaa.classification.accounts.v1.TwitterAccountList\x1a:.proto.rtaa.classification.accounts.v1.ResponseAccountList\"(\x82\xd3\xe4\x93\x02\":\x01*\"\x1d/v1/classify/accounts/twitterB\xf3\x01\n)com.proto.rtaa.classification.accounts.v1B\rAccountsProtoP\x01\xa2\x02\x04PRCA\xaa\x02%Proto.Rtaa.Classification.Accounts.V1\xca\x02%Proto\\Rtaa\\Classification\\Accounts\\V1\xe2\x02\x31Proto\\Rtaa\\Classification\\Accounts\\V1\\GPBMetadata\xea\x02)Proto::Rtaa::Classification::Accounts::V1b\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.rtaa.classification.accounts.v1.accounts_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n)com.proto.rtaa.classification.accounts.v1B\rAccountsProtoP\001\242\002\004PRCA\252\002%Proto.Rtaa.Classification.Accounts.V1\312\002%Proto\\Rtaa\\Classification\\Accounts\\V1\342\0021Proto\\Rtaa\\Classification\\Accounts\\V1\\GPBMetadata\352\002)Proto::Rtaa::Classification::Accounts::V1'
  _ACCOUNTSERVICE.methods_by_name['ClassifyTwitterAccount']._options = None
  _ACCOUNTSERVICE.methods_by_name['ClassifyTwitterAccount']._serialized_options = b'\202\323\344\223\002!:\001*\"\034/v1/classify/account/twitter'
  _ACCOUNTSERVICE.methods_by_name['ClassifyTwitterAccounts']._options = None
  _ACCOUNTSERVICE.methods_by_name['ClassifyTwitterAccounts']._serialized_options = b'\202\323\344\223\002\":\001*\"\035/v1/classify/accounts/twitter'
  _TWITTERACCOUNT._serialized_start=262
  _TWITTERACCOUNT._serialized_end=607
  _TWITTERACCOUNTLIST._serialized_start=609
  _TWITTERACCOUNTLIST._serialized_end=712
  _RESPONSEACCOUNT._serialized_start=714
  _RESPONSEACCOUNT._serialized_end=814
  _RESPONSEACCOUNTLIST._serialized_start=816
  _RESPONSEACCOUNTLIST._serialized_end=921
  _ACCOUNTSERVICE._serialized_start=924
  _ACCOUNTSERVICE._serialized_end=1308
# @@protoc_insertion_point(module_scope)
