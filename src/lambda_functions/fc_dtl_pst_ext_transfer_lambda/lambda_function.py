"""_summary_

    file Transfer lambda
    """
# pylint: disable=global-variable-undefined,line-too-long,import-error
import json
import os
import configparser
from datetime import datetime
import io
import paramiko
import boto3

from src.lambda_functions.common.logger import log_success_msg,log_error_msg, pattern

#Error Codes properties
ERR_PATH = 'src/lambda_functions/common/'
CONS_PATH = 'src/lambda_functions/fc_dtl_pst_ext_transfer_lambda/'

config = configparser.ConfigParser()
config.read(ERR_PATH+'errorcodes.properties')
error_codes = config['ERROR_CODES']

config.read(CONS_PATH+'constants.properties')
constants = config['CONSTANTS']

tmp_path = constants['lambda_tmp_path']
current_date=datetime.now().strftime("%d%m%Y%H%M%S%f")[:-3]
pattern['class_name']= os.path.basename(__file__)
pattern['level']= 'INFO'
pattern['unique_id']= "fc-dtl-pst-ext_" + f'{current_date}'


def send():
    """_summary_

    Connect to IBS Remote server and put the file
    """
    try:
        remote_path = (str(sftp_variables["Destination_absolute_path_IBS"])
                       +"/"+
                       str(source_path_sftp[1]))
        download_path = str(tmp_path)+source_path_sftp[1]
        s3_client.download_file(source_path_sftp[0], source_path_sftp[1], download_path)
        sftp_sender.put(download_path, remote_path)
        sftp_sender.close()
        transport_layer.close()
        log_success_msg(pattern,"INTERFACE-318 = File has been sent to IBS Remote Server")
        return "318 File has been sent to IBS remote server"
    except Exception as e:
        log_error_msg(pattern,"fc_dtl_pst_ext-XML-500-0071",
                      error_codes['fc_dtl_pst_ext-XML-500-0071'])
        raise e

def connection():
    """_summary_

    Connecting to sftp
    """
    try:
        log_success_msg(pattern,"Connecting IBS Remote Server")
        global transport_layer
        transport_layer = paramiko.Transport((sftp_variables["SFTP_Host"],
                                              int(sftp_variables["SFTP_Port"])))
        transport_layer.connect(username=sftp_variables["SFTP_USR_NAME"],
                                pkey=paramiko.RSAKey.from_private_key(io.StringIO(private_key_sftp))
                                )
        global sftp_sender
        sftp_sender = paramiko.SFTPClient.from_transport(transport_layer)
    except Exception as e:
        log_error_msg(pattern,"fc_dtl_pst_ext-XML-500-0007",
                      error_codes['fc_dtl_pst_ext-XML-500-0007'])
        raise e

def access():
    """_summary_

    Accessing the configuration file to fetch the information of source and client  
    """
    try:
        log_success_msg(pattern,"Accessing the Env variables")
        global source_path_sftp
        source_path_sftp = [bk_values[0],bk_values[1]]
        log_success_msg(pattern,"Getting SFTP Infomation")
        global sftp_variables
        sftp_variables = {
            "Destination_absolute_path_IBS" : os.environ['IBS_SFTP_PATH'],
            "SSH_Key" : os.environ['POL_SECRET_ARN'],
            "SFTP_Host" : os.environ['POL_SFTP_HOST'],
            "SFTP_Port" : os.environ['POL_SFTP_PORT'],
            "SFTP_USR_NAME" : os.environ['POL_SFTP_USER_NAME'],
            "Region" : os.environ['REGION']
            }
        secret_client_info = boto3.client('secretsmanager', region_name=sftp_variables["Region"])
        client_private_key = secret_client_info.get_secret_value(SecretId=sftp_variables["SSH_Key"])
        global private_key_sftp
        private_key_sftp = client_private_key['SecretString']
        log_success_msg(pattern,"SFTP Variables values fetched successfully")
    except Exception as e:
        log_error_msg(pattern,"fc_dtl_pst_ext-XML-500-0006",
                      error_codes['fc_dtl_pst_ext-XML-500-0006'])
        raise e

def decode():
    """_summary_

   decode
    """
    try:
        obj = s3_client.get_object(Bucket=bk_values[0], Key=bk_values[1])
        global data_string
        data_string = obj['Body'].read().decode()
    except Exception as e:
        log_error_msg(pattern,"fc_dtl_pst_ext-XML-500-0003",
                        error_codes['fc_dtl_pst_ext-XML-500-0003'])
        raise e

def info():
    """_summary_

   Decoding message and extracting information from SQS
    """
    try:
        log_success_msg(pattern,"Extracting S3 bucket information and SQS Event information")
        s3_event = json.loads(event['Records'][0]['body'])
        bucket = s3_event['Records'][0]['s3']['bucket']['name']
        key = s3_event['Records'][0]['s3']['object']['key']
        global bk_values
        bk_values = [bucket,key]
        log_success_msg(pattern,"Output File: "+str(key))

    except Exception as e:
        log_error_msg(pattern,"fc_dtl_pst_ext-XML-500-0036",
                        error_codes['fc_dtl_pst_ext-XML-500-0036'])
        raise e


def check_null():
    """_summary_

    checking file is empty or not
    """
    if not data_string:
        log_error_msg(pattern,"fc_dtl_pst_ext-XML-300-0004",
                      error_codes['fc_dtl_pst_ext-XML-300-0004'])
        raise ValueError("File is empty")
    #else:
    access()

def lambda_handler(eve, context):
    """_summary_

    main function
        
    """
    global event, lambda_name
    event = eve
    lambda_name = context.function_name
    #Connecting with AWS
    log_success_msg(pattern,"Acquring S3 Service")

    global s3_client
    s3_client = boto3.client('s3')

    info()
    decode()
    check_null()
    connection()
    return send()
