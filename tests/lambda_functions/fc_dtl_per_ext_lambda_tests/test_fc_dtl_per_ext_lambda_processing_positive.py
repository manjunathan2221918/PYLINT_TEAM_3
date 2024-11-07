"""
test_fc_dtl_per_ext_lambda_processing_positive positive pytest for fc_dtl_per_ext_process_lambda
"""
import os
from unittest.mock import patch
from unittest.mock import Mock
from src.lambda_functions.fc_dtl_per_ext_process_lambda import lambda_function

#KEY_FILE = 'CrewDetails.xml'

#Commenting out Pylint false positive error
#pylint: disable=line-too-long, too-few-public-methods, invalid-name, duplicate-code

class Context:
    """Mocking the Context object of lambda function using
       class attribute
    """
    function_name = "79104EXAMPLEB723"
    aws_request_id = "HHJSKKK"

def enc_var():
    """Mocked environment variables
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
    """ SQS mocking
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


class sub_class_s3:
    """
    mocking class
    """
    def decode(self):
        """
        mocking docode 
        """
        input_file = """<?xml version="1.0" encoding="ISO-8859-1" standalone="no"?>
                    <PersonnelInfo>
                        <FlightCrewData>
                            <CrewId>100001</CrewId>
                            <CrewCode>HUBRN</CrewCode>
                            <FirstName>balaji</FirstName>
                            <LastName>Rollow</LastName>
                            <CalledName>Jordin</CalledName>
                            <Gender>M</Gender>
                            <DateOfBirth>18-Dec-1974</DateOfBirth>
                            <JoiningDate>14-Nov-2002</JoiningDate>
                            <ToDate>14-Nov-2099</ToDate>
                            <PlaceofBirth>London</PlaceofBirth>
                            <CountryOfBirth>UK</CountryOfBirth>
                            <FlyingSinceDate>14-Nov-2002</FlyingSinceDate>
                            <LastPromotionDate>14-Nov-2002</LastPromotionDate>
                            <AppointmentCode>HHH</AppointmentCode>
                            <AppointmentStartDate>18-Dec-1964</AppointmentStartDate>
                            <AppointmentEndDate>14-Nov-2022</AppointmentEndDate>
                            <AppointmentCode>HH</AppointmentCode>
                            <AppointmentEndDate>14-Nov-2022</AppointmentEndDate>
                            <AirlineCode>BA</AirlineCode>
                            <EmploymentStartDate>18-Dec-1964</EmploymentStartDate>
                            <EmploymentEndDate>18-Dec-1964</EmploymentEndDate>
                            <SeniorityNumber>1994</SeniorityNumber>
                            <SeniorityFromDate>16-Apr-2019</SeniorityFromDate>
                            <SeniorityEndDate>31-Dec-4712</SeniorityEndDate>
                        </FlightCrewData>
                        <FlightCrewData>
                            <SeniorityNumber>1994</SeniorityNumber>
                            <SeniorityFromDate>16-Apr-2019</SeniorityFromDate>
                            <SeniorityEndDate>31-Dec-4712</SeniorityEndDate>
                        </FlightCrewData>
                        <FlightCrewData>
                            <CrewId>100002</CrewId>
                            <CrewCode>HUBRN</CrewCode>
                            <CalledName>Jordin</CalledName>
                            <ToDate>14-Nov-2099</ToDate>
                            <PlaceOfBirth>London</PlaceOfBirth>
                            <CountryOfBirth>UK</CountryOfBirth>
                            <FlyingSinceDate>14-Nov-2002</FlyingSinceDate>
                        </FlightCrewData>
                        <FlightCrewData>
                            <CrewId>100003</CrewId>
                            <AppointmentStartDate>18-Dec-1964</AppointmentStartDate>
                            <AppointmentEndDate>14-Nov-2022</AppointmentEndDate>
                        </FlightCrewData>
                        <FlightCrewData>
                            <CrewId>100004</CrewId>
                            <EmploymentStartDate>16-Apr-2019</EmploymentStartDate>
                        </FlightCrewData>
                        <FlightCrewData>
                            <CrewId>100005</CrewId>
                            <SeniorityFromDate>16-Apr-2019</SeniorityFromDate>
                            <SeniorityEndDate>31-Dec-4712</SeniorityEndDate>
                        </FlightCrewData>
                        <FlightCrewData>
                            <CrewId>100006</CrewId>
                            <AirlineCode></AirlineCode>
                            <EmploymentStartDate>16-Apr-2019</EmploymentStartDate>
                        </FlightCrewData>
                        <FlightCrewData>
                            <CrewId>100007</CrewId>
                            <AppointmentCode></AppointmentCode>
                            <AppointmentStartDate>18-Dec-1964</AppointmentStartDate>
                            <AppointmentEndDate>14-Nov-2022</AppointmentEndDate>
                        </FlightCrewData>
                        <FlightCrewData>
                            <CrewId>100008</CrewId>
                            <CrewCode>HUBRN</CrewCode>
                            <FirstName></FirstName>
                            <LastName>Rollow</LastName>
                            <CalledName>Jordin</CalledName>
                            <Gender>M</Gender>
                            <DateOfBirth>18-Dec-1974</DateOfBirth>
                            <JoiningDate>14-Nov-2002</JoiningDate>
                        </FlightCrewData>
                        <FlightCrewData>
                            <CrewId>100009</CrewId>
                            <FirstName>vasan</FirstName>
                            <LastName>Rollow</LastName>
                            <CalledName>Jordin</CalledName>
                            <Gender>M</Gender>
                            <DateOfBirth>18-Dec-1974</DateOfBirth>
                            <JoiningDate>14-Nov-2002</JoiningDate>
                        </FlightCrewData>
                    </PersonnelInfo>"""
        return input_file

mocking_sub_class_s3_obj = sub_class_s3()

class Mockers3:
    """
    mocking
    """
    def read(self):
        """
        mocking sub_class_s3_obj
        """
        return mocking_sub_class_s3_obj

mocking_s3_object = Mockers3()

@patch("src.lambda_functions.fc_dtl_per_ext_process_lambda.lambda_function.boto3.client")
def test(mock_client: Mock):
    """info function call
    """
    mock_client.return_value.get_object.return_value = {"Body": mocking_s3_object}
    enc_var()

    result = lambda_function.lambda_handler(get_json_origin(), Context)
    assert result[0][0][1:23] == "Element 'batchDetails'" #Batch Start
    assert result[0][1] == 'None'
    assert result[0][2][1:23] == "Element 'batchDetails'" #Batch Stop
    assert result[0][3] ==  'File Processing Complete'
