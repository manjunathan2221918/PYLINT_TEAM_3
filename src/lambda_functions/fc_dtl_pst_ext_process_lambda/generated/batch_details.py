"""_summary_
"""
#pylint: disable=line-too-long,invalid-name,too-few-public-methods,unused-import,import-error
from dataclasses import dataclass, field
from typing import Optional
import configparser
from xsdata.models.datatype import XmlDateTime
from src.lambda_functions.fc_dtl_pst_ext_process_lambda.generated.batch_general_types import BatchAttribute
from src.lambda_functions.fc_dtl_pst_ext_process_lambda.generated.meta_data import ActionTypes
from src.lambda_functions.fc_dtl_pst_ext_process_lambda.generated.common import BaseDetails

cons_path_pst = 'src/lambda_functions/fc_dtl_pst_ext_process_lambda/'
config = configparser.RawConfigParser()
config.read(cons_path_pst+'constants.properties')
constants = config['CONSTANTS']
link_pst=constants['link']
__NAMESPACE__ = link_pst

@dataclass
class BatchDetails(BaseDetails):
    """
    This schema defines the format of batch message information and also indicates
    the start / end of the batch message.

    :ivar batch_type: Batch type
    :ivar batch_attribute: Attributes of the batch message
    :ivar total_message_count: Total number of messages in the batch.
        Only specified in the 'END' message
    """
    class Meta:
        """meta
        """
        name = "batchDetails"
        namespace = link_pst

    batch_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "batchType",
            "type": "Element",
        }
    )
    batch_attribute: Optional[BatchAttribute] = field(
        default=None,
        metadata={
            "name": "batchAttribute",
            "type": "Element",
        }
    )
    total_message_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "totalMessageCount",
            "type": "Element",
        }
    )
