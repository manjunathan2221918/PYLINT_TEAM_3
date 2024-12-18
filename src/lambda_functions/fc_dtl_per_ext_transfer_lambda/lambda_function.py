"""
  fc_dtl_per_ext_transfer_lambda
  fetches file from S3 and send the file to IBS
"""
# pylint: disable=global-variable-undefined,invalid-name,global-statement,import-error
import json
import os
import configparser
from datetime import datetime
import io
import boto3
import paramiko
from src.lambda_functions.common.logger import log_success_msg,log_error_msg, pattern

#Error Codes properties
ERR_PATH = 'src/lambda_functions/common/'
CONS_PATH = 'src/lambda_functions/fc_dtl_per_ext_transfer_lambda/'

config_per = configparser.ConfigParser()
config_per.read(ERR_PATH+'errorcodes.properties')
error_codes = config_per['ERROR_CODES']

config_per.read(CONS_PATH+'constants.properties')
constants = config_per['CONSTANTS']

tmp_path = constants['lambda_tmp_path']

current_date=datetime.now().strftime("%d%m%Y%H%M%S%f")[:-3]
pattern['class_name']= os.path.basename(__file__)
pattern['level']= 'INFO'
pattern['unique_id']= "fc_dtl_per_ext_" + f'{current_date}'


source_path_sftp = None
private_key_sftp = None
sftp_variables_pst_per = None
bk_values = None
sftp_sender = None
transport_layer = None

def ftl_send():
    """
    Connect to IBS Remote server and put the file
    """

    try:
        remote_path = (str(sftp_variables_pst_per["Absolute_path_IBS"])
                       +"/"
                       +str(source_path_sftp[1]))
        download_path_local_314 = str(tmp_path)+source_path_sftp[1]
        s3_client.download_file(source_path_sftp[0], source_path_sftp[1], download_path_local_314)
        sftp_sender.put(download_path_local_314, remote_path)
        sftp_sender.close()
        transport_layer.close()
        log_success_msg(pattern,"INTERFACE - 314 = File has been sent to IBS Remote Server")
        return "314 File has been sent to IBS remote server"
    except Exception as e:
        log_error_msg(pattern,"fc_dtl_per_ext-XML-500-0071",
                      error_codes['fc_dtl_per_ext-XML-500-0071'])
        raise e

def ftl_connection():
    """
    Establish an SFTP connection using Pramiko with SFTP connection variables and private key.
    """
    global sftp_sender
    global transport_layer

    try:
        log_success_msg(pattern,"Connecting IBS Remote Server")
        transport_layer = paramiko.Transport((sftp_variables_pst_per["SFTP_Host_"],
                                              int(sftp_variables_pst_per["SFTP_Port_"])))
        transport_layer.connect(username=sftp_variables_pst_per["SFTP_USR_NAME"],
                                pkey=paramiko.RSAKey.from_private_key(io.StringIO(private_key_sftp))
                                )
        sftp_sender = paramiko.SFTPClient.from_transport(transport_layer)
    except Exception as e:
        log_error_msg(pattern,"fc_dtl_per_ext-XML-500-0007",
                      error_codes['fc_dtl_per_ext-XML-500-0007'])
        raise e

def ftl_access():
    """
    Accessing the configuration file to fetch the information of source and client
    """
    global private_key_sftp
    global source_path_sftp
    global sftp_variables_pst_per

    try:
        log_success_msg(pattern,"Accessing the Env variables")
        source_path_sftp = [bk_values[0],bk_values[1]]
        log_success_msg(pattern,"Getting SFTP Infomation")
        sftp_variables_pst_per = {
            "Absolute_path_IBS" : os.environ['IBS_SFTP_PATH'],
            "SSH_Key" : os.environ['POL_SECRET_ARN'],
            "SFTP_Host_" : os.environ['POL_SFTP_HOST'],
            "SFTP_Port_" : os.environ['POL_SFTP_PORT'],
            "SFTP_USR_NAME" : os.environ['POL_SFTP_USER_NAME'],
            "Region" : os.environ['REGION']
            }
        secret_client_info = boto3.client('secretsmanager',
        region_name=sftp_variables_pst_per["Region"])
        client_key = secret_client_info.get_secret_value(SecretId=sftp_variables_pst_per["SSH_Key"])
        private_key_sftp = client_key['SecretString']
        log_success_msg(pattern,"SFTP Variables values fetched successfully")
    except Exception as e:
        log_error_msg(pattern,"fc_dtl_per_ext-XML-500-0006",
                      error_codes['fc_dtl_per_ext-XML-500-0006'])
        raise e

def ftl_decode():
    """
    retrieves obj from s3 bucket using the s3_client and
    it decodes the content into string and stores in the global variable 'data_string'
    """
    global data_string
    try:
        obj_per = s3_client.get_object(Bucket=bk_values[0], Key=bk_values[1])
        data_string = obj_per['Body'].read().decode()
    except Exception as e:
        log_error_msg(pattern,"fc_dtl_per_ext-XML-500-0003",
                        error_codes['fc_dtl_per_ext-XML-500-0003'])
        raise e

def ftl_info():
    """
    Decoding message and extracting information from SQS
    """
    global bk_values

    try:
        log_success_msg(pattern,"Extracting S3 bucket information and SQS Event information")
        s3_event = json.loads(EVENT['Records'][0]['body'])
        bucket_ = s3_event['Records'][0]['s3']['bucket']['name']
        key_ = s3_event['Records'][0]['s3']['object']['key']
        bk_values = [bucket_,key_]
        log_success_msg(pattern,"Output File: "+str(key_))

    except Exception as e:
        log_error_msg(pattern,"fc_dtl_per_ext-XML-500-0036",
                        error_codes['fc_dtl_per_ext-XML-500-0036'])
        raise e

# checkig file is empty or not
def ftl_check_null():
    """
    checkig file is empty or not
    """
    if not data_string:
        log_error_msg(pattern,"fc_dtl_per_ext-XML-300-0004",
                      error_codes['fc_dtl_per_ext-XML-300-0004'])
        raise ValueError("File is empty")
    #else:
    ftl_access()

def lambda_handler(eve, context):
    """
    Connecting with AWS
    """
    global EVENT
    global lambda_name
    global s3_client
    EVENT = eve
    lambda_name = context.function_name
    s3_client = boto3.client('s3')
    log_success_msg(pattern,"Acquring S3 Service")

    ftl_info()
    ftl_decode()
    ftl_check_null()
    ftl_connection()
    return ftl_send()
