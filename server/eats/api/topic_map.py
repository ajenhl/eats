from tmapi.models import Locator, Topic

from eats.constants import ADMIN_NAME_TYPE_IRI, LANGUAGE_CODE_TYPE_IRI, \
    LANGUAGE_TYPE_IRI, SCRIPT_CODE_TYPE_IRI, SCRIPT_TYPE_IRI


def topic_exists (topic_map, type_iri, name, topic_id):
    """Return True if `topic_map` contains a topic with the type
    specified by `type_iri` and whose administrative name is `name`.

    If `topic_id` is not None, return False if the matching topic has
    that id.

    :param topic_map: the EATS topic map
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

def create_topic_by_type (topic_map, type_iri, data=None):
    """Creates a topic of the specified type.

    :param topic_map: the EATS topic map in which the authority topic is created
    :type topic_map: `TopicMap`
    :param type_iri: IRI used as the Subject Identifier for the typing topic
    :type type_iri: string
    :param data: optional data to be saved with the topic to be created
    :type name: dictionary or None
    :rtype: `Topic`

    """
    topic = topic_map.create_topic()
    topic_type = topic_map.create_topic_by_subject_identifier(
        Locator(type_iri))
    topic.add_type(topic_type)
    if data is not None:
        # Different data to save depending on the type.
        name_type = topic_map.create_topic_by_subject_identifier(
            Locator(ADMIN_NAME_TYPE_IRI))
        topic.create_name(data['name'], type=name_type)
        if 'code' in data:
            if type_iri == LANGUAGE_TYPE_IRI:
                occurrence_type_iri = LANGUAGE_CODE_TYPE_IRI
            elif type_iri == SCRIPT_TYPE_IRI:
                occurrence_type_iri = SCRIPT_CODE_TYPE_IRI
            occurrence_type = topic_map.create_topic_by_subject_identifier(
                Locator(occurrence_type_iri))
            topic.create_occurrence(occurrence_type, data.get('code'))
    return topic

def get_admin_name (topic_map, topic):
    """Return the administrative name of `topic`.

    :param topic_map: The EATS topic map
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

    :param topic_map: the EATS topic map
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

    :param topic_map: the EATS topic map
    :type topic_map:  `TopicMap`
    :param type_iri: IRI used as the Subject Identifier for the typing topic
    :type type_iri: string
    :rtype: `QuerySet` of `Topic`s

    """
    topic_type = topic_map.create_topic_by_subject_identifier(
        Locator(type_iri))
    return topic_map.get_topics().filter(types=topic_type)

def get_topic_data (topic_map, topic, type_iri):
    """Returns the data associated with topic.

    :param topic_map: the EATS topic map
    :type topic_map: `TopicMap`
    :param topic: the topic whose data is to be retrieved
    :type topic: `Topic`
    :param type_iri: IRI used as the SubjectIdentifier for the typing topic
    :type type_iri: string

    """
    data = {}
    data['name'] = get_admin_name(topic_map, topic)
    if type_iri == LANGUAGE_TYPE_IRI:
        code_occurrence_type = topic_map.get_topic_by_subject_identifier(
            Locator(LANGUAGE_CODE_TYPE_IRI))
        code_occurrence = topic.get_occurrences(code_occurrence_type)[0]
        data['code'] = code_occurrence.get_value()
    elif type_iri == SCRIPT_TYPE_IRI:
        code_occurrence_type = topic_map.get_topic_by_subject_identifier(
            Locator(SCRIPT_CODE_TYPE_IRI))
        code_occurrence = topic.get_occurrences(code_occurrence_type)[0]
        data['code'] = code_occurrence.get_value()
    return data

def update_topic_by_type (topic_map, topic, type_iri, data):
    """Updates `topic` with the information in `data`.

    :param topic_map: the EATS topic map
    :type topic_map: `TopicMap`
    :param topic: the topic to be updated
    :type topic: `Topic`
    :param type_iri: IRI used as the SubjectIdentifier for the typing topic
    :type type_iri: string

    """
    get_admin_name(topic_map, topic).set_value(data.get('name'))
    if type_iri == LANGUAGE_TYPE_IRI:
        code_occurrence_type = topic_map.get_topic_by_subject_identifier(
            Locator(LANGUAGE_CODE_TYPE_IRI))
        code_occurrence = topic.get_occurrences(code_occurrence_type)[0]
        code_occurrence.set_value(data.get('code'))
