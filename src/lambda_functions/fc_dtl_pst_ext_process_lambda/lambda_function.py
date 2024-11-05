"lambda function"
import json
from datetime import datetime,timezone
import os
import configparser
import uuid
import re
import boto3
from xsdata.formats.dataclass.serializers import XmlSerializer
from src.lambda_functions.fc_dtl_pst_ext_process_lambda.generated.crew_details import CrewDetails
from src.lambda_functions.fc_dtl_pst_ext_process_lambda.generated.batch_details import BatchDetails
from src.lambda_functions.fc_dtl_pst_ext_process_lambda.generated.meta_data import ActionTypes
from src.lambda_functions.fc_dtl_pst_ext_process_lambda.generated.crew_general_types import CrewPostings,CrewInfo
from src.lambda_functions.common.logger import log_success_msg,log_error_msg, pattern

#Commenting out Pylint false positive error
#pylint: disable=C0301,R0913,R0917

#getting values from constant properties file
ERROR_PATH = 'src/lambda_functions/common/'
CONSTANT_PATH = 'src/lambda_functions/fc_dtl_pst_ext_process_lambda/'
config = configparser.RawConfigParser()
config.read(ERROR_PATH+'errorcodes.properties')
error_codes = config['ERROR_CODES']
config.read(CONSTANT_PATH+'constants.properties')
constants = config['CONSTANTS']

batchType=constants['batchType']
originator=constants['originator']
destination=constants['destination']
company=constants['company']
tenant=constants['tenant']
r1=constants['rank1']
rank1=constants['updatedrank1']
r2=constants['rank2']
rank2=constants['updatedrank2']
ignored_base=constants['ignoredbase']
MESSAGE_REFERENCE=str(uuid.uuid4())
BATCH_REFERENCE=str(uuid.uuid4())
serializer=XmlSerializer()


def create_timestamp(current_timestamp):
    "function to create timestamp"
    return current_timestamp.isoformat(timespec='milliseconds').replace('+00:00', 'Z')

def transform_rank(rank):
    "function to transform rank"
    return {r1:rank1, r2:rank2}.get(rank, '')
def transform_date(batch_date):
    "function to transform date"
    return datetime.strptime(batch_date,'%d-%b-%Y').strftime('%Y-%m-%d')

def isalpha_check(value):
    "function to check character"
    if value.isdigit() or (any(char.isdigit() for char in value) and any(char.isalpha() for char in value)):
        return True
    return False

def create_batch_details(action, messagecount=None):
    "function to create batchdetails"
    batch_details = BatchDetails(
    batch_type=batchType,
    action_type=action,
    message_reference=MESSAGE_REFERENCE,
    batch_reference=BATCH_REFERENCE,
    timestamp=create_timestamp(datetime.now(timezone.utc)),
    originator=originator,
    destination=destination,
    company=company,
    tenant=tenant
    )
    if messagecount is not None:
        batch_details.total_message_count = int(messagecount) + 2
    return batch_details

def crewdetails_function(crew_info):
    "function to create crewdetails"
    crew_details = CrewDetails(
    action_type=ActionTypes.UPDATE,
    message_reference="CREW_SCHED_"+str(datetime.now(timezone.utc).timestamp()),
    timestamp=create_timestamp(datetime.now(timezone.utc)),
    originator=originator,
    destination=destination,
    crew_info=[crew_info]
    )
    return crew_details

def send_object_to_s3(messagecount,final_list):
    "function to send file to s3"
    if messagecount>0:
        try:
            formatted_date=datetime.now().strftime("%d%m%Y%H%M%S")
            filename="Crew_Postings_"+ f'{formatted_date}' + ".xml"
            s3_client.put_object(Bucket=os.environ['OUTPUT_BUCKET_NAME'],Key=filename,Body=final_list)
            log_success_msg(pattern,f"Output File Name:{filename}")
            log_success_msg(pattern,"File placed successfully in output S3")
            return "File Processed"
        except Exception as e:
            log_error_msg(pattern,"fc-dtl-pst-ext-XML-500-0039" ,f"{error_codes['fc-dtl-pst-ext-XML-500-0039']}")
            raise e
    else:
        log_success_msg(pattern,"No Crew Records found in the file")
        return "File processed without crew"


def add_crewdetails(crew_id,valid_crew,crew_posting,overall_field_list):
    "function to crewdetails"
    if valid_crew:
        crew_postings = CrewPostings(posting=crew_posting)
        crew_info = CrewInfo(postings=crew_postings,crew_id=crew_id)
        crew_details= crewdetails_function(crew_info)
        overall_field_list+= serializer.render(crew_details)
    return overall_field_list

def error_logging(base_value,fleet_value,rank_value,crew_id):
    "function to error logging"
    field_names = ['Base', 'Fleet', 'Rank']
    field_values = [base_value, fleet_value, rank_value]
    for field_name, field_value in zip(field_names, field_values):
        if not field_value:
            log_error_msg(pattern,"fc-dtl-pst-ext-XML-300-0006" ,f"{error_codes['fc-dtl-pst-ext-XML-300-0006']} crew id: {crew_id} {field_name} value is not available")

def mandatory_check(base_value,fleet_value,rank_value,crew_id,from_date_value,to_date_value,crew_posting,valid_crew):
    "function to mandatory check"
    if base_value=="---":
        log_error_msg(pattern,"fc-dtl-pst-ext-XML-300-0006" ,f"{error_codes['fc-dtl-pst-ext-XML-300-0006']} crew id: {crew_id} base value '---' is not valid")
        valid_crew = False
    elif (base_value and fleet_value and rank_value):
        post_data=CrewPostings.Posting(
            base=base_value,
            fleet=fleet_value,
            rank=rank_value,
            from_date=transform_date(from_date_value) if from_date_value else None,
            to_date=transform_date(to_date_value) if to_date_value else None,
            action_type=ActionTypes.UPDATE
        )
        crew_posting.append(post_data)
    else:
        error_logging(base_value,fleet_value,rank_value,crew_id)
        valid_crew = False
    return valid_crew
def postingcd_check(records,crew_posting,crew_id,overall_field_list,valid_crew):
    "function to postingcd check"
    for record in records:
        base_value=record["base"]
        fleet=record['fleet']
        fleet_value=fleet if isalpha_check(fleet) else ''
        rank_value=transform_rank(record['rank'])
        from_date_value=record["from_date"]
        to_date_value=record["to_date"]

        valid_crew=mandatory_check(base_value,fleet_value,rank_value,crew_id,from_date_value,to_date_value,crew_posting,valid_crew)
        if valid_crew is False:
            break
    overall_field_list=add_crewdetails(crew_id,valid_crew,crew_posting,overall_field_list)
    return overall_field_list
#check crew id have null value or not
def crew_id_check(crew_dict,overall_field_list):
    "function to check crew id"
    for crew_id, records in crew_dict.items():
        if not crew_id:
            log_error_msg(pattern,"fc-dtl-pst-ext-XML-300-0005", error_codes['fc-dtl-pst-ext-XML-300-0005'])
        else:
            crew_posting=[]
            valid_crew=True
            overall_field_list=postingcd_check(records,crew_posting,crew_id,overall_field_list,valid_crew)
    return overall_field_list
#create dict for lst data
def create_crewdict(lst_data):
    "creating crew dict from lst file"
    ignored_base_list=ignored_base.split(',')
    crewdata_dict = {}
    for post in lst_data[:-2]:
        crew_id=post[76:86].strip()
        base=post[6:9].strip()
        if base not in ignored_base_list:
            posting_data = {
                'rank':post[0:1].strip(),
                'fleet':post[2:5].strip(),
                'base':base,
                'from_date':post[91:102].strip(),
                'to_date':post[117:128].strip()
            }
            crewdata_dict.setdefault(crew_id, []).append(posting_data)
    return crewdata_dict

def mainfunction(lst_data):
    "main function"
    crew_dict=create_crewdict(lst_data)
    overall_field_list=serializer.render(create_batch_details(ActionTypes.START))
    overall_field_list= crew_id_check(crew_dict,overall_field_list)
    messagecount = len(re.findall(r'<ns0:crewDetails\b[^>]*>', overall_field_list))
    overall_field_list += serializer.render(create_batch_details(ActionTypes.END, messagecount))
    overall_field_list = overall_field_list.replace("ns0:", "").replace(":ns0", "")
    split_list = overall_field_list.split('<?xml version="1.0" encoding="UTF-8"?>')
    final_list = ''
    for item in split_list:
        if item != "":
            final_list = final_list +'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'+ item.strip()+ '\n'
    final_func = send_object_to_s3(messagecount,final_list)
    return ['main_func completed',final_func]

def lambda_handler(event, context):
    "main lambda function"
    print(context.function_name)
    current_date=datetime.now().strftime("%d%m%Y%H%M%S%f")[:-3]
    pattern['class_name']= os.path.basename(__file__)
    pattern['level']= 'INFO'
    pattern['unique_id']= "fc-dtl-pst-ext_" + f'{current_date}'
    global s3_client
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
        log_error_msg(pattern,"fc-dtl-pst-ext-XML-500-0036", error_codes['fc-dtl-pst-ext-XML-500-0036'])
        raise e

    #connect with s3 using bucket name and filename we got from SQS event message
    try:
        obj = s3_client.get_object(Bucket=bucket, Key=key)
        data = obj['Body'].read().decode()
    except Exception as e:
        log_error_msg(pattern,"fc-dtl-pst-ext-XML-500-0003", error_codes['fc-dtl-pst-ext-XML-500-0003'])
        raise e
    #check the file having any data
    if not data:
        log_error_msg(pattern,"fc-dtl-pst-ext-XML-300-0004", error_codes['fc-dtl-pst-ext-XML-300-0004'])
        raise ValueError('File is empty')
   
    log_success_msg(pattern,"File has Valid data")
    lst_data=data.splitlines()
    result_main = mainfunction(lst_data)
    return ['fc-dtl-pst-ext-process_Processed Successfully', result_main]