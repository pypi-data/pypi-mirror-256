# -*- coding: utf-8 -*-
# MinIO Python Library for Amazon S3 Compatible Cloud Storage,
# (C) 2023 MinIO, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
from datetime import datetime

from minio import Minio
from minio.commonconfig import SnowballObject

client = Minio(
    "play.min.io",
    access_key="Q3AM3UQ867SPQQA43P2F",
    secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
)

client.upload_snowball_objects(
    "my-bucket",
    [
        SnowballObject("my-object1", filename="/etc/hostname"),
        SnowballObject(
            "my-object2", data=io.BytesIO(b"hello"), length=5,
        ),
        SnowballObject(
            "my-object3", data=io.BytesIO(b"world"), length=5,
            mod_time=datetime.now(),
        ),
    ],
)
