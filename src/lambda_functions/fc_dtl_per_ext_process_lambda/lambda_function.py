"lambda function"
#Commenting out Pylint false positive error
#pylint: disable=C0301,E1111,global-variable-undefined,import-error
import json
import xml.etree.ElementTree as ET
from datetime import datetime,timezone
import os
import configparser
import uuid
import boto3
from defusedxml.ElementTree import fromstring
from src.lambda_functions.common.logger import log_success_msg,log_error_msg, pattern


ERROR_PATH = 'src/lambda_functions/common/'
CONSTANT_PATH = 'src/lambda_functions/fc_dtl_per_ext_process_lambda/'
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
airline=constants['airline']
destination=constants['destination']
company= constants ['company']
tenant=constants ["tenant"]

MESSAGE_REFERENCE=str(uuid.uuid4())
BATCH_REFERENCE=str(uuid.uuid4())


def transform_date(date_str):
    "function to transfrm date"
    date_obj= datetime.strptime(date_str,'%d-%b-%Y')
    return date_obj.strftime('%Y-%m-%d')

def create_timestamp(current_timestamp):
    "function to create timestamp"
    formatted_timestamp = current_timestamp.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    return formatted_timestamp

def element_string(element):
    "function to add declaration"
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'+ET.tostring(element, encoding='utf-8').decode('utf-8')

def batch(action):
    "function to add batch deatils"
    return ET.Element ("batchDetails",{
                'schemaVersion': schema_version,
                'actionType': action,
                'messageReference':MESSAGE_REFERENCE,
                'batchReference':BATCH_REFERENCE,
                'timestamp': create_timestamp(datetime.now(timezone.utc)),
                'originator': originator,
                'company':company,
                'tenant': tenant,
                'destination': destination,
                "proprietaryNotice":proprietary_notice,
                "xmlns":link
                })

def crew_header():
    "function to add crewdetails"
    return ET.Element('crewDetails',{
        'schemaVersion':schema_version,
        'actionType':action_type,
        'messageReference':"CREW_SCHED_"+str(datetime.now(timezone.utc).timestamp()),
        'timestamp':create_timestamp(datetime.now(timezone.utc)),
        'originator':originator,
        "proprietaryNotice":proprietary_notice ,
        "xmlns": link
        })

def main_function(s3_event):
    "main function"
    try:
        bucket = s3_event['Records'][0]['s3']['bucket']['name']
        log_success_msg(pattern,f" Bucket Name: {bucket}")
        key = s3_event['Records'][0]['s3']['object']['key']
        log_success_msg(pattern,f" File Name:{key}")

        #Reads S3 file data
        obj = s3_client.get_object(Bucket=bucket, Key=key)
        data_string = obj['Body'].read().decode()
        log_success_msg(pattern,"New File fetched from Input s3 Successfully ")
    except Exception as e:
        print(e)
        log_error_msg(pattern,"fc_dtl_per_ext-XML-500-0003", error_codes['fc_dtl_per_ext-XML-500-0003'])
        raise e

    if not data_string:
        log_error_msg(pattern,"fc_dtl_per_ext-XML-300-0004", error_codes['fc_dtl_per_ext-XML-300-0004'])
        raise ValueError('File is empty')
    log_success_msg(pattern,"File has Valid data")
    root =fromstring(data_string)
    crew_details=[]

    #Batch Header part
    batchstart=batch(start)
    ET.SubElement(batchstart,'batchType').text=batchType
    crew_details.append(batchstart)

    # crewdetails part
    crew_iterator = crew_iterate(root,key,crew_details)

    #Batch End part
    batchend=batch(end)
    messagecount=len(crew_details)+1
    ET.SubElement(batchend,'batchType').text=batchType
    ET.SubElement(batchend,'totalMessageCount').text=str(messagecount)

    crew_details.append(batchend)

    #checks any valid crew count
    file_write(messagecount,crew_details)
    return_main = [str(batchstart), str(crew_iterator),str(batchend), "File Processing Complete"]
    return return_main

def crew_iterate(root,key,crew_details):
    "function to iterate every crew"
    for item in root.findall('FlightCrewData'):
        crewdetails=crew_header()

        #check crew id field is present or not
        if item.find('CrewId') is None or item.find('CrewId').text is None:
            log_error_msg(pattern,"fc_dtl_per_ext-XML-300-0005",error_codes['fc_dtl_per_ext-XML-300-0005'])
            continue

        crew_id=item.find('CrewId').text
        crew_info = ET.SubElement(crewdetails, 'crewInfo',{'crewId':crew_id})

        #check mandatory fields are present
        if process_personal_info(item, crew_info, crew_id, key):
            continue
        if process_employment_info(item, crew_info, crew_id):
            continue
        if process_appointment_info(item, crew_info, crew_id,):
            continue
        if process_seniority_info(item, crew_info, crew_id):
            continue

        crew_details.append(crewdetails)

def log_error_and_continue(error_code, crew_id, message):
    "functiont to log error"
    log_error_msg(pattern,error_code, f"{error_codes[error_code]} crew_id: {crew_id} {message}")
    return True

def process_personal_info(item, crew_info, crew_id,key):
    "function to check mandatory elements for personal info"
    mandatory_fields = ['FirstName', 'LastName', 'Gender', 'DateOfBirth', 'JoiningDate']
    if check_mandatory_fields(item, mandatory_fields):
        personal_tag_creation(crew_info, item, key)
    elif not any(item.find(field) is not None for field in mandatory_fields):
        optional_fields = ['CrewCode', 'CalledName', 'PlaceofBirth', 'CountryOfBirth', 'FlyingSinceDate', 'LastPromotionDate']
        if any(item.find(field) is not None for field in optional_fields):
            personal_error_logging(item, crew_id)
            return True
    else:
        personal_error_logging(item, crew_id)
        return True
    return False

def process_employment_info(item, crew_info, crew_id):
    "function to check mandatory elements for employment info "
    if item.find('AirlineCode') is not None and item.find('AirlineCode').text is not None:
        employment_tag_creation(crew_info, item)
    else:
        if any(item.find(field) is not None for field in ['EmploymentStartDate', 'EmploymentEndDate']):
            return log_error_and_continue('fc_dtl_per_ext-XML-300-0007', crew_id, "AirlineCode field is either None or Not available")
    return False

def process_appointment_info(item, crew_info, crew_id):
    "function to check mandatory elements for appointment info"
    appointment_list = item.findall('AppointmentCode')
    startdatelist = item.findall('AppointmentStartDate')
    enddatelist = item.findall('AppointmentEndDate')
    allvalid = all(ac.text for ac in appointment_list)
    elements = list(item)

    if not appointment_list and (startdatelist or enddatelist):
        return log_error_and_continue('fc_dtl_per_ext-XML-300-0008', crew_id, "AppointmentCode field is either None or Not available")
    if allvalid:
        if appointment_list:
            appointments = ET.SubElement(crew_info, 'appointments')
            appointment_tag_creation(elements,appointments)
    else:
        return log_error_and_continue('fc_dtl_per_ext-XML-300-0008', crew_id, "AppointmentCode field is either None or Not available")
    return False

def process_seniority_info(item, crew_info, crew_id):
    "function to check mandatory elements for seniority info"
    if item.find('SeniorityNumber') is not None and item.find('SeniorityNumber').text is not None:
        seniority_tag_creation(crew_info, item)
    else:
        if any(item.find(field) is not None for field in ['SeniorityFromDate', 'SeniorityEndDate']):
            return log_error_and_continue('fc_dtl_per_ext-XML-300-0009', crew_id, "SeniorityNumber field is either None or Not available")
    return False

def check_mandatory_fields(item, fields):
    "function for mandatory check"
    return all(item.find(field) is not None and item.find(field).text is not None for field in fields)

def personal_error_logging(item,crew_id):
    "function for personal error logging"
    mandatory_fields=["FirstName","LastName","Gender","DateOfBirth","JoiningDate"]
    for field in mandatory_fields:
        if item.find(field) is None:
            log_error_msg(pattern,"fc_dtl_per_ext-XML-300-0006", f"{error_codes['fc_dtl_per_ext-XML-300-0006']}, crew id:{crew_id}  {field} field is Not available")
        elif item.find(field).text is None:
            log_error_msg(pattern,"fc_dtl_per_ext-XML-300-0006", f"{error_codes['fc_dtl_per_ext-XML-300-0006']}, crew id: {crew_id}  {field} field is  None")

def personal_tag_creation(crew_info,item,key):
    "function for personal tag creation"
    personal_info = ET.SubElement(crew_info, 'personalInfo')
    if (item.find('CrewCode') is not None and item.find('CrewCode').text is not None):
        ET.SubElement(personal_info, 'searchName').text = item.find('CrewCode').text
    else:
        first_name=(item.find('FirstName').text).upper()
        last_name=(item.find('LastName').text).upper()
        crew_code=first_name[0:4]+last_name[0]
        ET.SubElement(personal_info, 'searchName').text =crew_code
    ET.SubElement(personal_info, 'firstName').text = item.find('FirstName').text
    ET.SubElement(personal_info, 'lastName').text = item.find('LastName').text
    if (item.find('CalledName') is not None and item.find('CalledName').text is not None):
        ET.SubElement(personal_info, 'calledName').text = item.find('CalledName').text
    ET.SubElement(personal_info, 'gender').text = item.find('Gender').text
    ET.SubElement(personal_info, 'crewType').text = key[9].upper()
    ET.SubElement(personal_info, 'dateOfBirth').text =transform_date(item.find('DateOfBirth').text)
    if (item.find('PlaceofBirth') is not None and item.find('PlaceofBirth').text is not None ):
        ET.SubElement(personal_info, 'placeOfBirth').text = item.find('PlaceofBirth').text
    if (item.find('CountryOfBirth') is not None and item.find('CountryOfBirth').text is not None ):
        ET.SubElement(personal_info, 'countryOfBirth').text = item.find('CountryOfBirth').text
    ET.SubElement(personal_info, 'joiningDate').text =transform_date(item.find('JoiningDate').text)
    if (item.find('FlyingSinceDate') is not None and item.find('FlyingSinceDate').text is not None ):
        ET.SubElement(personal_info, 'flyingSinceDate').text =transform_date( item.find('FlyingSinceDate').text)
    if (item.find('LastPromotionDate')  is not None and item.find('LastPromotionDate').text is not None ):
        ET.SubElement(personal_info, 'lastPromotionDate').text =transform_date( item.find('LastPromotionDate').text)

def employment_tag_creation(crew_info,item):
    "function for employment tag creation"
    employments = ET.SubElement(crew_info, 'employments')
    employment = ET.SubElement(employments, 'employment',{"actionType":action_type})
    ET.SubElement(employment, 'crewId').text = item.find('CrewId').text
    ET.SubElement(employment, 'airlineCode').text = airline
    if (item.find('EmploymentStartDate') is not None and item.find('EmploymentStartDate').text is not None):
        ET.SubElement(employment, 'fromDate').text = transform_date(item.find('EmploymentStartDate').text)
    if (item.find('EmploymentEndDate') is not None and item.find('EmploymentEndDate').text is not None):
        ET.SubElement(employment, 'toDate').text = transform_date(item.find('EmploymentEndDate').text)

def appointment_tag_creation(elements,appointments):
    "function for appointment tag creation"
    i=0
    while i < len(elements):
        if elements[i].tag == 'AppointmentCode':
            appointment = ET.SubElement(appointments, 'appointment', {"actionType": action_type})
            ET.SubElement(appointment, 'appointmentCode').text = elements[i].text

            # Check and add AppointmentStartDate
            if i + 1 < len(elements) and elements[i + 1].tag == 'AppointmentStartDate' and elements[i + 1].text:
                ET.SubElement(appointment, 'fromDate').text = transform_date(elements[i + 1].text)

            # Check and add AppointmentEndDate
            if i + 1 < len(elements) and elements[i + 1].tag == 'AppointmentEndDate' and elements[i + 1].text:
                ET.SubElement(appointment, 'toDate').text = transform_date(elements[i + 1].text)
            elif i + 2 < len(elements) and elements[i + 2].tag == 'AppointmentEndDate' and elements[i + 2].text:
                ET.SubElement(appointment, 'toDate').text = transform_date(elements[i + 2].text)
        i += 1

def seniority_tag_creation(crew_info,item):
    "function for seniority tag creation"
    seniorities = ET.SubElement(crew_info, 'seniorities')
    seniority = ET.SubElement(seniorities, 'seniority',{"actionType":action_type})
    ET.SubElement(seniority, 'seniorityNumber').text = item.find('SeniorityNumber').text
    if (item.find('SeniorityFromDate') is not None and item.find('SeniorityFromDate').text is not None ):
        ET.SubElement(seniority, 'fromDate').text = transform_date(item.find('SeniorityFromDate').text)
    if (item.find('SeniorityEndDate') is not None and item.find('SeniorityEndDate').text is not None ):
        ET.SubElement(seniority, 'toDate').text = transform_date(item.find('SeniorityEndDate').text)

def file_write(messagecount,crew_details):
    "function to write in output s3"
    if messagecount>2:
        try:
            formatted_date=datetime.now().strftime("%d%m%Y%H%M%S%f")[:-3]
            output_content = '\n'.join(element_string(cr) for cr in crew_details)
            filename="CrewDetails_"+ f'{formatted_date}' + ".xml"
            bucket_name_env = os.environ['OUTPUT_BUCKET_NAME']
            s3_client.put_object(Bucket=bucket_name_env,Key=filename,Body=output_content)
            log_success_msg(pattern,"File placed successfully in output S3")
            log_success_msg(pattern,f"Output File Name:{filename}")
        except Exception as e:
            log_error_msg(pattern,"fc_dtl_per_ext-XML-500-0039",error_codes['fc_dtl_per_ext-XML-500-0039'])
            raise e

def lambda_handler(event, context):
    "main lambda function"
    global s3_client
    print(context.function_name)
    current_date=datetime.now().strftime("%d%m%Y%H%M%S%f")[:-3]
    pattern['class_name']= os.path.basename(__file__)
    pattern['level']= 'INFO'
    pattern['unique_id']= "fc-dtl-per-ext_" + f'{current_date}'
    try:
        #Read SQS message
        s3_event = json.loads(event['Records'][0]['body'])
        log_success_msg(pattern,"SQS Message fetched Successfully")
    except Exception as e:
        log_error_msg(pattern,"fc_dtl_per_ext-XML-500-0036",error_codes['fc_dtl_per_ext-XML-500-0036'])
        raise e

    s3_client = boto3.client('s3')
    caller_main = main_function(s3_event)
    return_message_db_connect = [caller_main, 'Values Fetched and Processed']
    return return_message_db_connect
