"""_summary_

    pytset for positive processing
    """
#pylint: disable=line-too-long, too-few-public-methods, invalid-name
import os
from unittest.mock import patch
from unittest.mock import Mock
from src.lambda_functions.fc_dtl_pst_ext_process_lambda.lambda_function import lambda_handler, postingcd_check, send_object_to_s3


#KEY_FILE = 'CrewDetails.xml'

class Context:
    """Mocking the Context object of lambda function using
       class attribute
    """
    function_name = "79104EXAMPLEB723"
    aws_request_id = "HHJSKKK"

def enc_var():
    """Mocked environment variables
    """
    os.environ['OUTPUT_BUCKET_NAME'] = 's3b-xml-318-iflightneo-output-dev-euwe1-01'

def get_json_origin():
    """ SQS mocking
    """
    event_sqs_json = {
    "Records": [
        {
            "body": 
            """
            {"Records":
            [
            {"s3":
            {"s3SchemaVersion":"1.0","configurationId":"tf-s3-queue-20240517160621839900000005",
            "bucket":{"name":"s3b-xml-318-iflightneo-output-dev-euwe1-01",
            "ownerIdentity":{"principalId":"AQZLYVWEEZIW8"},
            "arn":"arn:aws:s3: : :s3b-xml-314-iflightneo-output-dev-euwe1-01"},
            "object":{"key":"CrewDetails.xml","size":11839,
            "eTag":"12ab75463f210b345732f6508f3c89c7"}}}
            ]
            }
            """
        }
    ]
}
    return event_sqs_json

class sub_class_s3:
    """
    mocking class
    """
    def decode(self):
        """
        mocking docode 
        """
        input_file = """
P 777 LHR       9003 CLEMENTS              R    ROBERT                AAIBY     217423 CAA 02-JUN-2018 02-JUL-2018 N 01-OCT-2041 01-OCT-2041 P77L
  350 LHR       2515 ABBERTON              JM   JOHN                  ABBNJ     217424     06-NOV-2019 19-FEB-2020 N 06-JUN-2029 06-JUN-2029 P35L
C     LHR        174 ABBOTT                B    BRUCE                 ABBTB     668260     11-MAR-2009 17-APR-2009 Y 17-MAR-2031 17-MAR-2031 C77L
P 777           4506 ABBOTT                JO   JACK                  ABBTJ     238599     24-JUN-2024 20-OCT-2024 N 15-DEC-2059 15-DEC-2059 P77L
C 777 LHR        729 ABBOTT                MC   MARTIN                ABBTM            TC  05-JAN-2021 27-MAR-2021 N 11-JAN-2039 11-JAN-2039 C77L
P 320 LHR       4452 ABDUL-HAMID           OE   ODEI                  ABDDO     231406                 09-SEP-2024 N 22-MAY-2063 22-MAY-2063 P32L
C 320 LHR       1434 ABLEWHITE             R    RICHARD               ABLER     783422 TSC 08-JUN-2015 01-JUL-2015 N             06-OCT-2041 C32L
P 320 LHR       4393 ABLO                  SS   SAM                   ABLOS     244974     18-MAR-2024 15-JUL-2024 N 19-APR-2063 19-APR-2063 P32L
C 320 EUG       3690 ACRAMAN               D    DANIEL                ACRNZ     244974                 11-APR-2022 N             10-DEC-2055 C32X

FEEDSPAN 01-NOV-2024 30-NOV-2024
"""
        return input_file

mocking_sub_class_s3_obj = sub_class_s3()

class Mockers3:
    """mocking class
    """
    def read(self):
        """
        mocking sub_class_s3_obj
        """
        return mocking_sub_class_s3_obj

mocking_s3_object = Mockers3()

@patch("src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.boto3.client")
def test_1(mock_client: Mock):

    """info function call

    """
    mock_client.return_value.get_object.return_value = {"Body": mocking_s3_object}
    enc_var()
    result = lambda_handler(get_json_origin(), Context)
    assert result[0] == 'fc-dtl-pst-ext-process_Processed Successfully'

@patch("src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.boto3.client")
def test_2(mock_client: Mock):

    """info function call

    """
    mock_client.return_value.get_object.return_value = {"Body": mocking_s3_object}
    enc_var()

    result_1 = lambda_handler(get_json_origin(), Context)
    assert result_1[1][0] == 'main_func completed'

@patch("src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.boto3.client")
def test_3(mock_client: Mock):

    """info function call

    """
    mock_client.return_value.get_object.return_value = {"Body": mocking_s3_object}
    enc_var()
    result_1 = lambda_handler(get_json_origin(), Context)
    print(result_1)
    assert result_1[1][1] == "File Processed"

def test_send_object_to_s3():
    """info function call

    """
    cover_test = send_object_to_s3(0,[None])
    #assert cover_test is None
    assert cover_test == 'File processed without crew'

def test_mandatory_check_1():
    """info function call

    """
    record = [{'rank': 'P', 'fleet': '320', 'base': 'LHR', 'from_date': '06-NOV-2023', 'to_date': ''}]
    cover_test_mandatory = postingcd_check(record, [], None, None, None)
    assert cover_test_mandatory is None

def test_mandatory_check_2():
    """info function call

    """
    record = [{'rank': 'P', 'fleet': '787', 'base': 'LHR', 'from_date': '', 'to_date': '15-SEP-2045'}]
    cover_test_mandatory = postingcd_check(record,[], None, None, None)
    assert cover_test_mandatory is None

def test_mandatory_check_3():
    """info function call

    """
    record = [{'rank': 'P', 'fleet': '787', 'base': 'LHR', 'from_date': '', 'to_date': ''}]
    cover_test_mandatory = postingcd_check(record, [], None, None, None)
    assert cover_test_mandatory is None
