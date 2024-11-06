"""common
"""
#pylint: disable=unused-import,too-few-public-methods,import-error,too-many-instance-attributes,import-error
from dataclasses import dataclass, field
from typing import Optional
import configparser
from xsdata.models.datatype import XmlDateTime
from src.lambda_functions.fc_dtl_pst_ext_process_lambda.generated.meta_data import ActionTypes

CONS_PATH = 'src/lambda_functions/fc_dtl_pst_ext_process_lambda/'
config = configparser.RawConfigParser()
config.read(CONS_PATH+'constants.properties')
constants = config['CONSTANTS']
link = constants['link']
__NAMESPACE__ = link

@dataclass
class BaseDetails:
    """
    Base class for common message details.
    
    :ivar action_type: Message action type
    :ivar message_reference: Message reference
    :ivar batch_reference: Message batch/group reference
    :ivar sequence_number: Message sequence number in the batch/group
    :ivar total_message_count: Total number of messages in the RTU group
    :ivar batch_end_ind: Indicates whether the message is the last one
        in the batch/group
    :ivar timestamp: Message creation timestamp
    :ivar originator: Message originator
    :ivar company: Company
    :ivar tenant: Tenant
    :ivar destination: Message destination
    :ivar proprietary_notice: Proprietary notice
    :ivar schema_version: Schema version
    """
    class Meta:
        """meta
        """
        namespace = link

    action_type: Optional[ActionTypes] = field(
        default=None,
        metadata={
            "name": "actionType",
            "type": "Attribute",
        }
    )
    message_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "messageReference",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 50,
        }
    )
    batch_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "batchReference",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 50,
        }
    )
    sequence_number: Optional[int] = field(
        default=None,
        metadata={
            "name": "sequenceNumber",
            "type": "Attribute",
        }
    )
    total_message_count_attribute: Optional[int] = field(
        default=None,
        metadata={
            "name": "totalMessageCount",
            "type": "Attribute",
        }
    )
    batch_end_ind: Optional[bool] = field(
        default=None,
        metadata={
            "name": "batchEndInd",
            "type": "Attribute",
        }
    )
    timestamp: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    originator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    company: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_length": 1,
            "max_length": 15,
        }
    )
    tenant: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_length": 1,
            "max_length": 15,
        }
    )
    destination: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    proprietary_notice: str = field(
        init=False,
        default='(c) 2018 IBS Software Private Limited',
        metadata={
            "name": "proprietaryNotice",
            "type": "Attribute",
        }
    )
    schema_version: float = field(
        init=False,
        default=2.0,
        metadata={
            "name": "schemaVersion",
            "type": "Attribute",
            "required": True,
        }
    )
