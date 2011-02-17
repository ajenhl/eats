from tmapi.models import Locator, Topic

from eats.constants import ADMIN_NAME_TYPE_IRI, AUTHORITY_TYPE_IRI, \
    ENTITY_TYPE_IRI
from eats.api.authority import get_authority_admin_name


def authority_exists (topic_map, name, authority_id):
    """Return True if `topic_map` contains an authority topic whose
    administrative name is `name`.

    If `authority_id` is not None, return False if the matching
    authority topic has that id.

    :param topic_map: the EATS Topic Map
    :type topic_map: `TopicMap`
    :param name: administrative name of the authority
    :type name: string
    :rtype: Boolean

    """
    if authority_id is not None:
        authority = get_authority(topic_map, authority_id)
        if name == get_authority_admin_name(topic_map, authority).get_value():
            return False
    authorities = get_authorities(topic_map)
    for authority in authorities:
        if name == get_authority_admin_name(topic_map, authority).get_value():
            return True
    return False

def create_authority (topic_map, name):
    """Creates a topic representing an authority in `topic_map`.

    :param topic_map: the EATS Topic Map in which the authority topic is created
    :type topic_map: `TopicMap`
    :param name: administrative name of the authority
    :type name: string
    :rtype: `Topic`

    """
    topic = create_topic_by_type(topic_map, AUTHORITY_TYPE_IRI)
    name_type = topic_map.create_topic_by_subject_identifier(
            Locator(ADMIN_NAME_TYPE_IRI))
    topic.create_name(name, type=name_type)
    return topic

def create_entity (topic_map):
    return create_topic_by_type(topic_map, ENTITY_TYPE_IRI)

def create_topic_by_type (topic_map, type_iri):
    topic = topic_map.create_topic()
    topic_type = topic_map.create_topic_by_subject_identifier(
        Locator(type_iri))
    topic.add_type(topic_type)
    return topic

def get_authorities (topic_map):
    """Returns a `QuerySet` of authority topics.

    :param topic_map: the EATS Topic Map
    :type topic_map: `TopicMap`
    :rtype: `QuerySet`

    """
    authority_topic_type = topic_map.create_topic_by_subject_identifier(
        Locator(AUTHORITY_TYPE_IRI))
    return topic_map.get_topics().filter(types=authority_topic_type)
    
def get_authority (topic_map, authority_id):
    """Returns the authority topic with `authority_id`, or None if
    there is no such topic.

    :param topic_map: the EATS Topic Map
    :type topic_map: `TopicMap`
    :rtype: `Topic`

    """
    authority = topic_map.get_construct_by_id(authority_id)
    if authority is not None:
        authority_topic_type = topic_map.get_topic_by_subject_identifier(
            Locator(AUTHORITY_TYPE_IRI))
        if not isinstance(authority, Topic) or \
                authority_topic_type not in authority.types.all():
            authority = None
    return authority
