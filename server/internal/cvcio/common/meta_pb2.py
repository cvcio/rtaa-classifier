# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cvcio/common/meta.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from internal.tagger import tagger_pb2 as tagger_dot_tagger__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='cvcio/common/meta.proto',
  package='common',
  syntax='proto3',
  serialized_options=b'Z#github.com/cvcio/proto/cvcio/common',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x17\x63vcio/common/meta.proto\x12\x06\x63ommon\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x13tagger/tagger.proto\"\xe9\x02\n\x04Meta\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06source\x18\x02 \x01(\t\x12\x13\n\x0bscreen_name\x18\x03 \x01(\t\x12`\n\x12\x63omment_created_at\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampB(\x9a\x84\x9e\x03#json:\"comment_created_at,omitempty\"\x12Z\n\x0fuser_created_at\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampB%\x9a\x84\x9e\x03 json:\"user_created_at,omitempty\"\x12V\n\rclassified_at\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampB#\x9a\x84\x9e\x03\x1ejson:\"classified_at,omitempty\"\x12\x0c\n\x04link\x18\x07 \x01(\t\x12\x0c\n\x04lang\x18\x08 \x01(\tB%Z#github.com/cvcio/proto/cvcio/commonb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,tagger_dot_tagger__pb2.DESCRIPTOR,])




_META = _descriptor.Descriptor(
  name='Meta',
  full_name='common.Meta',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='common.Meta.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='source', full_name='common.Meta.source', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='screen_name', full_name='common.Meta.screen_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='comment_created_at', full_name='common.Meta.comment_created_at', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\232\204\236\003#json:\"comment_created_at,omitempty\"', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_created_at', full_name='common.Meta.user_created_at', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\232\204\236\003 json:\"user_created_at,omitempty\"', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='classified_at', full_name='common.Meta.classified_at', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\232\204\236\003\036json:\"classified_at,omitempty\"', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='link', full_name='common.Meta.link', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='lang', full_name='common.Meta.lang', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=90,
  serialized_end=451,
)

_META.fields_by_name['comment_created_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_META.fields_by_name['user_created_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_META.fields_by_name['classified_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name['Meta'] = _META
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Meta = _reflection.GeneratedProtocolMessageType('Meta', (_message.Message,), {
  'DESCRIPTOR' : _META,
  '__module__' : 'cvcio.common.meta_pb2'
  # @@protoc_insertion_point(class_scope:common.Meta)
  })
_sym_db.RegisterMessage(Meta)


DESCRIPTOR._options = None
_META.fields_by_name['comment_created_at']._options = None
_META.fields_by_name['user_created_at']._options = None
_META.fields_by_name['classified_at']._options = None
# @@protoc_insertion_point(module_scope)