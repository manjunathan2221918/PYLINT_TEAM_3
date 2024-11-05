from dataclasses import dataclass, field
from enum import Enum
import configparser

cons_path = 'src/lambda_functions/fc_dtl_pst_ext_process_lambda/'
config = configparser.RawConfigParser()
config.read(cons_path+'constants.properties')
constants = config['CONSTANTS']
link=constants['link']
__NAMESPACE__ = link


class ActionTypes(Enum):
    """
    Actions that can be performed on the message content.
    """
    ACKNOWLEDGE = 'ACKNOWLEDGE'
    CREATE = 'CREATE'
    DELETE = 'DELETE'
    END = 'END'
    GET = 'GET'
    START = 'START'
    UPDATE = 'UPDATE'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
@dataclass
class MetaData:
    """
    This schema holds message general information.

    :ivar schema_version: Schema version
    """
    class Meta:
        name = "metaData"
        namespace = link

    schema_version: float = field(
        default=2.0,
        metadata={
            "name": "schemaVersion",
            "type": "Attribute",
        }
    )