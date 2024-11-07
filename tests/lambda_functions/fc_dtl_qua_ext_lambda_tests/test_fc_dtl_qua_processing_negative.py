"""
    test_fc_dtl_qua_processing_negative negative pytest for fc_dtl_qua_ext_process_lambda
"""
from unittest.mock import patch
from unittest.mock import Mock
import pytest
from moto import mock_aws
from src.lambda_functions.fc_dtl_qua_ext_process_lambda import lambda_function


#key_file = 'CrewDetails.xml'

#Commenting out Pylint false positive error due to sonar conflict
#C0103 - UPPER_CASE NAMING CONVENTION, R0903 - Public method

#pylint: disable=R0903, invalid-name

class Context:
    """This class mocks the behavior of Context parameter of lambda function
    """
    function_name = "79104EXAMPLEB723"
    aws_request_id = "HHJSKKK"

def get_json_fake():
    """
    Get SQS message false
    """
    event = {
    "Records": [
        {
            "dy": 
            """
            {"Records":
            [
            {"s3":
            {"s3SchemaVersion":"1.0","configurationId":"tf-s3-queue-20240517160621839900000005",
            "bucket":
            {"name":"s3b-xml-314-iflightneo-output-dev-euwe1-01",
            "ownerIdentity":{"principalId":"AQZLYVWEEZIW8"},
            "arn":"arn:aws:s3: : :s3b-xml-314-iflightneo-output-dev-euwe1-01"},
            "object":{"key":"CrewDetails.xml",
            "size":11839,"eTag":"12ab75463f210b345732f6508f3c89c7"}}}
            ]
            }
            """
        }
    ]
}
    return event

def get_json_origin():
    """
    return sqs message JSON
    """
    event = {
    "Records": [
        {
            "body": 
            """
            {"Records":
            [
            {"s3":
            {"s3SchemaVersion":"1.0","configurationId":"tf-s3-queue-20240517160621839900000005",
            "bucket":{"name":"s3b-xml-314-iflightneo-output-dev-euwe1-01",
            "ownerIdentity":{"principalId":"AQZLYVWEEZIW8"},
            "arn":"arn:aws:s3: : :s3b-xml-314-iflightneo-output-dev-euwe1-01"},
            "object":{"key":"CrewDetails.xml",
            "size":11839,"eTag":"12ab75463f210b345732f6508f3c89c7"}}}
            ]
            }
            """
        }
    ]
}
    return event

class sub_class_s3:
    """Class which is used for mock and decode method
    """
    def decode(self):
        """
        method decode
        """
        input_file = None
        return input_file

class sub_class_gets3:
    """Class sub_class_gets3 
    """
    def decode(self):
        """Method decode
        """
        input_file = """<?xml version="1.0" encoding="ISO-8859-1" standalone="no"?>
                        <QualificationInfo>
                            <FlightCrewData>
                                <crewId>222942</crewId>
                                <licenseCode>LIC</licenseCode>
                                <licenseNumber>GBR.FCL.AT.412106L</licenseNumber>
                                <issueDate>2025-03-07</issueDate>
                                <effectiveDate>2025-03-07</effectiveDate>
                                <expiryDate>2050-03-07</expiryDate>
                            </FlightCrewData>
                        </QualificationInfo>"""
        return input_file

mocking_sub_class_s3_obj = sub_class_s3()
mocking_sub_class_gets3_obj =sub_class_gets3()

class Mockers3:
    """Mocker class which has read method and returns an object of another class
    """
    def read(self):
        """read method
        Returns:
            object: another class object
        """
        return mocking_sub_class_s3_obj
class Mockergets3:
    """class mockrgets3 which returns read method
    """
    def read(self):
        """method read

        Returns:
            object: returns object of another class
        """
        return mocking_sub_class_gets3_obj
mocking_s3_object = Mockers3()
mocking_s3_get_object=Mockergets3()
mocking_s3_put_object= Mockers3()

@patch("src.lambda_functions.fc_dtl_qua_ext_process_lambda.lambda_function.boto3.client")
def test(mock_client: Mock):
    """main test function test 0 of 2"""
    mock_client.return_value.get_object.return_value = {"Body": mocking_s3_object}
    mock_client.return_value.put_object.return_value = {"Body": mocking_s3_put_object}

    with pytest.raises(ValueError, match = 'File is empty'):
        lambda_function.lambda_handler(get_json_origin(), Context)

@mock_aws
def test_1():
    """test 1 of 2 and capture exception
    """
    with pytest.raises(KeyError):
        lambda_function.lambda_handler(get_json_fake(), Context)

@mock_aws
def test_2():
    """test 2 of 2 which capture exception
    """
    with pytest.raises(Exception):
        lambda_function.lambda_handler(get_json_origin(), Context)

# @patch("src.lambda_functions.fc_dtl_qua_ext_process_lambda.lambda_function.boto3.client")
# def test_3(mock_client: Mock):
#     mock_client.return_value.get_object.return_value = {"Body": mocking_s3_get_object}
#     with pytest.raises(Exception):
#         lambda_function.lambda_handler(get_json_origin(), Context)
