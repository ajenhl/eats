from eats.models import EATSUser


def get_user_preferences (request):
    """Returns a dictionary of user preferences derived from `request`.

    :rtype: dictionary

    """
    preferences = {'preferred_authority': None,
                   'preferred_language': None,
                   'preferred_script': None}
    try:
        eats_user = request.user.eats_user
        preferences['preferred_authority'] = eats_user.get_authority()
        preferences['preferred_language'] = eats_user.get_language()
        preferences['preferred_script'] = eats_user.get_script()
    except (AttributeError, EATSUser.DoesNotExist):
        pass
    return preferences

def user_is_editor (user):
    if not user.is_authenticated():
        return False
    try:
        eats_user = user.eats_user
    except EATSUser.DoesNotExist:
        return False
    if not eats_user.is_editor():
        return False
    return True

