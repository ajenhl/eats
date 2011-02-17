"""Module containing API for handling entities."""

from eats.constants import ENTITY_ROLE_TYPE, EXISTENCE_ASSOCIATION_TYPE

def get_existences (entity, authority=None):
    """Returns the existences for `entity`.

    If `authority` is not None, returns only those existences that are
    asserted by that authority.

    :param entity: the entity whose existences are to be returned
    :type entity: `Topic`
    :param authority: the optional authority
    :type authority: `Topic`
    :rtype: list of `Association`s

    """
    roles = entity.get_roles_played(ENTITY_ROLE_TYPE,
                                    EXISTENCE_ASSOCIATION_TYPE)
    associations = [role.get_parent() for role in roles]
    if authority is not None:
        associations = [association for association in associations if
                        authority in association.get_scope()]
    return associations
