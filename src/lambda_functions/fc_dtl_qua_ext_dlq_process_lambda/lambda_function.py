"lambda_function"
#Commenting out Pylint false positive error
#pylint: disable=W0718,import-error
import json
import os
import configparser
from datetime import datetime
import boto3
from src.lambda_functions.common.logger import log_success_msg,log_error_msg, pattern

ERROR_PATH = 'src/lambda_functions/common/'
config = configparser.ConfigParser()
config.read(ERROR_PATH+'errorcodes.properties')
error_codes = config['ERROR_CODES']

def lambda_handler(event, context):
    "main lambda function"
    print(context.function_name)
    current_date_qua=datetime.now().strftime("%d%m%Y%H%M%S%f")[:-3]
    pattern['class_name']= os.path.basename(__file__)
    pattern['level']= 'INFO'
    pattern['unique_id']= "fc-dtl-qua-ext_" + f'{current_date_qua}'

    for s3_rec in event['Records']:
        try:
            # read sqs message
            message_body = s3_rec['body']
            data=json.loads(message_body)
            bucket = data['Records'][0]['s3']['bucket']['name']
            log_success_msg(pattern,f" Bucket Name: {bucket}")
            file = data['Records'][0]['s3']['object']['key']
            log_success_msg(pattern,f" File Name:{file}")
            log_success_msg(pattern,"SQS Message fetched Successfully")
        except Exception:
            log_error_msg(pattern,"fc-dtl-qua-ext-XML-500-0039",
                          f"{error_codes['fc-dtl-qua-ext-XML-500-0039']}")
            return "Failed"
        try:
            # store the event message in s3 bucket
            bucket_name = os.environ['ERROR_BUCKET_NAME']
            timestamp=(datetime.now()).strftime("%d%m%Y%H%M%S")
            file_name = f"fc-dtl-qua-ext_{timestamp}.txt"
            s3 = boto3.client('s3')
            s3.put_object(Bucket=bucket_name, Key=file_name, Body=message_body)
            log_success_msg(pattern,f"Output File Name:{file_name}")
            log_success_msg(pattern,"Message placed successfully on text file")
            return "Dead Letter Queue"
        except Exception:
            log_error_msg(pattern,"fc-dtl-qua-ext-XML-500-0003",
                          f"{error_codes['fc-dtl-qua-ext-XML-500-0003']}")
            return "Failed to put message"
