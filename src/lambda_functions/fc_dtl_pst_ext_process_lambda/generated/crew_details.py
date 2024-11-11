"""crew_details
"""
#pylint: disable=unused-import,too-few-public-methods,import-error
from dataclasses import dataclass, field
from typing import List
import configparser
from xsdata.models.datatype import XmlDateTime
from src.lambda_functions.fc_dtl_pst_ext_process_lambda.generated.crew_general_types import CrewInfo
from src.lambda_functions.fc_dtl_pst_ext_process_lambda.generated.meta_data import ActionTypes
from src.lambda_functions.fc_dtl_pst_ext_process_lambda.generated.common import BaseDetails


CONS_PATH_CD = 'src/lambda_functions/fc_dtl_pst_ext_process_lambda/'
config = configparser.RawConfigParser()
config.read(CONS_PATH_CD+'constants.properties')
constants = config['CONSTANTS']
link=constants['link']

__NAMESPACE__ = link

@dataclass
class CrewDetails(BaseDetails):
    """
    This schema holds the crew details information.

    :ivar crew_info: Crew information
    """
    class Meta:
        """metadata
        """
        name = "crewDetails"
        namespace = link

    crew_info: List[CrewInfo] = field(
        default_factory=list,
        metadata={
            "name": "crewInfo",
            "type": "Element",
            "min_occurs": 1,
        }
    )
