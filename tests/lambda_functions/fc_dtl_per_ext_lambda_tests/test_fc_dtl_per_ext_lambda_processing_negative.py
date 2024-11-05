"""_summary_

    pytest negative_process
"""
#pylint: disable=unused-import
import os
import sys
from unittest.mock import patch
from unittest.mock import Mock
import pytest
import boto3
from src.lambda_functions.fc_dtl_per_ext_process_lambda import lambda_function


KEY_FILE = 'CrewDetails.xml'
#Commenting out Pylint false positive error
#pylint: disable=line-too-long, too-few-public-methods, invalid-name, duplicate-code

class Context:
    """Mocking the Context object of lambda function using
       class attribute
    """
    function_name = "79104EXAMPLEB723"
    aws_request_id = "HHJSKKK"


def get_json_fake():
    """ SQS mocking
    """
    event = {
    "Records": [
        {
            "dy": 
            """
            {"Records":
            [
            {"s3":
            {"s3SchemaVersion":"1.0","configurationId":"tf-s3-queue-20240517160621839900000005","bucket":{"name":"s3b-xml-314-iflightneo-output-dev-euwe1-01","ownerIdentity":{"principalId":"AQZLYVWEEZIW8"},"arn":"arn:aws:s3: : :s3b-xml-314-iflightneo-output-dev-euwe1-01"},"object":{"key":"CrewDetails.xml","size":11839,"eTag":"12ab75463f210b345732f6508f3c89c7"}}}
            ]
            }
            """
        }
    ]
}
    return event

def get_json_s3_fail():
    """
    mocking
    """
    event = {
    "Records": [
        {
            "body": 
            """
            {"Records":
            [
            {"s4":
            {"s3SchemaVersion":"1.0","configurationId":"tf-s3-queue-20240517160621839900000005","bucket":{"name":"s3b-xml-314-iflightneo-output-dev-euwe1-01","ownerIdentity":{"principalId":"AQZLYVWEEZIW8"},"arn":"arn:aws:s3: : :s3b-xml-314-iflightneo-output-dev-euwe1-01"},"object":{"key":"CrewDetails.xml","size":11839,"eTag":"12ab75463f210b345732f6508f3c89c7"}}}
            ]
            }
            """
        }
    ]
}
    return event
def get_json_origin():
    """
    SQS mocking
    """
    event = {
    "Records": [
        {
            "body": 
            """
            {"Records":
            [
            {"s3":
            {"s3SchemaVersion":"1.0","configurationId":"tf-s3-queue-20240517160621839900000005","bucket":{"name":"s3b-xml-314-iflightneo-output-dev-euwe1-01","ownerIdentity":{"principalId":"AQZLYVWEEZIW8"},"arn":"arn:aws:s3: : :s3b-xml-314-iflightneo-output-dev-euwe1-01"},"object":{"key":"CrewDetails.xml","size":11839,"eTag":"12ab75463f210b345732f6508f3c89c7"}}}
            ]
            }
            """
        }
    ]
}
    return event

class sub_class_s3_fake:
    """mocking class
    """
    def decode(self):
        """
        mocking decode
        """
        input_file = None
        return input_file

mocking_sub_class_s3_obj = sub_class_s3_fake()

class Mockers3fake:
    """mocking class
    """
    def read(self):
        """
        mocking
        """
        return mocking_sub_class_s3_obj

mocking_s3_object_fake = Mockers3fake()


@patch("src.lambda_functions.fc_dtl_per_ext_process_lambda.lambda_function.boto3.client")
def test_fake(mock_client: Mock):
    """info function call
    """
    mock_client.return_value.get_object.return_value = {"Body": mocking_s3_object_fake}

    with pytest.raises(KeyError, match = 'body'):
        lambda_function.lambda_handler(get_json_fake(), Context)

    with pytest.raises(KeyError, match = 's3'):
        lambda_function.lambda_handler(get_json_s3_fail(), Context)

    with pytest.raises(ValueError, match = 'File is empty'):
        lambda_function.lambda_handler(get_json_origin(), Context)
