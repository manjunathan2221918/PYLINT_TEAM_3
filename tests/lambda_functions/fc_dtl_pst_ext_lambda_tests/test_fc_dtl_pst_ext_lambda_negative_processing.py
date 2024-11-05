"""
    pytest for negative_processing 318
    """
#pylint: disable=line-too-long, too-few-public-methods, invalid-name
from unittest.mock import patch
from unittest.mock import Mock
from moto import mock_aws
import pytest
from src.lambda_functions.fc_dtl_pst_ext_process_lambda.lambda_function import lambda_handler

KEY_FILE = 'CrewDetails.xml'

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
            {"s3SchemaVersion":"1.0","configurationId":"tf-s3-queue-20240517160621839900000005","bucket":{"name":"s3b-xml-318-iflightneo-output-dev-euwe1-01","ownerIdentity":{"principalId":"AQZLYVWEEZIW8"},"arn":"arn:aws:s3: : :s3b-xml-314-iflightneo-output-dev-euwe1-01"},"object":{"key":"CrewDetails.xml","size":11839,"eTag":"12ab75463f210b345732f6508f3c89c7"}}}
            ]
            }
            """
        }
    ]
}
    return event

def get_json_origin():
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
            {"s3":
            {"s3SchemaVersion":"1.0","configurationId":"tf-s3-queue-20240517160621839900000005","bucket":{"name":"s3b-xml-318-iflightneo-output-dev-euwe1-01","ownerIdentity":{"principalId":"AQZLYVWEEZIW8"},"arn":"arn:aws:s3: : :s3b-xml-314-iflightneo-output-dev-euwe1-01"},"object":{"key":"CrewDetails.xml","size":11839,"eTag":"12ab75463f210b345732f6508f3c89c7"}}}
            ]
            }
            """
        }
    ]
}
    return event

class sub_class_s3:
    """mocking class
    """
    def decode(self):
        """
        mocking decode
        """
        input_file = None
        return input_file

class sub_class_gets3:
    """mocking class
    """
    def decode(self):
        """mocking
    """
        input_file = """
P 777 LHR       9003 CLEMENTS              R    ROBERT                AAIBY     217423 CAA 02-JUN-2018 02-JUL-2018 N 01-OCT-2041 01-OCT-2041 P77L

FEEDSPAN 01-NOV-2024 30-NOV-2024
"""
        return input_file

mocking_sub_class_s3_obj = sub_class_s3()
mocking_sub_class_gets3_obj =sub_class_gets3()

class Mockers3:
    """mocking class
    """
    def read(self):
        """mocking
        """
        return mocking_sub_class_s3_obj

class Mockergets3:
    """mocking class
    """
    def read(self):
        """mocking
        """
        return mocking_sub_class_gets3_obj

mocking_s3_object = Mockers3()
mocking_s3_get_object=Mockergets3()
mocking_s3_put_object= Mockers3()

@patch("src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.boto3.client")
def test(mock_client: Mock):

    """info function call

    """
    mock_client.return_value.get_object.return_value = {"Body": mocking_s3_object}
    mock_client.return_value.put_object.return_value = {"Body": mocking_s3_put_object}

    with pytest.raises(ValueError, match = 'File is empty'):
        lambda_handler(get_json_origin(), Context)

@mock_aws
def test_1():
    """info function call

    """
    with pytest.raises(Exception):
        lambda_handler(get_json_fake(), Context)

@mock_aws
def test_2():
    """info function call

    """
    with pytest.raises(Exception):
        lambda_handler(get_json_origin(), Context)

# @patch("src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.boto3.client")
# def test_3(mock_client: Mock):
#     mock_client.return_value.get_object.return_value = {"Body": mocking_s3_get_object}
#     with pytest.raises(Exception):
#         lambda_handler(get_json_origin(), Context)
