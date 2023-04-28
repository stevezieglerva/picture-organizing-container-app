import json
import os
from abc import ABC, abstractmethod
from collections import namedtuple
from datetime import datetime

import boto3

S3Object = namedtuple("S3Object", "bucket key date size")


class S3Base(ABC):
    """Abstract base class for S3 methods allowing local file creation and easier AWS mocking"""

    @abstractmethod
    def put_object(self, bucket, key, data):
        raise NotImplementedError

    @abstractmethod
    def list_objects(self, bucket, prefix, total_max=0):
        raise NotImplementedError

    @abstractmethod
    def get_object(self, bucket, key):
        raise NotImplementedError

    @abstractmethod
    def delete_object(self, bucket, key):
        raise NotImplementedError


class S3(S3Base):
    """Actual S3 class with put and list objects"""

    def put_object(self, bucket, key, data):
        s3 = boto3.client("s3")
        resp = s3.put_object(Bucket=bucket, Key=key, Body=data)
        print(f"key: {key} resp {resp}")
        result = S3Object(
            bucket=bucket, key=key, date=datetime.now().isoformat, size=len(data)
        )
        return result

    def list_objects(self, bucket, prefix, total_max=0):
        print(locals())
        s3 = boto3.client("s3")
        results = []
        continuation_token = "start"
        print(f"Prefix: {prefix}")
        while continuation_token:
            if continuation_token == "start":
                if total_max > 0:
                    response = s3.list_objects_v2(
                        Bucket=bucket, Prefix=prefix, MaxKeys=total_max
                    )
                else:
                    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
                if "Contents" in response:
                    results += response["Contents"]
            else:
                response = s3.list_objects_v2(
                    Bucket=bucket,
                    Prefix=prefix,
                    ContinuationToken=continuation_token,
                )
                results.extend(response["Contents"])
            print(f"\tTotal objects: {len(results)}")
            continuation_token = response.get("NextContinuationToken", False)
            if total_max > 0 and len(results) >= total_max:
                continuation_token = ""
                print("Stopping since total_max hit")

        s3_results = []
        for object in results:
            # print(json.dumps(object, indent=3, default=str))
            file = S3Object(
                bucket=bucket,
                key=object["Key"],
                date=object["LastModified"],
                size=object["Size"],
            )
            s3_results.append(file)
        return s3_results

    def get_object(self, bucket, key):
        s3 = boto3.client("s3")
        response = s3.get_object(Bucket=bucket, Key=key)
        return response["Body"].read()

    def delete_object(self, bucket, key):
        s3 = boto3.client("s3")
        response = s3.delete_object(Bucket=bucket, Key=key)
        return response


class S3FakeLocal(S3Base):
    def put_object(self, bucket, key, data):
        filename = f"test_fakes3_integration_{bucket}__{key.replace('/', '__')}"
        with open(filename, "w") as file:
            file.write(data)
        result = S3Object(
            bucket="local", key=filename, date=datetime.now().isoformat, size=len(data)
        )
        return result

    def list_objects(self, bucket, prefix, total_max=0):
        raise NotImplementedError

    def get_object(self, bucket, key):
        filename = f"test_fakes3_integration_{bucket}__{key.replace('/', '__')}"
        print(f"Reading: {filename}")
        with open(filename, "r") as file:
            return file.read()

    def delete_object(self, bucket, key):
        filename = f"test_fakes3_integration_{bucket}__{key.replace('/', '__')}"
        print(f"Deleting: {filename}")
        os.remove(filename)
