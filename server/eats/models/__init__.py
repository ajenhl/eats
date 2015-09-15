"""Model definitions for the EATS application.

These models are all proxy models for the real models provided by the
TMAPI application.

"""

from .authority import Authority
from .calendar import Calendar
from .date import Date
from .date_part import DatePart
from .date_period import DatePeriod
from .date_type import DateType
from .eats_topic_map import EATSTopicMap
from .eats_user import EATSUser
from .eatsml_import import EATSMLImport
from .entity import Entity
from .entity_relationship_cache import EntityRelationshipCache
from .entity_relationship_property_assertion import EntityRelationshipPropertyAssertion
from .entity_relationship_type import EntityRelationshipType
from .entity_type import EntityType
from .entity_type_property_assertion import EntityTypePropertyAssertion
from .existence_property_assertion import ExistencePropertyAssertion
from .language import Language
from .name import Name
from .name_cache import NameCache
from .name_index import NameIndex
from .name_part import NamePart
from .name_part_type import NamePartType
from .name_property_assertion import NamePropertyAssertion
from .note_property_assertion import NotePropertyAssertion
from .name_type import NameType
from .script import Script
