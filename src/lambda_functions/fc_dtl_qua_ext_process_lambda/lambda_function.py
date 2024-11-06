"lambda function"
#Commenting out Pylint false positive error
#pylint: disable=C0301,E1111,global-variable-undefined,import-error
import json
import xml.etree.ElementTree as ET
from datetime import datetime,timezone
import os
import configparser
import uuid
import re
import boto3
from defusedxml.ElementTree import fromstring
from src.lambda_functions.common.logger import log_success_msg,log_error_msg, pattern


ERROR_PATH = 'src/lambda_functions/common/'
CONSTANT_PATH = 'src/lambda_functions/fc_dtl_qua_ext_process_lambda/'
config = configparser.RawConfigParser()
config.read(ERROR_PATH+'errorcodes.properties')
error_codes = config['ERROR_CODES']
config.read(CONSTANT_PATH+'constants.properties')
constants = config['CONSTANTS']


start = constants ['batchstart']
end = constants ['batchend']
schema_version = constants ['schema_Version']
action_type = constants ['action_type']
proprietary_notice=constants['proprietarynotice']
link=constants['link']
batchType=constants['batchType']
originator=constants['originator']
destination=constants['destination']
company= constants ['company']
tenant=constants ["tenant"]
r1=constants['rank1']
rank1=constants['updatedrank1']
r2=constants['rank2']
rank2=constants['updatedrank2']
DECLARATION='<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
MESSAGE_REFERENCE=str(uuid.uuid4())
BATCH_REFERENCE=str(uuid.uuid4())

def create_timestamp(current_timestamp):
    "function to replace utc variance"
    return current_timestamp.isoformat(timespec='milliseconds').replace('+00:00', 'Z')

def add_declaration(element):
    "function to add declaration"
    return DECLARATION+ET.tostring(element, encoding='utf-8').decode('utf-8')

def batch(action):
    "function for batchdetails"
    return ET.Element ("batchDetails",{
                'schemaVersion': schema_version,
                'actionType': action,
                'messageReference':MESSAGE_REFERENCE,
                'batchReference':BATCH_REFERENCE,
                'timestamp': create_timestamp(datetime.now(timezone.utc)),
                'originator': originator,
                'destination': destination,
                'company':company,
                'tenant': tenant,
                "proprietaryNotice":proprietary_notice,
                "xmlns":link
                })

def crew_header():
    "function for crew details"
    return ET.Element('crewDetails',{
        'schemaVersion':schema_version,
        'actionType':action_type,
        'messageReference':"CREW_SCHED_"+str(datetime.now(timezone.utc).timestamp()),
        'timestamp':create_timestamp(datetime.now(timezone.utc)),
        'originator':originator,
        'destination': destination,
        "proprietaryNotice":proprietary_notice ,
        "xmlns": link
        })

def main_function(bucket,key):
    "function to connect with s3 using bucket name and filename we got from SQS event message"
    try:
        obj = s3_client.get_object(Bucket=bucket, Key=key)
        data_string = obj['Body'].read().decode()
    except Exception as e:
        log_error_msg(pattern,"fc-dtl-qua-ext-XML-500-0003",error_codes['fc-dtl-qua-ext-XML-500-0003'])
        raise e

    #check the file having any data
    if not data_string:
        log_error_msg(pattern,"fc-dtl-qua-ext-XML-300-0004", f"{error_codes['fc-dtl-qua-ext-XML-300-0004']} no data present in the file")
        raise ValueError('File is empty')
    log_success_msg(pattern,"File has Valid data")
    root =fromstring(data_string)
    crew_details=[]

    #batch Header
    batchstart=batch(start)
    ET.SubElement(batchstart,'batchType').text=batchType
    crew_details.append(batchstart)

    #crewdetails part
    crew_iterator = crew_iterate(root,crew_details)

    #Batch End part
    batchend=batch(end)
    ET.SubElement(batchend,'batchType').text=batchType
    messagecount=len(crew_details) + 1
    ET.SubElement(batchend,'totalMessageCount').text=str(messagecount)
    crew_details.append(batchend)

    #if message count is more than 2 (batchstart,batch end), it will create a output xml file
    file_write(messagecount,crew_details)
    return_main = [str(batchstart), str(crew_iterator),str(batchend), "File Processing Complete"]
    return return_main

#iterate every crew present in the input file and map it to the respective field
def crew_iterate(root,crew_details):
    "function to iterate every crew"
    for item in root.findall('FlightCrewData'):
        crewdetails=crew_header()

        #check crew id field is having valid data
        if item.find('crewId').text == 'None':
            log_error_msg(pattern,"fc-dtl-qua-ext-XML-300-0005" , f"{error_codes['fc-dtl-qua-ext-XML-300-0005']} - CrewId field is None")
            continue

        crew_id=item.find('crewId').text
        crew_info = ET.SubElement(crewdetails, 'crewInfo',{'crewId':crew_id})

        #check mandatory fields are present in each section

        if process_qualification_info(item, crew_info, crew_id):
            continue
        if process_license_info(item, crew_info, crew_id):
            continue

        crew_details.append(crewdetails)

def process_qualification_info(item, crew_info, crew_id):
    "function to mandatory check for qualification"
    qualificationcode_list = item.findall('qualificationCode')
    elements = list(item)

    if all(ac.text !='None' for ac in qualificationcode_list):
        if qualificationcode_list:
            qualifications = ET.SubElement(crew_info, 'qualifications')
            qualification_tag_creation(elements,qualifications)
        return False
    log_error_msg(pattern,"fc-dtl-qua-ext-XML-300-0006" , f"{error_codes['fc-dtl-qua-ext-XML-300-0006']} crew id: {crew_id} qualification Code field is None")
    return True

def transform_fleet_type(fleet_type):
    "function to tranform fleet"
    return '' if fleet_type in ["Ascend", "None"] else re.sub(r'[^\d]', '', fleet_type)

def transform_rank(rank):
    "function to transform rank"
    return {r1:rank1, r2:rank2}.get(rank, '')

def qualification_tag_creation(elements,qualifications):
    "function to create qualification tag"
    i=0
    while i < len(elements):
        if elements[i].tag == 'qualificationCode':
            qualification_code=elements[i].text
            rank=elements[i+3].text
            transformed_rank=transform_rank(rank)
            fleet_type=elements[i+4].text
            split_fleet=fleet_type.split('/')
            for fleet in split_fleet:
                transformed_fleet_type=transform_fleet_type(fleet)
                modified_qual=transformed_rank+transformed_fleet_type+qualification_code
                qualification = ET.SubElement(qualifications, 'qualification', {"actionType":action_type})
                ET.SubElement(qualification, 'qualificationCode').text = modified_qual
                if elements[i + 1].text !='None':
                    ET.SubElement(qualification, 'fromDate').text =elements[i + 1].text
                if elements[i + 2].text !='None':
                    ET.SubElement(qualification, 'toDate').text =elements[i + 2].text
        i += 1

def process_license_info(item, crew_info, crew_id):
    "function to mandatory check for license elements"
    licence_list = item.findall('licenseCode')
    mandatory_fields = ['licenseCode', 'licenseNumber', 'issueDate', 'effectiveDate', 'expiryDate']
    if len(licence_list)==0:
        return False
    if all(item.find(field).text !='None' for field in mandatory_fields):
        license_tag_creation(crew_info, item)
        return False
    license_error_logging(item, crew_id)
    return True

def license_tag_creation(crew_info,item):
    "function to create licence tag"
    licenses = ET.SubElement(crew_info, 'licenses')
    licence = ET.SubElement(licenses, 'license',{"actionType":action_type})
    ET.SubElement(licence, 'licenseCode').text = item.find('licenseCode').text
    ET.SubElement(licence, 'licenseNumber').text = item.find('licenseNumber').text
    ET.SubElement(licence, 'issueDate').text = item.find('issueDate').text
    ET.SubElement(licence, 'effectiveDate').text = item.find('effectiveDate').text
    ET.SubElement(licence, 'expiryDate').text = item.find('expiryDate').text

def license_error_logging(item,crew_id):
    "function to log error for license section"
    mandatory_fields=['licenseCode', 'licenseNumber', 'issueDate', 'effectiveDate', 'expiryDate']
    for field in mandatory_fields:
        if item.find(field).text == 'None':
            log_error_msg(pattern, "fc-dtl-qua-ext-XML-300-0007", f"{error_codes['fc-dtl-qua-ext-XML-300-0007']}, crew id: {crew_id}  {field} field is  None")

def file_write(messagecount,crew_details):
    "function to send file to output s3"
    if messagecount>2:
        try:
            formatted_date=datetime.now().strftime("%d%m%Y%H%M%S")
            output_content = '\n'.join(add_declaration(cr) for cr in crew_details)
            filename="CrewQualifications_"+ f'{formatted_date}' + ".xml"
            s3_client.put_object(Bucket=os.environ['OUTPUT_BUCKET_NAME'],Key=filename,Body=output_content)
            log_success_msg(pattern,f"Output File Name:{filename}")
            log_success_msg(pattern,"File placed successfully in output S3")
        except Exception as e:
            log_error_msg(pattern,"fc-dtl-qua-ext-XML-500-0039", error_codes['fc-dtl-qua-ext-XML-500-0039'])
            raise e
    else:
        log_success_msg(pattern,"No Crew Records found in the file")

def lambda_handler(event, context):
    """main function

    Args:
        event (_type_): _description_
        context (_type_): _description_

    Raises:
        "function will start once lambda invoked"

    Returns:
        _type_: _description_
    """
    global s3_client
    print(context.function_name)
    #setting syntax for logger
    current_date=datetime.now().strftime("%d%m%Y%H%M%S%f")[:-3]
    pattern['class_name']= os.path.basename(__file__)
    pattern['level']= 'INFO'
    pattern['unique_id']= "fc-dtl-qua-ext_" + f'{current_date}'
    s3_client = boto3.client('s3')

    try:
        #Read SQS message
        s3_event = json.loads(event['Records'][0]['body'])
        log_success_msg(pattern,"SQS Message fetched Successfully")
        bucket = s3_event['Records'][0]['s3']['bucket']['name']
        log_success_msg(pattern,f"Bucket_Name:{bucket}")
        key = s3_event['Records'][0]['s3']['object']['key']
        log_success_msg(pattern,f"File_Name:{key}")
    except Exception as e:
        log_error_msg(pattern,"fc-dtl-qua-ext-XML-500-0036" , error_codes['fc-dtl-qua-ext-XML-500-0036'])
        raise e
    caller_main = main_function(bucket,key)
    return_message = [caller_main, 'Values Fetched and Processed']
    return return_message
