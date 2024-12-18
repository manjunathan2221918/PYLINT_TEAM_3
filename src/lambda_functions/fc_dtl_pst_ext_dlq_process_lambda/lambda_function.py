"lambda_function"
#Commenting out Pylint false positive error
#pylint: disable=W0718,line-too-long,import-error
import json
import os
import configparser
from datetime import datetime
import boto3
from src.lambda_functions.common.logger import log_success_msg,log_error_msg, pattern

ERROR_PATH_PST = 'src/lambda_functions/common/'
config = configparser.ConfigParser()
config.read(ERROR_PATH_PST+'errorcodes.properties')
error_codes = config['ERROR_CODES']


def lambda_handler(event, context):
    "main lambda function"
    print(context.function_name)
    current_date_=datetime.now().strftime("%d%m%Y%H%M%S%f")[:-3]
    pattern['class_name']= os.path.basename(__file__)
    pattern['level']= 'INFO'
    pattern['unique_id']= "fc-dtl-pst-ext_" + f'{current_date_}'

    for s3_rec_pst in event['Records']:
        try:
            # read sqs message
            message_body_pst = s3_rec_pst['body']
            data=json.loads(message_body_pst)
            bucket = data['Records'][0]['s3']['bucket']['name']
            log_success_msg(pattern,f" Bucket Name: {bucket}")
            file_pst = data['Records'][0]['s3']['object']['key']
            log_success_msg(pattern,f" File Name:{file_pst}")
            log_success_msg(pattern,"SQS Message fetched Successfully")
        except Exception:
            log_error_msg(pattern,"fc_dtl_pst_ext-XML-500-0039", f"{error_codes['fc-dtl-pst-ext-XML-500-0039']}")
            return "Failed"
        try:
            # store the event message in s3 bucket
            bucket_name = os.environ['ERROR_BUCKET_NAME']
            timestamp=(datetime.now()).strftime("%d%m%Y%H%M%S")
            file_name = f"fc-dtl-pst-ext_{timestamp}.txt"
            s3_pst = boto3.client('s3')
            s3_pst.put_object(Bucket=bucket_name, Key=file_name, Body=message_body_pst)
            log_success_msg(pattern,f"Output File Name:{file_name}")
            log_success_msg(pattern,"Message placed successfully on text file")
            return "Dead Letter Queue"
        except Exception:
            log_error_msg(pattern,"fc_dtl_pst_ext-XML-500-0003", f"{error_codes['fc-dtl-pst-ext-XML-500-0003']}")
            return "Failed to put message"
