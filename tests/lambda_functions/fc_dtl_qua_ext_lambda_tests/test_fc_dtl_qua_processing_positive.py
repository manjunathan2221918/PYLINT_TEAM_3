"""Test File for Processing lambda
"""
import os
from unittest.mock import patch
from unittest.mock import Mock
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

def enc_var():
    """This functions returns environment variables to mock
    """
    os.environ["ERROR_BUCKET_NAME"] = "DUMMY_BUCKET"
    os.environ['REGION'] = "us-east-1"
    os.environ['ACCOUNT_ID'] = '730335227492'
    os.environ['BUCKET_NAME'] = 's3b-pol-bacommaestrodni-dev-euwe1-01'
    os.environ['INPUT_SQS_NAME'] = 'sqs-iflightneoint-dev-euwe1-xml-314-queue-1'
    os.environ['OUTPUT_BUCKET_NAME'] = 's3b-xml-314-iflightneo-output-dev-euwe1-01'
    os.environ['RDS_SECRET_NAME'] = 'java-util-test-password'
    os.environ['SQS_DLQ_NAME'] = 'sqs-iflightneoint-dev-euwe1-xml-314-dlq-queue-1'


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
            "size":11839,"eTag":"12ab75463f210b345732f6508f3c89c7"}
            }}
            ]
            }
            """
        }
    ]
}
    return event


class sub_class_s3:
    """Class Sub_class_s3 which mocks method decode
    """
    def decode(self):
        """
        method decode
        """
        input_file = """<?xml version="1.0" encoding="ISO-8859-1" standalone="no"?>
                        <QualificationInfo>
                            <FlightCrewData>
                                <crewId>227942</crewId>
                                <licenseCode>LIC</licenseCode>
                                <licenseNumber>GBR.FCL.AT.422106L</licenseNumber>
                                <issueDate>2024-03-07</issueDate>
                                <effectiveDate>2024-03-07</effectiveDate>
                                <expiryDate>2040-03-07</expiryDate>
                                <qualificationCode>APG</qualificationCode>
                                <fromDate>2024-03-07</fromDate>
                                <toDate>2099-03-07</toDate>
                                <rank>C</rank>
                                <fleettype>Ascend</fleettype>
                                <qualificationCode>APG</qualificationCode>
                                <fromDate>2024-03-07</fromDate>
                                <toDate>2099-03-07</toDate>
                                <rank>P</rank>
                                <fleettype>B777/B787</fleettype>
                                <qualificationCode>APG</qualificationCode>
                                <fromDate>2024-03-07</fromDate>
                                <toDate>2099-03-07</toDate>
                                <rank>None</rank>
                                <fleettype>None</fleettype>
                            </FlightCrewData>
                            <FlightCrewData>
                                <crewId>242942</crewId>
                                <qualificationCode>None</qualificationCode>
                                <fromDate>2024-03-07</fromDate>
                                <toDate>2099-03-07</toDate>
                                <rank>C</rank>
                                <fleettype>A380</fleettype>
                            </FlightCrewData>
                            <FlightCrewData>
                                <crewId>None</crewId>
                                <qualificationCode>None</qualificationCode>
                                <fromDate>2024-03-07</fromDate>
                                <toDate>2099-03-07</toDate>
                                <rank>C</rank>
                                <fleettype>A380</fleettype>
                            </FlightCrewData>
                            <FlightCrewData>
                                <crewId>227942</crewId>
                                <licenseCode>None</licenseCode>
                                <licenseNumber>GBR.FCL.AT.412106L</licenseNumber>
                                <issueDate>2023-03-07</issueDate>
                                <effectiveDate>2023-03-07</effectiveDate>
                                <expiryDate>2041-03-07</expiryDate>
                            </FlightCrewData>
                        </QualificationInfo>"""
        return input_file

mocking_sub_class_s3_obj = sub_class_s3()

class Mockers3:
    """Class mocker which mocks read method
       and return a mock object
    """
    def read(self):
        """read method of mocker

        Returns:
            object: mocking sub class s3
        """
        return mocking_sub_class_s3_obj

mocking_s3_object = Mockers3()

@patch("src.lambda_functions.fc_dtl_qua_ext_process_lambda.lambda_function.boto3.client")
def test(mock_client: Mock):
    """test function
    """
    mock_client.return_value.get_object.return_value = {"Body": mocking_s3_object}
    enc_var()
    result = lambda_function.lambda_handler(get_json_origin(), Context)
    assert result[0][0][1:23] == "Element 'batchDetails'" #Batch Start
    assert result[0][1] == 'None'
    assert result[0][2][1:23] == "Element 'batchDetails'" #Batch Stop
    assert result[0][3] ==  'File Processing Complete'
    