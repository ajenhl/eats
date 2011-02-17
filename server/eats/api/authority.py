from tmapi.models import Locator

from eats.constants import ADMIN_NAME_TYPE_IRI

def get_authority_admin_name (topic_map, authority):
    """Return the administrative name of `authority`.

    :param topic_map: The EATS Topic Map
    :type topic_map: `TopicMap`
    :param authority: The authority
    :type authority: `Topic`
    :rtype: `Name`

    """
    name_type = topic_map.create_topic_by_subject_identifier(
        Locator(ADMIN_NAME_TYPE_IRI))
    # There should only be a single such name, but this is not
    # enforced at the TMAPI level. There seems little need to raise an
    # error here if there is more than one.
    return authority.get_names(name_type)[0]
