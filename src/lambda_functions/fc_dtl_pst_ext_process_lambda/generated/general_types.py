"""general_types
"""
#pylint: disable=unused-import,too-few-public-methods,invalid-name
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
import configparser
from xsdata.models.datatype import XmlDuration


cons_path = 'src/lambda_functions/fc_dtl_pst_ext_process_lambda/'
config = configparser.RawConfigParser()
config.read(cons_path+'constants.properties')
constants = config['CONSTANTS']
link=constants['link']
__NAMESPACE__ = link


class CrewTypes(Enum):
    """
    Crew types.
    """
    F = 'F'
    C = 'C'
@dataclass
class DaysOfWeek:
    """
    :ivar day_of_week: Day of week
    """
    day_of_week: List[str] = field(
        default_factory=list,
        metadata={
            "name": "dayOfWeek",
            "type": "Element",
            "namespace": link,
            "min_occurs": 1,
            "max_occurs": 7,
            "pattern": r'[1-7]',
        }
    )
@dataclass
class DurationOrPercentage:
    """
    Duration or percentage.
    """
    duration_value: Optional[XmlDuration] = field(
        default=None,
        metadata={
            "name": "durationValue",
            "type": "Element",
            "namespace": link,
        }
    )
    percentage_value: Optional[float] = field(
        default=None,
        metadata={
            "name": "percentageValue",
            "type": "Element",
            "namespace": link,
        }
    )
class FleetTypes(Enum):
    """
    Fleet types.
    """
    AGREEMENT = 'AGREEMENT'
    BASE = 'BASE'
    LICENSE = 'LICENSE'
class HaulTypes(Enum):
    """Haul types - Long haul / short haul/Medium Haul"""
    L = 'L'
    M = 'M'
    S = 'S'
@dataclass
class LengthType:
    """
    Specification of length with unit.

    :ivar value:
    :ivar unit: Unit of length
    """
    value: Optional[int] = field(
        default=None,
        metadata={
            "required": True,
        }
    )
    unit: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 2,
        }
    )
@dataclass
class Parameters:
    """
    :ivar parameter: Parameter name, value, and sub parameters
    """
    parameter: List["Parameters.Parameter"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": link,
            "min_occurs": 1,
        }
    )

    @dataclass
    class Parameter:
        """
        :ivar sub_parameter: Sub parameter name and value
        :ivar key: Parameter name
        :ivar value: Parameter value
        """
        sub_parameter: List["Parameters.Parameter.SubParameter"] = field(
            default_factory=list,
            metadata={
                "name": "subParameter",
                "type": "Element",
                "namespace": link,
            }
        )
        key: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
        value: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )

        @dataclass
        class SubParameter:
            """
            :ivar key: Sub parameter name
            :ivar value: Sub parameter value
            """
            key: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )
            value: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )
class PeriodTypes(Enum):
    """
    Period type.
    """
    D = 'D'
    W = 'W'
    M = 'M'
    Y = 'Y'
@dataclass
class SpecialDutyCodes:
    """
    Special duty codes.

    :ivar special_duty_code: Special duty code
    """
    special_duty_code: List["SpecialDutyCodes.SpecialDutyCode"] = field(
        default_factory=list,
        metadata={
            "name": "specialDutyCode",
            "type": "Element",
            "namespace": link,
            "min_occurs": 1,
        }
    )

    @dataclass
    class SpecialDutyCode:
        """
        :ivar value:
        :ivar type_value: Special duty type
        """
        value: str = field(
            default='',
            metadata={
                "required": True,
                "min_length": 1,
                "max_length": 10,
            }
        )
        type_value: Optional[str] = field(
            default=None,
            metadata={
                "name": "type",
                "type": "Attribute",
                "min_length": 1,
                "max_length": 15,
            }
        )
@dataclass
class VolumeType:
    """
    Specification of volume with unit.

    :ivar value:
    :ivar unit: Unit of volume
    """
    value: Optional[int] = field(
        default=None,
        metadata={
            "required": True,
        }
    )
    unit: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 2,
        }
    )
class WeightUnitTypes(Enum):
    """
    Unit of weight.
    """
    KG = 'KG'
    LBS = 'LBS'
@dataclass
class GeneralTypes:
    """
    This schema holds general types information.

    :ivar schema_version: Schema version
    """
    class Meta:
        """meta
        """
        name = "generalTypes"
        namespace = link

    schema_version: float = field(
        default=2.0,
        metadata={
            "name": "schemaVersion",
            "type": "Attribute",
        }
    )
@dataclass
class CrewApplicability:
    """
    :ivar crew_type: Crew type
    :ivar base: Base
    :ivar fleet: Fleet
    :ivar rank: Rank
    """
    crew_type: Optional[CrewTypes] = field(
        default=None,
        metadata={
            "name": "crewType",
            "type": "Element",
            "namespace": link,
        }
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
            "pattern": r'[A-Z]{3}',
        }
    )
    fleet: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
            "min_length": 1,
            "max_length": 20,
        }
    )
    rank: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
            "min_length": 1,
            "max_length": 8,
        }
    )
@dataclass
class CrewApplicabilityMulti:
    """
    Crew applicability.

    :ivar crew_type: Crew type
    :ivar fleets: Fleets
    :ivar ranks: Ranks
    :ivar bases: Bases
    """
    crew_type: Optional[CrewTypes] = field(
        default=None,
        metadata={
            "name": "crewType",
            "type": "Element",
            "namespace": link,
        }
    )
    fleets: Optional["CrewApplicabilityMulti.Fleets"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    ranks: Optional["CrewApplicabilityMulti.Ranks"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    bases: Optional["CrewApplicabilityMulti.Bases"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )

    @dataclass
    class Fleets:
        """
        :ivar fleet: Fleet
        """
        fleet: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": link,
                "min_occurs": 1,
                "min_length": 1,
                "max_length": 20,
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
class Fleet:
    """
    Fleet.
    """
    value: str = field(
        default='',
        metadata={
            "required": True,
            "min_length": 1,
            "max_length": 20,
        }
    )
    fleet_type: Optional[FleetTypes] = field(
        default=None,
        metadata={
            "name": "fleetType",
            "type": "Attribute",
        }
    )
@dataclass
class WeightType:
    """
    Specification of weight with unit.

    :ivar value:
    :ivar unit: Unit of weight
    """
    value: Optional[int] = field(
        default=None,
        metadata={
            "required": True,
        }
    )
    unit: Optional[WeightUnitTypes] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
