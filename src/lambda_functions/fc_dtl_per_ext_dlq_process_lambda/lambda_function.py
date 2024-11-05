"""_fc_dtl_per_ext_dlq_process_
    Fetches message from SQS and send to S3 bucket
"""
import json
import os
import configparser
from datetime import datetime
import boto3
from src.lambda_functions.common.logger import log_success_msg,log_error_msg, pattern

ERR_PATH = 'src/lambda_functions/common/'
config = configparser.ConfigParser()
config.read(ERR_PATH+'errorcodes.properties')
error_codes = config['ERROR_CODES']
#Disable Pylint for below false positive errors
# pylint: disable=line-too-long, broad-except
def lambda_handler(event, context):
    """main invoking function

    Args:
        event (_json_): Information and talks which resource triggered this lambda
        context (_object_): Contains information about the lambda function

    Returns:
        String: Dead Letter Queue
    """
    print(context.function_name)
    current_date=datetime.now().strftime("%d%m%Y%H%M%S%f")[:-3]
    pattern['class_name']= os.path.basename(__file__)
    pattern['level']= 'INFO'
    pattern['unique_id']= "fc_dtl_per_ext_" + f'{current_date}'

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
            log_error_msg(pattern,"fc_dtl_per_ext-XML-500-0039", error_codes['fc_dtl_per_ext-XML-500-0039'])
            return "Failed"
        try:
            # store the event message in s3 bucket
            bucket_name = os.environ['ERROR_BUCKET_NAME']
            timestamp=(datetime.now()).strftime("%d%m%Y%H%M%S")
            file_name = f"fc-dtl-per-ext_{timestamp}.txt"
            s3 = boto3.client('s3')
            s3.put_object(Bucket=bucket_name, Key=file_name, Body=message_body)
            log_success_msg(pattern,f"Output File Name:{file_name}")
            log_success_msg(pattern,"Message placed successfully on text file")
            return "Dead Letter Queue"
        except Exception:
            log_error_msg(pattern,"fc_dtl_per_ext-XML-500-0003",error_codes['fc_dtl_per_ext-XML-500-0003'])
            return "Failed to put message"
