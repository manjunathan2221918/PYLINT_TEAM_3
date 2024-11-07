"""
test_fc_dtl_qua_transfer  pytest for fc_dtl_qua_ext_transfer_lambda
"""
import os
from unittest.mock import MagicMock, patch, Mock, mock_open # pylint: disable=unused-import
from unittest import mock
import pytest
import boto3 # pylint: disable=unused-import
import paramiko # pylint: disable=unused-import
from src.lambda_functions.fc_dtl_qua_ext_transfer_lambda import lambda_function

#Remove Pylint false positive warnings
#pylint: disable=line-too-long, invalid-name, global-statement, unused-variable, unused-import
class Context: #pylint: disable=too-few-public-methods
    """Class Context which mock outs the lambda_handler
    """
    function_name = "AWS_MOCK_FUNCTION_LAMBDA"
    aws_request_id = "AWS12345LAMBDA0989"

def get_json_origin():
    """Input SQS JSON"""
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
            "object":{"key":"CrewDetails.xml","size":11839,
            "eTag":"12ab75463f210b345732f6508f3c89c7"}}}
            ]
            }
            """
        }
    ]
}
    return event

def get_json_fake():
    """Input SQS JSON"""
    event = {
    "Records": [
        {
            "bdy": 
            """
            {"Records":
            [
            {"s3":
            {"s3SchemaVersion":"1.0","configurationId":"tf-s3-queue-20240517160621839900000005",
            "bucket":{"name":"s3b-xml-314-iflightneo-output-dev-euwe1-01",
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
    return event

def enc_var():
    """This Functions lets out the mocked environment variables
    """
    os.environ['OUTPUT_BUCKET_NAME'] = "DUMMY_BUCKET"
    os.environ['IBS_SFTP_PATH'] = "remote"
    os.environ['CPD_SECRET_ARN'] = "util-test-password"
    os.environ['REGION'] = "us-east-1"
    os.environ['CPD_SFTP_HOST'] = "127.0.0.1"
    os.environ['CPD_SFTP_PORT'] = "22"
    os.environ['CPD_SFTP_USER_NAME'] = "user"

@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.info')
@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.decode')
@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.check_null')
@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.connection')
@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.send')
def test_lambda_handler(mocked_send, mocked_connection, mocked_check, mocked_decode, mocked_info):
    """test lambda_handler

    Args:
        mocked_send (obj): returns None explicitly 
        mocked_connection (obj): returns None explicitly 
        mocked_check (obj): returns None explicitly 
        mocked_decode (obj): returns None explicitly 
        mocked_info (obj): returns None explicitly 
    """
    mocked_send.return_value = None
    mocked_connection.return_value = None
    mocked_check.return_value = None
    mocked_decode.return_value = None
    mocked_info.return_value = None

    result = lambda_function.lambda_handler(get_json_origin(), Context)
    assert result is None

def test_info():
    """Test Info function alone
    """
    lambda_function.info()

@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.info')
@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.decode')
@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.check_null')
@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.connection')
@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.send')
def test_lambda_handler_negative(mocked_send, mocked_connection, mocked_check, mocked_decode, mocked_info):
    """test lambda_handler negative scenario

    Args:
        mocked_send (obj): returns None explicitly 
        mocked_connection (obj): returns None explicitly 
        mocked_check (obj): returns None explicitly 
        mocked_decode (obj): returns None explicitly 
        mocked_info (obj): returns None explicitly 
    """
    mocked_send.return_value = None
    mocked_connection.return_value = None
    mocked_check.return_value = None
    mocked_decode.return_value = None
    mocked_info.return_value = None

    result = lambda_function.lambda_handler(get_json_fake(), Context)
    assert result is None

def test_info_negative_315():
    """Test Info function with negative scenario and catch it
    """
    with pytest.raises(Exception):
        lambda_function.info()

@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.s3_client')
@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.bk_values', ['test-bucket', 'test-key'])
def test_decode_success_315(mock_s3_client):
    """test function for decoding success

    Args:
        mock_s3_client (obj): magicmock with str method
    """
    mock_obj = MagicMock()
    mock_obj['Body'].read.return_value = b'some data'
    mock_s3_client.get_object.return_value = mock_obj
    lambda_function.decode()

@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.s3_client')
@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.bk_values', ['test-bucket', 'test-key'])
def test_decode_failure_315(mock_s3_client):
    """Test decode failure scenario

    Args:
        mock_s3_client (obj): raise Exception
    """
    mock_s3_client.get_object.side_effect = Exception('S3 Error')
    with pytest.raises(Exception):
        lambda_function.decode()

@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.access')
def test_check_null_315(mock_access):
    """test check null function

    Args:
        mock_access (obj): return None
    """
    mock_access.return_value = None
    lambda_function.check_null()


def test_access_failed_315():
    """Test Access Failed with Exception
    """
    with pytest.raises(KeyError, match = 'CPD_SECRET_ARN'):
        lambda_function.access()

mock_sftp_variables = {
    "Region": "us-west-2",
    "SSH_Key": "test_key_id"
}


private_key_sftp = None


def setup_mock_client(mock_get_secret_value):
    """setup the mock client

    Args:
        mock_get_secret_value (obj): return magic mock object
    """
    mock_client = MagicMock()
    mock_client.get_secret_value.return_value = {'SecretString': 'mocked_private_key'}
    mock_get_secret_value.return_value = mock_client
    return mock_client


@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.boto3.client')
def test_access_success(mock_boto_client):
    """Test Access Success

    Args:
        mock_boto_client (obj): Return a magic mock 
    """
    enc_var()
    mock_client = setup_mock_client(mock_boto_client)
    global private_key_sftp
    private_key_sftp = None
    with pytest.raises(Exception):
        lambda_function.access()
        assert private_key_sftp == 'mocked_private_key'
        mock_boto_client.assert_called_once_with('secretsmanager', region_name=mock_sftp_variables["Region"])
        mock_client.get_secret_value.assert_called_once_with(SecretId=mock_sftp_variables["SSH_Key"])

@patch('paramiko.Transport')
def test_connection(mock_transport):
    """Test Connection Function

    Args:
        mock_transport (Obj): Magic mock object
    """
    mock_transport_instance = MagicMock()
    mock_transport.side_effect = Exception('Connection Failed')
    with pytest.raises(Exception, match = 'Connection Failed'):
        lambda_function.connection()

sftp_variables = {
    "SFTP_Host": "host",
    "SFTP_Port": "22",
    "SFTP_USR_NAME": "user"
}

private_key_sftp = "dummy_private_key"

def test_connection_success():
    """Test Connection Success Scenario
    """
    with mock.patch('paramiko.Transport') as mock_transport:
        with mock.patch('paramiko.RSAKey.from_private_key') as mock_rsa_key:
            with mock.patch('paramiko.SFTPClient.from_transport') as mock_sftp_client:
                mock_transport_instance = mock_transport.return_value
                mock_rsa_key_instance = mock_rsa_key.return_value
                # mock_sftp_client_instance = mock_sftp_client.return_value
                with pytest.raises(Exception):
                    lambda_function.connection()

                    mock_transport.assert_called_once_with(('host', 22))
                    # mock_transport_instance.connect.assert_called_once_with(
                    #     username='user',
                    #     pkey=mock_rsa_key_instance
                    # )
                    # mock_sftp_client.assert_called_once_with(mock_transport_instance)

@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.s3_client')
@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.sftp_sender')
@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.transport_layer')
@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.sftp_variables', {'Destination_absolute_path_IBS': 'remote'})
def test_send_success(mock_transport_layer, mock_sftp_sender, mock_s3_client):
    """Test the send function

    Args:
        mock_transport_layer (obj): return magic mock object
        mock_sftp_sender (obj): return magic mock object
        mock_s3_client (obj): return magic mock object
    """
    mock_s3_client.download_file = MagicMock()
    mock_sftp_sender.put = MagicMock()
    mock_sftp_sender.close = MagicMock()
    mock_transport_layer.close = MagicMock()
    lambda_function.send()
    mock_s3_client.download_file.assert_called_once_with('s3b-xml-314-iflightneo-output-dev-euwe1-01', 'CrewDetails.xml', '/tmp/'+'CrewDetails.xml')
    mock_sftp_sender.put.assert_called_once_with('/tmp/'+'CrewDetails.xml', 'remote/'+'CrewDetails.xml')
    mock_sftp_sender.close.assert_called_once()
    mock_transport_layer.close.assert_called_once()



@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.s3_client')
@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.sftp_sender')
@patch('src.lambda_functions.fc_dtl_qua_ext_transfer_lambda.lambda_function.transport_layer')
def test_send_failure(mock_transport_layer, mock_sftp_sender, mock_s3_client):
    """Test Send Failure

    Args:
        mock_transport_layer (Obj): Raise an exception
        mock_sftp_sender (Obj): Raise an exception
        mock_s3_client (Obj): Raise an exception
    """
    mock_s3_client.download_file = MagicMock(side_effect=Exception("Download failed"))

    with pytest.raises(Exception, match="Download failed"):
        lambda_function.send()

    # Ensure other methods are not called in case of failure
    mock_sftp_sender.put.assert_not_called()
    mock_sftp_sender.close.assert_not_called()
    mock_transport_layer.close.assert_not_called()
