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
import time
import ctypes

from hvm.env import HVM_USER_DIR

_LOAD_HVM_TENSORFLOW = False
_HVM_TF_LIB = None


def _load_lib():
    global _LOAD_HVM_TENSORFLOW
    global _HVM_TF_LIB
    if _LOAD_HVM_TENSORFLOW:
        return
    from .build import HVM_TF_LIB_NAME
    _HVM_TF_LIB_PATH = os.path.join(HVM_USER_DIR, HVM_TF_LIB_NAME)
    curdir = os.getcwd()
    libdir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(libdir)
    try:
        # _HVM_TF_LIB = ctypes.CDLL(_HVM_TF_LIB_PATH, ctypes.RTLD_LOCAL)
        import tensorflow as tf
        _HVM_TF_LIB = tf.load_op_library(_HVM_TF_LIB_PATH)
    finally:
        os.chdir(curdir)
    _LOAD_HVM_TENSORFLOW = True


def get_dataset_op():
    return _HVM_TF_LIB.HerculesTFDatasetCallbackOp


def compile_or_load_lib(silent=True):
    from hvm import contrib
    from .build import HVM_TF_LIB_NAME
    _HVM_TF_LIB_PATH = os.path.join(HVM_USER_DIR, HVM_TF_LIB_NAME)

    try:
        with contrib.util.filelock(_HVM_TF_LIB_PATH, timeout=300):
            success = False
            if os.path.exists(_HVM_TF_LIB_PATH):
                try:
                    _load_lib()
                    success = True
                except Exception as e:
                    success = False
                    print(f'[WARNING] hercules tensorflow extension: load failed: {e}, try rebuild and reload...',
                          file=sys.stderr)
            if not success:
                from .build import build_with_cmake
                try:
                    build_with_cmake()
                except Exception as e:
                    print(f'[WARNING] hercules tensorflow extension: build failed: {e}',
                          file=sys.stderr)
                    if not silent:
                        raise
                try:
                    _load_lib()
                except Exception as e:
                    print(f'[WARNING] hercules tensorflow extension: reload failed: {e}',
                          file=sys.stderr)
                    if not silent:
                        raise
    except contrib.util.FileLockTimeout:
        print(
            '\033[91mIt took too much time to wait for compiling tensorflow extension, please check if there is really a process hold this file \"{}.lock\".\033[0m'.format(
                _HVM_TF_LIB_PATH))
        raise
