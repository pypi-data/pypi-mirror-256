# Copyright 2022 ByteDance Ltd. and/or its affiliates.
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import os
import sys

HVM_DEV_MODE = os.environ.get('HVM_DEV_MODE', '').lower()
HVM_DEV_MODE = HVM_DEV_MODE == '1'

HVM_INFO_COLLECTION = os.environ.get('HVM_INFO_COLLECTION', "1").lower()
HVM_INFO_COLLECTION = HVM_INFO_COLLECTION == "1"

HVM_USER_DIR = os.environ.get('HVM_USER_DIR', os.path.expanduser('~/.hercules/'))
try:
    os.makedirs(HVM_USER_DIR, exist_ok=True)
except:
    print('[WARNING] User directory created failed: ', HVM_USER_DIR, file=sys.stderr)
