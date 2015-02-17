#  Copyright 2014 Michael Medin
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from google.protobuf.descriptor import FieldDescriptor
import re, sys
from jinja2 import Template, Environment
import hashlib

FIELD_LABEL_MAP = {
    FieldDescriptor.LABEL_OPTIONAL: 'optional',
    FieldDescriptor.LABEL_REQUIRED: 'required',
    FieldDescriptor.LABEL_REPEATED: 'repeated'
}

FIELD_TYPE_MAP = {
    FieldDescriptor.TYPE_DOUBLE: 'double',
    FieldDescriptor.TYPE_FLOAT: 'float',
    FieldDescriptor.TYPE_INT64: 'int64',
    FieldDescriptor.TYPE_UINT64: 'uint64',
    FieldDescriptor.TYPE_INT32: 'int32',
    FieldDescriptor.TYPE_FIXED64: 'fixed64',
    FieldDescriptor.TYPE_FIXED32: 'fixed32',
    FieldDescriptor.TYPE_BOOL: 'bool',
    FieldDescriptor.TYPE_STRING: 'string',
    FieldDescriptor.TYPE_GROUP: 'group',
    FieldDescriptor.TYPE_MESSAGE: 'message',
    FieldDescriptor.TYPE_BYTES: 'bytes',
    FieldDescriptor.TYPE_UINT32: 'uint32',
    FieldDescriptor.TYPE_ENUM: 'enum',
    FieldDescriptor.TYPE_SFIXED32: 'sfixed32',
    FieldDescriptor.TYPE_SFIXED64: 'sfixed64',
    FieldDescriptor.TYPE_SINT32: 'sint32',
    FieldDescriptor.TYPE_SINT64: 'sint64',
}

def cinclude(string):
    return string.replace('.', '/').lower()

def make_title(prefix, text, suffix):
    text = text.strip()
    ret = ''
    if prefix:
        ret = len(text)*prefix + '\n'
    ret += text + '\n'
    ret += len(text)*suffix + '\n'
    return ret

def rst_link(string):
    return '`' + string.strip() + '`_'

def rst_pad(string, padlen):
    padding = padlen*' '
    return padding + string.rstrip('\n').replace('\n', '\n' + padding)

def rst_title(string, level):
    if level == 1:
        return make_title('#', string, '#')
    elif level == 2:
        return make_title('*', string, '*')
    elif level == 3:
        return make_title('', string, '=')
    elif level == 4:
        return make_title('', string, '^')
    else:
        return make_title('', string, '"')

def format_comment(string):
    return '\n'.join(map(lambda x:x.strip(), string.split('\n')))

HEADER_TPL = """{% macro gen_message(desc, level, path, trail) -%}
{% set trail = trail + '.' + desc.name %}
{% if level < 4 %}{{desc.name|rst_title(level)}}
{% endif %}
.. py:class:: {{trail}}

{% if COMMENTS[path] -%}{{COMMENTS[path]|format_comment|rst_pad(4)}}{% endif %}
{% for field_descriptor in desc.enum_type -%}
{% set spath = path + ',4,%d'%loop.index0 %}
    .. py:attribute:: {{field_descriptor.name}}
    
{% if COMMENTS[spath] -%}{{COMMENTS[spath]|format_comment|rst_pad(8)}}
{% endif %}
        ========================= =====
        Possible values           Id
        ========================= =====
{% for value in field_descriptor.value %}        {{value.name.ljust(25)}} {{value.number}}
{% endfor %}        ========================= =====
{% endfor %}
{% for field_descriptor in desc.field -%}
{% set spath = path + ',2,%d'%loop.index0 %}
    .. py:attribute:: {{field_descriptor.name}}
    
        A **{{FIELD_LABEL_MAP[field_descriptor.label]}}** value of type **{{FIELD_TYPE_MAP[field_descriptor.type]}}**
        
{% if COMMENTS[spath] -%}{{COMMENTS[spath]|format_comment|rst_pad(8)}}
{% endif %}
        
{% endfor %}
{% if desc.nested_type %}    **Nested messages**

{% for sdesc in desc.nested_type %}    * :py:class:`{{(trail + '.' + sdesc.name)}}`
{% endfor %}{% endif %}
{% for sdesc in desc.nested_type -%}
{{ gen_message(sdesc, 3, "%s,3,%d"%(path, loop.index0), trail) }}
{% endfor %}
{%- endmacro %}.. default-domain:: python

{{desc.package|rst_title(1)}}

{% for sdesc in desc.message_type %}
{{ gen_message(sdesc, 2, "4,%d"%loop.index0, desc.package) }}
{% endfor %}
"""

def make_paths(source_code):
    locations = {}
    for l in source_code.location:
        if hasattr(l, 'leading_comments') and l.leading_comments:
            locations[','.join(map(lambda x:'%s'%x, l.path))] = l.leading_comments.strip()
    return locations

def document_file(file_descriptor):
    env = Environment()
    env.filters['cinclude'] = cinclude
    env.filters['rst_title'] = rst_title
    env.filters['rst_pad'] = rst_pad
    env.filters['rst_link'] = rst_link
    env.filters['format_comment'] = format_comment
    
    comments = make_paths(file_descriptor.source_code_info)
    #sys.stderr.write('\n---->%s'%comments.keys())
    sys.stderr.write('\n---->%s'%comments)
    template = env.from_string(HEADER_TPL)
    data ={
        'desc':file_descriptor, 
        'COMMENTS':comments, 
        'FIELD_TYPE_MAP':FIELD_TYPE_MAP, 
        'FIELD_LABEL_MAP':FIELD_LABEL_MAP}
    return template.render(data)
