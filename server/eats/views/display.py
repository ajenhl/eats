from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.shortcuts import redirect, render

import ddh_utils.utils
from lxml import etree

from eats.constants import UNNAMED_ENTITY_NAME
from eats.decorators import add_topic_map
from eats.exceptions import EATSMergedIdentifierException
from eats.forms.display import EntitySearchForm
from eats.lib.eatsml_exporter import EATSMLExporter
from eats.lib.user import get_eats_user, get_user_preferences, user_is_editor
from eats.lib.views import get_topic_or_404
from eats.models import Authority, Entity, EntityRelationshipPropertyAssertion, EntityRelationshipType, EntityType, EntityTypePropertyAssertion


def home (request):
    context_data = {}
    context_data['user_is_editor'] = user_is_editor(request.user)
    return render(request, 'eats/display/home.html', context_data)

@add_topic_map
def entity_view (request, topic_map, entity_id):
    try:
        entity = get_topic_or_404(Entity, entity_id)
    except EATSMergedIdentifierException as e:
        return redirect('eats-entity-view', entity_id=e.new_id, permanent=True)
    user_preferences = get_user_preferences(request)
    preferred_authority = user_preferences['preferred_authority']
    preferred_language = user_preferences['preferred_language']
    preferred_script = user_preferences['preferred_script']
    try:
        preferred_name_form = entity.get_preferred_name(
            authority=preferred_authority, language=preferred_language,
            script=preferred_script).name.assembled_form
    except AttributeError:
        preferred_name_form = UNNAMED_ENTITY_NAME
    existence_pas = entity.get_existences()
    has_existence_dates = entity.get_existence_dates().count()
    entity_type_pas = entity.get_entity_types()
    name_pas = entity.get_eats_names()
    relationship_pas = entity.get_entity_relationships()
    note_pas = entity.get_notes(user=get_eats_user(request))
    subject_identifier_pas = entity.get_eats_subject_identifiers()
    context_data = {'eats_user': get_eats_user(request),
                    'entity': entity,
                    'has_existence_dates': has_existence_dates,
                    'preferred_authority': preferred_authority,
                    'preferred_language': preferred_language,
                    'preferred_name_form': preferred_name_form,
                    'preferred_script': preferred_script,
                    'existence_pas': existence_pas,
                    'entity_type_pas': entity_type_pas, 'name_pas': name_pas,
                    'note_pas': note_pas,
                    'property_assertion_full_certainty':
                        topic_map.property_assertion_full_certainty,
                    'relationship_pas': relationship_pas,
                    'subject_identifier_pas': subject_identifier_pas,
                    'site': Site.objects.get_current(),
                    'user_is_editor': user_is_editor(request.user)}
    return render(request, 'eats/display/entity.html', context_data)

@add_topic_map
def entity_eatsml_view (request, topic_map, entity_id):
    try:
        entity = get_topic_or_404(Entity, entity_id)
    except EATSMergedIdentifierException as e:
        return redirect('eats-entity-eatsml-view', entity_id=e.new_id,
                        permanent=True)
    eats_user = get_eats_user(request)
    tree = EATSMLExporter(topic_map).export_entities([entity], eats_user)
    xml = etree.tostring(tree, encoding='utf-8', pretty_print=True)
    return HttpResponse(xml, content_type='text/xml')

@add_topic_map
def search (request, topic_map):
    form_data = request.GET or None
    entity_types = EntityType.objects.filter_by_used_by_authority()
    form = EntitySearchForm(topic_map, data=form_data,
                            entity_types=entity_types)
    entities = []
    user_preferences = {}
    if form.is_valid():
        name = form.cleaned_data['name']
        entity_type_ids = form.cleaned_data['entity_types']
        entity_types = [EntityType.objects.get_by_identifier(entity_type_id) for
                        entity_type_id in entity_type_ids]
        results = topic_map.lookup_entities(name, entity_types)
        page_number = request.GET.get('page')
        try:
            results_per_page = settings.EATS_RESULTS_PER_PAGE
        except AttributeError:
            results_per_page = 10
        paginator, entities = ddh_utils.utils.create_pagination(
            results, results_per_page, page_number)
        user_preferences = get_user_preferences(request)
    context_data = {
        'eats_user': get_eats_user(request), 'entities': entities,
        'property_assertion_full_certainty':
        topic_map.property_assertion_full_certainty,
        'querydict': request.GET, 'search_form': form,
        'user_is_editor': user_is_editor(request.user)}
    context_data.update(user_preferences)
    return render(request, 'eats/display/search.html', context_data)

@add_topic_map
def search_eatsml (request, topic_map):
    name = request.GET.get('name', '')
    entities = topic_map.lookup_entities(name)
    eats_user = get_eats_user(request)
    tree = EATSMLExporter(topic_map).export_entities(entities, user=eats_user)
    xml = etree.tostring(tree, encoding='utf-8', pretty_print=True)
    return HttpResponse(xml, content_type='text/xml')

@add_topic_map
def statistics (request, topic_map):
    number_entities = Entity.objects.count()
    entity_type_stats = {}
    entity_relationship_stats = {}
    authorities = list(Authority.objects.all())
    for entity_type in EntityType.objects.all():
        et_data = entity_type_stats.setdefault(entity_type.get_admin_name(), {})
        for authority in authorities:
            et_data[authority.get_admin_name()] = EntityTypePropertyAssertion.objects.filter_by_authority_entity_type(authority, entity_type).count()
    for entity_relationship_type in EntityRelationshipType.objects.all():
        ert_data = entity_relationship_stats.setdefault(entity_relationship_type.get_admin_name(), {})
        for authority in authorities:
            ert_data[authority.get_admin_name()] = EntityRelationshipPropertyAssertion.objects.filter_by_authority_entity_relationship_type(authority, entity_relationship_type).count()
    context_data = {
        'number_entities': number_entities,
        'entity_type_stats': entity_type_stats,
        'entity_relationship_stats': entity_relationship_stats,
        'authorities': [authority.get_admin_name() for authority in authorities],
    }
    return render(request, 'eats/display/statistics.html', context_data)
