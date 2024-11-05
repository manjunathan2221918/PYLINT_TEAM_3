"""Test File for 318 DLQ 
"""
import os
import pytest
import boto3
from moto import mock_aws

from src.lambda_functions.fc_dtl_pst_ext_dlq_process_lambda.lambda_function import lambda_handler

#pylint: disable=redefined-outer-name

class Context: # pylint: disable=too-few-public-methods
    """This class mocks the Context paramter of lambda_handler
    """
    function_name = "AWS_MOCK_FUNCTION_LAMBDA"
    aws_request_id = "AWS12345LAMBDA0989"

def get_json_origin_318_dlq():
    """
    Input SQS message
    """
    sqs_event = {
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
    return sqs_event

def get_json_fake_318_dlq():
    """Input sqs message but fake"""
    sqs_event = {
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
    return sqs_event


@pytest.fixture
def s3_boto_318_fixture_setup():
    """Create an dlq S3 boto3 client and return the client object"""
    with mock_aws():
        s3 = boto3.client('s3', region_name='us-east-1')
        return s3

@mock_aws
def test_positive_318_dlq(s3_boto_318_fixture_setup):
    """Test the custom lambda function mocking aws with moto"""
    bucket_1 = "s3b-xml-315-iflightneo-output-dev-euwe1-01"
    key = "CrewDetails.xml"
    body = "testing"
    s3_boto_318_fixture_setup.create_bucket(Bucket=bucket_1)
    s3_boto_318_fixture_setup.put_object(Bucket=bucket_1, Key=key, Body=body)
    os.environ["ERROR_BUCKET_NAME"] = "s3b-xml-315-iflightneo-output-dev-euwe1-01"
    result = lambda_handler(get_json_origin_318_dlq(), Context)
    assert result == "Dead Letter Queue"


def test_negative_1_318_dlq():
    "Fail Test only for SQS"
    result = lambda_handler(get_json_fake_318_dlq(), Context)
    assert result == "Failed"


def test_negative_2_318_dlq():
    "Fail Test for store the event message in s3 bucket by ignoring env variables"
    result = lambda_handler(get_json_origin_318_dlq(), Context)
    assert result == "Failed to put message"
