#  Copyright 2015 Michael Medin
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

from setuptools import setup, find_packages

setup(
    name             = 'rst-protobuf',
    version          = '0.0.1',
    packages         = [ 'rst_protobuf' ],
    scripts          = ['protoc-gen-rst', 'protoc-gen-rst.cmd'],
    install_requires = [ 'protobuf>=2.3.0' ],
    author           = 'Gregory Szorc',
    author_email     = 'gregory.szorc@gmail.com',
    description      = 'Rst protocol buffer code generator',
    license          = 'Apache 2.0',
    url              = 'http://github.com/mickem/rst-protobuf'
)
