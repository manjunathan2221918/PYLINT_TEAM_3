"""batch general types
"""
#pylint: disable=unused-import,too-few-public-methods,import-error,too-many-instance-attributes,too-few-public-methods,invalid-name
from dataclasses import dataclass, field
from typing import List, Optional
import configparser
from xsdata.models.datatype import XmlDateTime
from src.lambda_functions.fc_dtl_pst_ext_process_lambda.generated.general_types import (
    CrewTypes,
    Fleet,
    Parameters,
)


cons_path_gt = 'src/lambda_functions/fc_dtl_pst_ext_process_lambda/'
config = configparser.RawConfigParser()
config.read(cons_path_gt+'constants.properties')
constants = config['CONSTANTS']
link=constants['link']
__NAMESPACE__ = link


@dataclass
class BatchGeneralTypes:
    """
    This schema holds batch message general types.

    :ivar schema_version: Schema version
    """
    class Meta:
        """meta
        """
        name = "batchGeneralTypes"
        namespace = link

    schema_version: float = field(
        default=2.0,
        metadata={
            "name": "schemaVersion",
            "type": "Attribute",
        }
    )
@dataclass
class BatchAttribute:
    """
    :ivar crew_type: Crew type
    :ivar crew_ids: Crew IDs
    :ivar fleets: FLeets
    :ivar bases: Bases
    :ivar ranks: Ranks
    :ivar from_date_time: From date time
    :ivar to_date_time: To date time
    :ivar roster_period: Roster period
    :ivar parameters: Additional customer specific parameters for the
        BatchAttribute
    """
    crew_type: Optional[CrewTypes] = field(
        default=None,
        metadata={
            "name": "crewType",
            "type": "Element",
            "namespace": link,
        }
    )
    crew_ids: Optional["BatchAttribute.CrewIds"] = field(
        default=None,
        metadata={
            "name": "crewIds",
            "type": "Element",
            "namespace": link,
        }
    )
    fleets: Optional["BatchAttribute.Fleets"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    bases: Optional["BatchAttribute.Bases"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    ranks: Optional["BatchAttribute.Ranks"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    from_date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "fromDateTime",
            "type": "Element",
            "namespace": link,
        }
    )
    to_date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "toDateTime",
            "type": "Element",
            "namespace": link,
        }
    )
    roster_period: Optional[str] = field(
        default=None,
        metadata={
            "name": "rosterPeriod",
            "type": "Element",
            "namespace": link,
            "min_length": 1,
            "max_length": 20,
        }
    )
    parameters: Optional[Parameters] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )

    @dataclass
    class CrewIds:
        """
        :ivar crew_id: Crew ID
        """
        crew_id: List[str] = field(
            default_factory=list,
            metadata={
                "name": "crewId",
                "type": "Element",
                "namespace": link,
                "min_occurs": 1,
                "min_length": 1,
                "max_length": 25,
            }
        )

    @dataclass
    class Fleets:
        """
        :ivar fleet: Fleet
        """
        fleet: List[Fleet] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": link,
                "min_occurs": 1,
            }
        )

    @dataclass
    class Bases:
        """
        :ivar base: Base
        """
        base: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": link,
                "min_occurs": 1,
                "pattern": r'[A-Z]{3}',
            }
        )

    @dataclass
    class Ranks:
        """
        :ivar rank: Rank
        """
        rank: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": link,
                "min_occurs": 1,
                "min_length": 1,
                "max_length": 8,
            }
        )
