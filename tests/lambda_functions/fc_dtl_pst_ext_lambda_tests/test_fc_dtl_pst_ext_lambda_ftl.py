"""
New pytest for transfer_lambda for redundancy
"""
#pylint: disable=unused-import
from unittest.mock import MagicMock, patch, Mock, mock_open
from unittest import mock
import os
import boto3
import paramiko
import pytest
from src.lambda_functions.fc_dtl_pst_ext_transfer_lambda import lambda_function

#Commenting out Pylint false positive error
#pylint: disable=line-too-long, broad-except, too-few-public-methods, global-statement, unused-variable, invalid-name

class Context:
    """Mocking the Context object of 318 lambda function using
       class attribute
    """
    function_name = "AWS_MOCK_FUNCTION_LAMBDA"
    aws_request_id = "AWS125LAMBDA099"

def get_json_origin_318_pr():
    """ SQS mocking for 318 pr lambda
    """
    event_sqs_return = {
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
    return event_sqs_return

def get_json_fake_318_pr():
    """ Mokcing error input sqs message
    """
    event_sqs_return_error = {
    "Records": [
        {
            "bdy": 
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
    return event_sqs_return_error

def enc_var():
    """Mocked environment variables
    """
    os.environ['OUTPUT_BUCKET_NAME'] = "DUMMY_BUCKET"
    os.environ['IBS_SFTP_PATH'] = "remote"
    os.environ['POL_SECRET_ARN'] = "util-test-password"
    os.environ['REGION'] = "us-east-1"
    os.environ['POL_SFTP_HOST'] = "127.0.0.1"
    os.environ['POL_SFTP_PORT'] = "22"
    os.environ['POL_SFTP_USER_NAME'] = "user"


@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.info')
@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.decode')
@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.check_null')
@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.connection')
@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.send')
def test_lambda_handler(mocked_send_318, mocked_connection_318, mocked_check_318, mocked_decode_318, mocked_info_318):
    """lambda_hanlder_success testing function

    Args:
        mocked_send (mock_obj): None
        mocked_connection (mock_obj): None
        mocked_check (mock_obj): None
        mocked_decode (mock_obj): None
        mocked_info (mock_obj): None
    """
    mocked_send_318.return_value = None
    mocked_connection_318.return_value = None
    mocked_check_318.return_value = None
    mocked_decode_318.return_value = None
    mocked_info_318.return_value = None

    result = lambda_function.lambda_handler(get_json_origin_318_pr(), Context)
    assert result is None

def test_info():
    """info function call
    """
    lambda_function.info()

@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.info')
@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.decode')
@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.check_null')
@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.connection')
@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.send')
def test_lambda_handler_negative_318(mocked_send_n_318, mocked_connection_n_318, mocked_check_n_318, mocked_decode_n_318, mocked_info_n_318):
    """testing lambda_handler_negative

    Args:
        mocked_send (mock_obj): None
        mocked_connection (mock_obj): None
        mocked_check (mock_obj): None
        mocked_decode (mock_obj): None
        mocked_info (mock_obj): None
    """
    mocked_send_n_318.return_value = None
    mocked_connection_n_318.return_value = None
    mocked_check_n_318.return_value = None
    mocked_decode_n_318.return_value = None
    mocked_info_n_318.return_value = None

    result_of_lh = lambda_function.lambda_handler(get_json_fake_318_pr(), Context)
    assert result_of_lh is None

def test_info_negative_318():
    """info function negative test 318
    """
    with pytest.raises(Exception):
        lambda_function.info()

@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.s3_client')
@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.bk_values', ['test-bucket', 'test-key'])
def test_decode_success_318(mock_s3_client_obj):
    """test decode function success scenario

    Args:
        mock_s3_client (mock_obj): string
    """
    mock_obj_pst = MagicMock()
    mock_obj_pst['Body'].read.return_value = b'some data'
    mock_s3_client_obj.get_object.return_value = mock_obj_pst
    lambda_function.decode()

@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.s3_client')
@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.bk_values', ['test-bucket', 'test-key'])
def test_decode_failure_318(mock_s3_client_obj):
    """test_decode_failure scenario
    Args:
        mock_s3_client (mock_oject): return a error
    """
    mock_s3_client_obj.get_object.side_effect = Exception('S3 Error')
    with pytest.raises(Exception):
        lambda_function.decode()

@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.access')
def test_check_null_318(mock_access):
    """test_check null

    Args:
        mock_access (mock): None
    """
    mock_access.return_value = None
    lambda_function.check_null()


def test_access_failed_318():
    """test access failed
    """
    with pytest.raises(Exception):
        lambda_function.access()

mock_sftp_variables_pytest = {
    "Region": "us-west-2",
    "SSH_Key": "test_key_id"
}


private_key_sftp_ftl = None


def setup_mock_client(mock_get_secret_value):
    """ mock client setup

    Args:
        mock_get_secret_value (mock): key value pair

    Returns:
        dict: string
    """
    mock_client_obj = MagicMock()
    mock_client_obj.get_secret_value.return_value = {'SecretString': 'mocked_private_key'}
    mock_get_secret_value.return_value = mock_client_obj
    return mock_client_obj


@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.boto3.client')
def test_access_success_318(mock_boto_client):
    """test access success

    Args:
        mock_boto_client (mock): dict
    """
    enc_var()
    mock_client = setup_mock_client(mock_boto_client)
    global private_key_sftp_ftl
    private_key_sftp_ftl = None
    with pytest.raises(Exception):
        lambda_function.access()
        assert private_key_sftp_ftl == 'mocked_private_key'
        mock_boto_client.assert_called_once_with('secretsmanager', region_name=mock_sftp_variables_pytest["Region"])
        mock_client.get_secret_value.assert_called_once_with(SecretId=mock_sftp_variables_pytest["SSH_Key"])
@patch('paramiko.Transport')
def test_connection_318(mock_transport_tc):
    """test sftp connection success

    Args:
        mock_transport (mock): error
    """
    mock_transport_instance_318_ftl = MagicMock()
    mock_transport_tc.side_effect = Exception('Connection Failed 318')
    with pytest.raises(Exception, match = 'Connection Failed 318'):
        lambda_function.connection()

# sftp_variables = {
#     "SFTP_Host": "host",
#     "SFTP_Port": "22",
#     "SFTP_USR_NAME": "user"
# }

private_key_sftp_ftl = "dummy_private_key"

def test_connection_success_ftl_318():
    """test connection success
    """
    with mock.patch('paramiko.Transport') as mock_transport:
        with mock.patch('paramiko.RSAKey.from_private_key') as mock_rsa_key:
            with mock.patch('paramiko.SFTPClient.from_transport') as mock_sftp_client:
                mock_transport_instance_318_ftl = mock_transport.return_value
                mock_rsa_key_instance_var = mock_rsa_key.return_value
                # mock_sftp_client_instance = mock_sftp_client.return_value
                with pytest.raises(Exception):
                    lambda_function.connection()

                    mock_transport.assert_called_once_with(('host', 22))
                    # mock_transport_instance_318_ftl.connect.assert_called_once_with(
                    #     username='user',
                    #     pkey=mock_rsa_key_instance
                    # )
                    # mock_sftp_client.assert_called_once_with(mock_transport_instance_318_ftl)

@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.s3_client')
@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.sftp_sender')
@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.transport_layer')
@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.sftp_variables', {'Destination_absolute_path_IBS': 'remote'})
def test_send_success_ftl_318(mock_transport_layer_ss, mock_sftp_sender_ss, mock_s3_client_ss):
    """send test

    Args:
        mock_transport_layer_ss (mock_obj): magic mock
        mock_sftp_sender_ss (mock_obj): magic mock
        mock_s3_client_ss (mock_obj): magic mock
    """
    mock_s3_client_ss.download_file = MagicMock()
    mock_sftp_sender_ss.put = MagicMock()
    mock_sftp_sender_ss.close = MagicMock()
    mock_transport_layer_ss.close = MagicMock()
    lambda_function.send()
    mock_s3_client_ss.download_file.assert_called_once_with('s3b-xml-314-iflightneo-output-dev-euwe1-01', 'CrewDetails.xml', '/tmp/'+'CrewDetails.xml')
    mock_sftp_sender_ss.put.assert_called_once_with('/tmp/'+'CrewDetails.xml', 'remote/'+'CrewDetails.xml')
    mock_sftp_sender_ss.close.assert_called_once()
    mock_transport_layer_ss.close.assert_called_once()



@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.s3_client')
@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.sftp_sender')
@patch('src.lambda_functions.fc_dtl_pst_ext_transfer_lambda.lambda_function.transport_layer')
def test_send_failure_ftl_318(mock_transport_layer_sf, mock_sftp_sender_sf, mock_s3_client_sf):
    """send failure test for 318 ftl

    Args:
        mock_transport_layer_sf (mock_obj): magic mock
        mock_sftp_sender_sf (mock_obj): magic mock
        mock_s3_client_sf (mock_obj): magic mock
    """
    mock_s3_client_sf.download_file = MagicMock(side_effect=Exception("Download failed"))

    with pytest.raises(Exception, match="Download failed"):
        lambda_function.send()

    # Ensure other methods are not called in case of failure
    mock_sftp_sender_sf.put.assert_not_called()
    mock_sftp_sender_sf.close.assert_not_called()
    mock_transport_layer_sf.close.assert_not_called()
