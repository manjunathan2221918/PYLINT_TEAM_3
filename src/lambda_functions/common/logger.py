import logging
import os

logger= logging.getLogger()

#Setting common pattern for logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

pattern={
    'class_name':'',
    'level':'',
    'request_id':'',
    'unique_id': '',
    }

#Funtion for logging success messages
#Pattern-<Date/Time> <Request Id> <Level> <Classname> <uniqueId> -<message>
def log_success_msg(pattern, log_message):

    unique_id=pattern['unique_id']
    class_name=pattern['class_name']
    request_id=pattern['request_id']
    level=pattern['level']
    classname= os.path.splitext(class_name)[0]

    #Setting log level from env variable
    logger.setLevel(level.upper())

    
    if level.upper()=='INFO':

        logger.info(f"{request_id} {level.upper()} {classname} {unique_id} - {log_message}")

    elif level.upper()=='DEBUG':
        
        logger.debug(f"{request_id} {level.upper()} {classname} {unique_id} - {log_message}")

#Funtion for logging Error messages
def log_error_msg(pattern, error_code, error_message):

    unique_id=pattern['unique_id']
    class_name=pattern['class_name']
    request_id=pattern['request_id']
    classname= os.path.splitext(class_name)[0]

    error_type=get_error_type(error_code)

    level="ERROR"
    logger.setLevel(logging.ERROR)
    logger.error(f"{request_id} {level} {classname} {unique_id} {error_type} {error_code}- {error_message}")

     
   
def get_error_type(error_code):

    if '500' in error_code:

        error_type="Technical Exception"

    elif '300' in error_code:
        
        error_type="Validation Exception"

    elif '400' in error_code:

        error_type="Business Exception"

    return error_type