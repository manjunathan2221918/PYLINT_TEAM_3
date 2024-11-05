from dataclasses import dataclass, field
from typing import List
from xsdata.models.datatype import XmlDateTime
from src.lambda_functions.fc_dtl_pst_ext_process_lambda.generated.crew_general_types import CrewInfo
from src.lambda_functions.fc_dtl_pst_ext_process_lambda.generated.meta_data import ActionTypes
from src.lambda_functions.fc_dtl_pst_ext_process_lambda.generated.common import BaseDetails
import configparser

cons_path = 'src/lambda_functions/fc_dtl_pst_ext_process_lambda/'
config = configparser.RawConfigParser()
config.read(cons_path+'constants.properties')
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
