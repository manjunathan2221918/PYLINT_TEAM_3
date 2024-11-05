"""Test File for DLQ lambda
"""
import os
import pytest
import boto3
from moto import mock_aws

from src.lambda_functions.fc_dtl_qua_ext_dlq_process_lambda.lambda_function import lambda_handler

#pylint: disable=redefined-outer-name

class Context: # pylint: disable=too-few-public-methods
    """Class which mock the context paramter of 318 lambda_handler
    """
    function_name = "AWS_MOCK_FUNCTION_LAMBDA"
    aws_request_id = "AWS345LAMBDA0989"

def get_json_origin_315_sqs_dlq():
    """Input SQS JSON for 315 dlq
    """
    event_sqs_315 = {
    "Records": [
        {
            "body": 
            """
            {"Records":
            [
            {"s3":
            {"s3SchemaVersion":"1.0","configurationId":"tf-s3-queue-20240517160621839900000005",
            "bucket":{"name":"s3b-xml-315-iflightneo-output-dev-euwe1-01",
            "ownerIdentity":{"principalId":"AQZLYVWEEZIW8"},
            "arn":"arn:aws:s3: : :s3b-xml-315-iflightneo-output-dev-euwe1-01"},
            "object":{"key":"CrewDetails.xml",
            "size":11839,"eTag":"12ab75463f210b345732f6508f3c89c7"}}}
            ]
            }
            """
        }
    ]
}
    return event_sqs_315

def get_json_fake_sqs_dlq():
    """Input JSON false
    """
    event = {
    "Records": [
        {
            "b": 
            """
            {"Record":
            [
            {"s3":
            {"s3SchemaVersion":"1.0","configurationId":"tf-s3-queue-20240517160621839900000005",
            "bucket":{"name":"s3b-xml-315-iflightneo-output-dev-euwe1-01",
            "ownerIdentity":{"principalId":"AQZLYVWEEZIW8"},
            "arn":"arn:aws:s3: : :s3b-xml-315-iflightneo-output-dev-euwe1-01"},
            "object":{"key":"CrewDetails.xml",
            "size":11839,"eTag":"12ab75463f210b345732f6508f3c89c7"}}}
            ]
            }
            """
        }
    ]
}
    return event


@pytest.fixture
def s3_boto():
    """Create an S3 boto3 client and return the client object"""
    with mock_aws():
        s3 = boto3.client('s3', region_name='us-east-1')
        return s3

@mock_aws
def test_positive_315(s3_boto):
    """Test the custom lambda function mocking aws with moto"""
    bucket = "s3b-xml-315-iflightneo-output-dev-euwe1-01"
    key = "CrewDetails.xml"
    body = "testing"
    s3_boto.create_bucket(Bucket=bucket)
    s3_boto.put_object(Bucket=bucket, Key=key, Body=body)
    os.environ["ERROR_BUCKET_NAME"] = "s3b-xml-315-iflightneo-output-dev-euwe1-01"
    result = lambda_handler(get_json_origin_315_sqs_dlq(), Context)
    assert result == "Dead Letter Queue"


def test_negative_1_315():
    "Fail Test only for SQS"
    result = lambda_handler(get_json_fake_sqs_dlq(), Context)
    assert result == "Failed"


def test_negative_2_315():
    "Fail Test for store the event message in s3 bucket by ignoring env variables"
    result = lambda_handler(get_json_origin_315_sqs_dlq(), Context)
    assert result == "Failed to put message"
