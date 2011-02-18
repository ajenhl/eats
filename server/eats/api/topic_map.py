from tmapi.models import Locator, Topic

from eats.constants import ADMIN_NAME_TYPE_IRI


def topic_exists (topic_map, type_iri, name, topic_id):
    """Return True if `topic_map` contains a topic with the type
    specified by `type_iri` and whose administrative name is `name`.

    If `topic_id` is not None, return False if the matching topic has
    that id.

    :param topic_map: the EATS Topic Map
    :type topic_map: `TopicMap`
    :param type_iri: IRI used as the Subject Identifier for the typing topic
    :type type_iri: string
    :param name: administrative name of the topic
    :type name: string
    :param topic_id: 
    :rtype: Boolean

    """
    if topic_id is not None:
        topic = get_topic_by_id(topic_map, topic_id, type_iri)
        if name == get_admin_name(topic_map, topic).get_value():
            return False
    topics = get_topics_by_type(topic_map, type_iri)
    for topic in topics:
        if name == get_admin_name(topic_map, topic).get_value():
            return True
    return False

def create_topic_by_type (topic_map, type_iri, admin_name=None):
    """Creates a topic of the specified type.

    :param topic_map: the EATS Topic Map in which the authority topic is created
    :type topic_map: `TopicMap`
    :param type_iri: IRI used as the Subject Identifier for the typing topic
    :type type_iri: string
    :param name: optional administrative name of the topic to be created
    :type name: string or None
    :rtype: `Topic`

    """
    topic = topic_map.create_topic()
    topic_type = topic_map.create_topic_by_subject_identifier(
        Locator(type_iri))
    topic.add_type(topic_type)
    if admin_name is not None:
        name_type = topic_map.create_topic_by_subject_identifier(
            Locator(ADMIN_NAME_TYPE_IRI))
        topic.create_name(admin_name, type=name_type)
    return topic

def get_admin_name (topic_map, topic):
    """Return the administrative name of `topic`.

    :param topic_map: The EATS Topic Map
    :type topic_map: `TopicMap`
    :param topic: The topic whose name is to be returned
    :type authority: `Topic`
    :rtype: `Name`

    """
    name_type = topic_map.create_topic_by_subject_identifier(
        Locator(ADMIN_NAME_TYPE_IRI))
    # There should only be a single such name, but this is not
    # enforced at the TMAPI level. There seems little need to raise an
    # error here if there is more than one.
    return topic.get_names(name_type)[0]

def get_topic_by_id (topic_map, topic_id, type_iri):
    """Returns the topic with `topic_id`, or None if there is no such
    topic that is of the type specified by `type_iri`.

    :param topic_map: the EATS Topic Map
    :type topic_map: `TopicMap`
    :param topic_id: identifier of the topic
    :type topic_id: integer
    :param type_iri: IRI used as the Subject Identifier for the typing topic
    :type type_iri: string
    :rtype: `Topic`

    """
    topic = topic_map.get_construct_by_id(topic_id)
    if topic is not None:
        topic_type = topic_map.get_topic_by_subject_identifier(
            Locator(type_iri))
        if not isinstance(topic, Topic) or topic_type not in topic.types.all():
            topic = None
    return topic

def get_topics_by_type (topic_map, type_iri):
    """Returns a `QuerySet` of topics of the type specified by
    `type_iri`.

    :param topic_map: the EATS Topic Map
    :type topic_map:  `TopicMap`
    :param type_iri: IRI used as the Subject Identifier for the typing topic
    :type type_iri: string
    :rtype: `QuerySet` of `Topic`s

    """
    topic_type = topic_map.create_topic_by_subject_identifier(
        Locator(type_iri))
    return topic_map.get_topics().filter(types=topic_type)
