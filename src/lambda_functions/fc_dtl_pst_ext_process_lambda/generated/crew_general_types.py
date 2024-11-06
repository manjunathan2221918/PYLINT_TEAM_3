"""crew_general
"""
#pylint: disable=line-too-long,,unused-import,too-few-public-methods,invalid-name,too-many-lines,too-many-instance-attributes,import-error
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
import configparser
from xsdata.models.datatype import XmlDate, XmlDateTime, XmlDuration, XmlTime
from src.lambda_functions.fc_dtl_pst_ext_process_lambda.generated.general_types import (
    CrewTypes,
    DaysOfWeek,
    Parameters,
    PeriodTypes,
)

cons_path = 'src/lambda_functions/fc_dtl_pst_ext_process_lambda/'
config = configparser.RawConfigParser()
config.read(cons_path+'constants.properties')
constants = config['CONSTANTS']
link=constants['link']
__NAMESPACE__ = link


class CrewActionTypes(Enum):
    """
    Actions that can be performed on the message content.
    """
    CREATE = 'CREATE'
    DELETE = 'DELETE'
    UPDATE = 'UPDATE'
class GenderTypes(Enum):
    """
    Gender types.
    """
    M = 'M'
    F = 'F'
    TG = 'TG'
    ND = 'ND'
class PostingTypes(Enum):
    """
    Posting types.
    """
    PERMANENT = 'PERMANENT'
    TEMPORARY = 'TEMPORARY'
class QualificationRenewalTypes(Enum):
    """
    Qualification renewal types.
    """
    INITIAL = 'INITIAL'
    RECURRENT = 'RECURRENT'
    REQUALIFICATION = 'REQUALIFICATION'
class QualificationStatuses(Enum):
    """
    Qualification statuses.
    """
    ACTUAL = 'ACTUAL'
    PLANNED = 'PLANNED'
@dataclass
class CrewGeneralTypes:
    """
    This schema holds crew general types.

    :ivar schema_version: Schema version
    """
    class Meta:
        """meta
        """
        name = "crewGeneralTypes"
        namespace = link

    schema_version: float = field(
        default=2.0,
        metadata={
            "name": "schemaVersion",
            "type": "Attribute",
        }
    )
@dataclass
class CrewAddresses:
    """
    Crew addresses.

    :ivar address: Address
    :ivar snapshot_ind: Snapshot indicator
    """
    address: List["CrewAddresses.Address"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    snapshot_ind: Optional[bool] = field(
        default=None,
        metadata={
            "name": "snapshotInd",
            "type": "Attribute",
        }
    )

    @dataclass
    class Address:
        """
        :ivar address_type: Address type
        :ivar address_line1: Address line one
        :ivar address_line2: Address line two
        :ivar address_line3: Address line three
        :ivar city: city
        :ivar state: State
        :ivar country: Country
        :ivar postal_code: Pin or zip code
        :ivar primary_ind: Indicates whether the address is primary or
            not
        :ivar from_date: From date
        :ivar to_date: To date
        :ivar action_type: Action type
        """
@dataclass
class CrewAppointments:
    """
    Crew appointments.

    :ivar appointment: Appointment
    """
    appointment: List["CrewAppointments.Appointment"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": link,
            "min_occurs": 1,
        }
    )

    @dataclass
    class Appointment:
        """
        :ivar appointment_code: Appointment code
        :ivar from_date: From date
        :ivar to_date: To date
        :ivar from_date_time: From date
        :ivar to_date_time: To date
        :ivar action_type: Action type
        """
@dataclass
class CrewContacts:
    """
    Crew Contacts.

    :ivar contact: Contact
    :ivar snapshot_ind: Snapshot indicator
    """
    contact: List["CrewContacts.Contact"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    snapshot_ind: Optional[bool] = field(
        default=None,
        metadata={
            "name": "snapshotInd",
            "type": "Attribute",
        }
    )

    @dataclass
    class Contact:
        """
        :ivar contact_type: Contact type
        :ivar contact_value: Contact value
        :ivar primary_ind: Indicates whether the contact is primary or
            not
        :ivar from_date: From date
        :ivar to_date: To date
        :ivar action_type: Action type
        """
@dataclass
class CrewContracts:
    """
    Crew contracts.

    :ivar contract: Contract
    """
    contract: List["CrewContracts.Contract"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": link,
            "min_occurs": 1,
        }
    )

    @dataclass
    class Contract:
        """
        :ivar contract_code: Contract code
        :ivar contract_factor: Contract factor (Not part of product)
        :ivar contract_type: Contract type (Not part of product)
        :ivar contract_reference_number: Contract reference number
        :ivar from_date: From date
        :ivar to_date: To date
        :ivar from_date_time: From date
        :ivar to_date_time: To date
        :ivar action_type: Action type
        """
@dataclass
class CrewEmergencyContacts:
    """
    Crew emergency contacts.

    :ivar emergency_contact: Emergency contact
    :ivar snapshot_ind: Snapshot indicator
    """
    emergency_contact: List["CrewEmergencyContacts.EmergencyContact"] = field(
        default_factory=list,
        metadata={
            "name": "emergencyContact",
            "type": "Element",
            "namespace": link,
        }
    )
    snapshot_ind: Optional[bool] = field(
        default=None,
        metadata={
            "name": "snapshotInd",
            "type": "Attribute",
        }
    )

    @dataclass
    class EmergencyContact:
        """
        :ivar relation: Relationship with the emergency contact
        :ivar name: Name of the emergency contact
        :ivar contact_number: Contact number of the emergency contact
        :ivar primary_ind: Indicates whether the address is primary or
            not
        :ivar comments: Comments
        :ivar from_date: From date
        :ivar to_date: To date
        :ivar action_type: Action type
        """
@dataclass
class CrewEmployments:
    """
    Crew employments.

    :ivar employment: Employment
    :ivar snapshot_ind: Snapshot indicator
    """
    employment: List["CrewEmployments.Employment"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    snapshot_ind: Optional[bool] = field(
        default=None,
        metadata={
            "name": "snapshotInd",
            "type": "Attribute",
        }
    )

    @dataclass
    class Employment:
        """
        :ivar crew_id: Crew ID
        :ivar airline_code: Airline / organization code that defines the
            employment of the crew
        :ivar from_date: From date
        :ivar to_date: To date
        :ivar from_date_time: From date
        :ivar to_date_time: To date
        :ivar action_type: Action type
        """
@dataclass
class CrewGroups:
    """
    Crew groups.

    :ivar group: Group
    """
    group: List["CrewGroups.Group"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": link,
            "min_occurs": 1,
        }
    )

    @dataclass
    class Group:
        """
        :ivar group_code: Crew group code
        :ivar group_type: Crew group type
        :ivar from_date: From date
        :ivar to_date: To date
        :ivar from_date_time: From date
        :ivar to_date_time: To date
        :ivar action_type: Action type
        """
@dataclass
class CrewLicenses:
    """
    Crew license documents.

    :ivar license: License document
    :ivar snapshot_ind: Snapshot indicator
    """
    license: List["CrewLicenses.License"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    snapshot_ind: Optional[bool] = field(
        default=None,
        metadata={
            "name": "snapshotInd",
            "type": "Attribute",
        }
    )

    @dataclass
    class License:
        """
        :ivar license_code: License code
        :ivar license_number: License reference number
        :ivar issuing_authority: Authority who issued the license
        :ivar country_of_issue: Country from where the license was
            issued
        :ivar issue_date: Date on which the license was issued
        :ivar effective_date: Effective date
        :ivar expiry_date: Expiry date
        :ivar comments: Comments
        :ivar action_type: Action type
        """
@dataclass
class CrewMedicalDocuments:
    """
    Crew medical documents.

    :ivar medical_document: Medical document
    """
    medical_document: List["CrewMedicalDocuments.MedicalDocument"] = field(
        default_factory=list,
        metadata={
            "name": "medicalDocument",
            "type": "Element",
            "namespace": link,
            "min_occurs": 1,
        }
    )

    @dataclass
    class MedicalDocument:
        """
        :ivar medical_qualification: Medical qualification
        :ivar document_reference_number: Reference number of the medical
            document submitted
        :ivar country_of_issue: Country from where the medical document
            was issued
        :ivar issue_date: Issue date
        :ivar expiry_date: Expiry date
        :ivar comments: Comments
        :ivar action_type: Action type
        """
@dataclass
class CrewNationalities:
    """
    Crew nationalities.

    :ivar nationality: Nationality
    :ivar snapshot_ind: Snapshot indicator
    """
    nationality: List["CrewNationalities.Nationality"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    snapshot_ind: Optional[bool] = field(
        default=None,
        metadata={
            "name": "snapshotInd",
            "type": "Attribute",
        }
    )

    @dataclass
    class Nationality:
        """
        :ivar country: Country from where the passport was issued
        :ivar from_date: From date
        :ivar to_date: To date
        :ivar action_type: Action type
        """
@dataclass
class CrewOtherDocuments:
    """
    Crew other documents.

    :ivar other_document: Other document
    """
    other_document: List["CrewOtherDocuments.OtherDocument"] = field(
        default_factory=list,
        metadata={
            "name": "otherDocument",
            "type": "Element",
            "namespace": link,
            "min_occurs": 1,
        }
    )

    @dataclass
    class OtherDocument:
        """
        :ivar document_reference_number: Reference number of the
            submitted document
        :ivar document_code: Document code
        :ivar country_of_issue: Country from where the document was
            issued
        :ivar issue_date: Issue date
        :ivar effective_date: Effective date
        :ivar expiry_date: Expiry date
        :ivar comments: Comments
        :ivar action_type: Action type
        """
@dataclass
class CrewPassports:
    """
    Crew Passports.

    :ivar passport: Passport
    :ivar snapshot_ind: Snapshot indicator
    """
    passport: List["CrewPassports.Passport"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    snapshot_ind: Optional[bool] = field(
        default=None,
        metadata={
            "name": "snapshotInd",
            "type": "Attribute",
        }
    )

    @dataclass
    class Passport:
        """
        :ivar passport_number: Passport number
        :ivar place_of_issue: Place from where the passort was issued
        :ivar country_of_issue: Country from where the passport was
            issued
        :ivar issue_date: Date on which the passport was issued
        :ivar cancellation_date: Date on which the passport was
            cancelled
        :ivar expiry_date: Expiry date
        :ivar primary_ind: Indicates whether the passport is primary or
            not
        :ivar comments: Comments
        :ivar action_type: Action type
        """
@dataclass
class CrewPersonalInfo:
    """
    Personal information of the crew.

    :ivar search_name: Search name
    :ivar first_name: First name
    :ivar middle_name: Middle name
    :ivar last_name: Last name
    :ivar called_name: Name by which crew wishes to be called
    :ivar gender: Gender
    :ivar crew_type: Crew type
    :ivar date_of_birth: Date of birth
    :ivar place_of_birth: Place of birth
    :ivar country_of_birth: Country of birth
    :ivar joining_date: Date of joining
    :ivar joining_date_time: DateTime of joining
    :ivar leaving_date: Date of leaving
    :ivar leaving_date_time: DateTime of leaving
    :ivar last_promotion_date: Date on which the crew was last promoted
    :ivar last_promotion_date_time: DateTime on which the crew was last
        promoted
    :ivar flying_since_date: Date from which the crew started flying
    :ivar flying_since_date_time: DateTime from which the crew started
        flying
    :ivar social_security_number: Social security number
    :ivar religion: Religion
    :ivar race: Race
    :ivar marital_status: Marital status
    """
@dataclass
class CrewPostings:
    """
    Crew postings.

    :ivar posting: Posting
    """
    posting: List["CrewPostings.Posting"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": link,
            "min_occurs": 1,
        }
    )

    @dataclass
    class Posting:
        """
        :ivar base: Base
        :ivar fleet: Fleet
        :ivar rank: Rank
        :ivar posting_type: Posting type
        :ivar from_date: From date
        :ivar to_date: To date
        :ivar from_date_time: From date
        :ivar to_date_time: To date
        :ivar action_type: Action type
        """
        base: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": link,
                "required": True,
                "pattern": r'[A-Z]{3}',
            }
        )
        fleet: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": link,
                "required": True,
                "min_length": 1,
                "max_length": 20,
            }
        )
        rank: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": link,
                "required": True,
                "min_length": 1,
                "max_length": 8,
            }
        )
        posting_type: Optional[PostingTypes] = field(
            default=None,
            metadata={
                "name": "postingType",
                "type": "Element",
                "namespace": link,
            }
        )
        from_date: Optional[XmlDate] = field(
            default=None,
            metadata={
                "name": "fromDate",
                "type": "Element",
                "namespace": link,
            }
        )
        to_date: Optional[XmlDate] = field(
            default=None,
            metadata={
                "name": "toDate",
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
        action_type: Optional[CrewActionTypes] = field(
            default=None,
            metadata={
                "name": "actionType",
                "type": "Attribute",
            }
        )
@dataclass
class CrewPreferences:
    """
    Crew preferences.

    :ivar preference: Preference
    """
    preference: List["CrewPreferences.Preference"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": link,
            "min_occurs": 1,
        }
    )

    @dataclass
    class Preference:
        """
        :ivar preference_type: Preference type
        :ivar airport: Airport
        :ivar airport_group_code: Airport group code
        :ivar airport_group_type: Airport group type
        :ivar limit: Limit specified for the restriction or preference
            type
        :ivar from_time: From time
        :ivar to_time: To time
        :ivar no_fly_crew_id: No fly with crew ID
        :ivar period_type: Period type
        :ivar period_count: Period count
        :ivar meal_preference: Meal preference
        :ivar days_of_week: Days of week applicable for the preference /
            restriction
        :ivar value: Preference value used for general purpose
        :ivar buddies: Buddy preference
        :ivar activity_code: Activity code
        :ivar comments: Comments
        :ivar from_date: From date
        :ivar to_date: To date
        :ivar action_type: Action type
        """
        @dataclass
        class Buddies:
            """
            :ivar buddy_crew: Buddy crew Id
            """
            buddy_crew: Optional[str] = field(
                default=None,
                metadata={
                    "name": "buddyCrew",
                    "type": "Element",
                    "namespace": link,
                    "required": True,
                    "min_length": 1,
                    "max_length": 25,
                }
            )
@dataclass
class CrewQualifications:
    """
    Crew qualifications.

    :ivar qualification: Qualification
    :ivar snapshot_ind: Snapshot indicator
    """
    qualification: List["CrewQualifications.Qualification"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    snapshot_ind: Optional[bool] = field(
        default=None,
        metadata={
            "name": "snapshotInd",
            "type": "Attribute",
        }
    )

    @dataclass
    class Qualification:
        """
        :ivar qualification_code: Qualification code
        :ivar qualification_status: Qualification status
        :ivar renewal_type: Qualification renewal type
        :ivar document_reference: Reference number of the document
            submitted for license, medical qualification etc.
        :ivar issue_location: Issue location
        :ivar check_date: Date on which the qualification check was done
        :ivar initial_from_date: Initial start date of the qualification
        :ivar active_ind: Indicates whether the record is active or not
        :ivar comments: Comments
        :ivar from_date: From date
        :ivar to_date: To date
        :ivar action_type: Action type
        """
@dataclass
class CrewQualifiedRanks:
    """
    Crew qualified ranks.

    :ivar qualified_rank: Qualified rank
    """
    qualified_rank: List["CrewQualifiedRanks.QualifiedRank"] = field(
        default_factory=list,
        metadata={
            "name": "qualifiedRank",
            "type": "Element",
            "namespace": link,
            "min_occurs": 1,
        }
    )

    @dataclass
    class QualifiedRank:
        """
        :ivar rank: Qualified Rank
        :ivar from_date: From date
        :ivar to_date: To date
        :ivar from_date_time: From date
        :ivar to_date_time: To date
        :ivar action_type: Action type
        """
@dataclass
class CrewRestrictions:
    """
    Crew restrictions.

    :ivar restriction: Restriction
    """
    restriction: List["CrewRestrictions.Restriction"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": link,
            "min_occurs": 1,
        }
    )

    @dataclass
    class Restriction:
        """
        :ivar restriction_type: Restriction type
        :ivar airport: Airport
        :ivar airport_group_code: Airport group code
        :ivar airport_group_type: Airport group type
        :ivar limit: Limit specified for the restriction or preference
            type
        :ivar from_time: From time
        :ivar to_time: To time
        :ivar no_fly_crew_id: No fly with crew ID
        :ivar period_type: Period type
        :ivar period_count: Period count
        :ivar meal_preference: Meal preference
        :ivar days_of_week: Days of week applicable for the preference /
            restriction
        :ivar country: Country
        :ivar sector_mask: Sector mask
        :ivar comments: Comments
        :ivar from_date: From date
        :ivar to_date: To date
        :ivar action_type: Action type
        """
@dataclass
class CrewVisas:
    """
    Crew visas.

    :ivar visa: Visa
    :ivar snapshot_ind: Snapshot indicator
    """
    visa: List["CrewVisas.Visa"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    snapshot_ind: Optional[bool] = field(
        default=None,
        metadata={
            "name": "snapshotInd",
            "type": "Attribute",
        }
    )

    @dataclass
    class Visa:
        """
        :ivar visa_number: Visa number
        :ivar visa_type: Type of visa issued
        :ivar country_of_issue: Country for which the visa was issued
        :ivar place_of_issue: Country from where the visa was issued
        :ivar duration_of_stay: Duration for which the crew will be able
            to stay on a single visit
        :ivar passport_number: Passport to which the visa is attached
        :ivar issue_date: Date on which the visa was issued
        :ivar effective_date: Effective date
        :ivar expiry_date: Expiry date
        :ivar comments: Comments
        :ivar action_type: Action type
        """
@dataclass
class Seniorities:
    """
    Seniorities.

    :ivar seniority: Seniority
    """
    seniority: List["Seniorities.Seniority"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": link,
            "min_occurs": 1,
        }
    )

    @dataclass
    class Seniority:
        """
        :ivar seniority_number: Seniority number
        :ivar seniority_type: Seniority type
        :ivar group_code: Seniority group code
        :ivar from_date: From date
        :ivar to_date: To date
        :ivar action_type: Action type
        """
@dataclass
class CrewInfo:
    """
    :ivar personal_info: Personal information
    :ivar employments: Employments
    :ivar contracts: Contracts
    :ivar postings: Postings
    :ivar qualifications: Qualifications
    :ivar qualified_ranks: Qualified ranks
    :ivar groups: Groups
    :ivar appointments: Appointments
    :ivar preferences: Preferences
    :ivar restrictions: Restrictions
    :ivar seniorities: Seniorities
    :ivar medical_documents: Medical documents
    :ivar licenses: Licenses
    :ivar visas: Visas
    :ivar passports: Passports
    :ivar other_documents: Other documents
    :ivar nationalities: Nationalities
    :ivar addresses: Addresses
    :ivar contacts: Contacts
    :ivar emergency_contacts: Emergency contacts
    :ivar cloaked_ind: Indicates whether the crew is cloaked
    :ivar parameters: Parameter types and values
    :ivar crew_id: Crew ID
    """
    personal_info: Optional[CrewPersonalInfo] = field(
        default=None,
        metadata={
            "name": "personalInfo",
            "type": "Element",
            "namespace": link,
        }
    )
    employments: Optional[CrewEmployments] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    contracts: Optional[CrewContracts] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    postings: Optional[CrewPostings] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    qualifications: Optional[CrewQualifications] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    qualified_ranks: Optional[CrewQualifiedRanks] = field(
        default=None,
        metadata={
            "name": "qualifiedRanks",
            "type": "Element",
            "namespace": link,
        }
    )
    groups: Optional[CrewGroups] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    appointments: Optional[CrewAppointments] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    preferences: Optional[CrewPreferences] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    restrictions: Optional[CrewRestrictions] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    seniorities: Optional[Seniorities] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    medical_documents: Optional[CrewMedicalDocuments] = field(
        default=None,
        metadata={
            "name": "medicalDocuments",
            "type": "Element",
            "namespace": link,
        }
    )
    licenses: Optional[CrewLicenses] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    visas: Optional[CrewVisas] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    passports: Optional[CrewPassports] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    other_documents: Optional[CrewOtherDocuments] = field(
        default=None,
        metadata={
            "name": "otherDocuments",
            "type": "Element",
            "namespace": link,
        }
    )
    nationalities: Optional[CrewNationalities] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    addresses: Optional[CrewAddresses] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    contacts: Optional[CrewContacts] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    emergency_contacts: Optional[CrewEmergencyContacts] = field(
        default=None,
        metadata={
            "name": "emergencyContacts",
            "type": "Element",
            "namespace": link,
        }
    )
    cloaked_ind: Optional[bool] = field(
        default=None,
        metadata={
            "name": "cloakedInd",
            "type": "Element",
            "namespace": link,
        }
    )
    parameters: Optional[Parameters] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": link,
        }
    )
    crew_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "crewId",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 25,
        }
    )
