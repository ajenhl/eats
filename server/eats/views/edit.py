import io

from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import get_object_or_404, redirect, render

from lxml import etree

from eats.constants import UNNAMED_ENTITY_NAME
from eats.exceptions import EATSMergedIdentifierException
from eats.lib.eatsml_exporter import EATSMLExporter
from eats.lib.eatsml_importer import EATSMLImporter
from eats.lib.property_assertions import EntityRelationshipPropertyAssertions, EntityTypePropertyAssertions, ExistencePropertyAssertions, NamePropertyAssertions, NotePropertyAssertions, SubjectIdentifierPropertyAssertions
from eats.lib.user import get_user_preferences, user_is_editor
from eats.lib.views import get_topic_or_404
from eats.decorators import add_topic_map
from eats.forms.edit import CreateEntityForm, create_choice_list, CurrentAuthorityForm, DateForm, EATSMLImportForm, EntityMergeForm
from eats.models import Authority, Calendar, DatePeriod, DateType, EATSMLImport, Entity, EntityType


@user_passes_test(user_is_editor)
@add_topic_map
def entity_add (request, topic_map):
    editor = request.user.eats_user
    authorities = editor.editable_authorities.all()
    if request.method == 'POST':
        form = CreateEntityForm(topic_map, authorities, request.POST)
        if form.is_valid():
            authority_id = form.cleaned_data['authority']
            authority = Authority.objects.get_by_identifier(authority_id)
            if authority != editor.get_current_authority():
                editor.set_current_authority(authority)
            entity = topic_map.create_entity(authority)
            redirect_url = reverse('entity-change',
                                   kwargs={'entity_id': entity.get_id()})
            return redirect(redirect_url)
    else:
        form = CreateEntityForm(topic_map, authorities)
    context_data = {'form': form}
    return render(request, 'eats/edit/entity_add.html', context_data)

@user_passes_test(user_is_editor)
@add_topic_map
def entity_change (request, topic_map, entity_id):
    try:
        entity = get_topic_or_404(Entity, entity_id)
    except EATSMergedIdentifierException as e:
        return redirect('entity-change', entity_id=e.new_id, permanent=True)
    editor = request.user.eats_user
    context_data = {'entity': entity, 'is_valid': True}
    authority = editor.get_current_authority()
    editable_authorities = editor.editable_authorities.all()
    authority_data = {'current_authority': authority.get_id()}
    entity_data = None
    if request.method == 'POST':
        if '_change_authority' in request.POST:
            authority_data = request.POST
        else:
            entity_data = request.POST
    current_authority_form = CurrentAuthorityForm(
        topic_map, editable_authorities, authority_data)
    existences = ExistencePropertyAssertions(topic_map, entity, authority,
                                             entity_data)
    entity_types = EntityTypePropertyAssertions(topic_map, entity, authority,
                                                entity_data)
    names = NamePropertyAssertions(topic_map, entity, authority, entity_data)
    notes = NotePropertyAssertions(topic_map, entity, authority, entity_data)
    entity_relationships = EntityRelationshipPropertyAssertions(
        topic_map, entity, authority, entity_data)
    subject_identifiers = SubjectIdentifierPropertyAssertions(
        topic_map, entity, authority, entity_data)
    existences_formset = existences.formset
    entity_types_formset = entity_types.formset
    names_formset = names.formset
    notes_formset = notes.formset
    entity_relationships_formset = entity_relationships.formset
    subject_identifiers_formset = subject_identifiers.formset
    if request.method == 'POST':
        redirect_url = reverse('entity-change', kwargs={'entity_id': entity_id})
        if '_change_authority' in request.POST:
            if current_authority_form.is_valid():
                authority_id = current_authority_form.cleaned_data[
                    'current_authority']
                authority = Authority.objects.get_by_identifier(authority_id)
                editor.set_current_authority(authority)
                return redirect(redirect_url)
        else:
            formsets = (existences_formset, entity_types_formset,
                        names_formset, notes_formset,
                        entity_relationships_formset,
                        subject_identifiers_formset)
            is_valid = False
            for formset in formsets:
                is_valid = formset.is_valid()
                if not is_valid:
                    context_data['is_valid'] = False
                    break
            if is_valid:
                for formset in formsets:
                    formset.save()
                if '_save_add' in request.POST:
                    redirect_url = reverse('entity-add')
                return redirect(redirect_url)
    context_data['entity_id'] = entity_id
    context_data['current_authority_form'] = current_authority_form
    context_data['existence_non_editable'] = existences.non_editable
    context_data['existence_formset'] = existences_formset
    context_data['entity_type_non_editable'] = entity_types.non_editable
    context_data['entity_type_formset'] = entity_types_formset
    context_data['name_non_editable'] = names.non_editable
    context_data['name_formset'] = names_formset
    context_data['note_formset'] = notes_formset
    context_data['note_non_editable'] = notes.non_editable
    context_data['entity_relationship_formset'] = entity_relationships_formset
    context_data['entity_relationship_non_editable'] = entity_relationships.non_editable
    context_data['subject_identifier_formset'] = subject_identifiers_formset
    context_data['subject_identifier_non_editable'] = subject_identifiers.non_editable
    context_data['property_assertion_full_certainty'] = \
        topic_map.property_assertion_full_certainty
    user_preferences = get_user_preferences(request)
    context_data.update(user_preferences)
    preferred_name_assertion = entity.get_preferred_name(
        user_preferences['preferred_authority'],
        user_preferences['preferred_language'],
        user_preferences['preferred_script'])
    if preferred_name_assertion:
        context_data['preferred_name'] = preferred_name_assertion.name.assembled_form
    else:
        context_data['preferred_name'] = UNNAMED_ENTITY_NAME
    return render(request, 'eats/edit/entity_change.html', context_data)

@user_passes_test(user_is_editor)
@add_topic_map
def entity_delete (request, topic_map, entity_id):
    try:
        entity = get_topic_or_404(Entity, entity_id)
    except EATSMergedIdentifierException as e:
        return redirect('entity-delete', entity_id=e.new_id, permanent=True)
    editable_authorities = request.user.eats_user.editable_authorities.all()
    assertion_getters = [entity.get_eats_names, entity.get_entity_relationships,
                         entity.get_entity_types, entity.get_existences,
                         entity.get_eats_subject_identifiers, entity.get_notes]
    can_delete = True
    for assertion_getter in assertion_getters:
        for assertion in assertion_getter():
            if assertion.authority not in editable_authorities:
                can_delete = False
    if request.method == 'POST' and can_delete:
        entity.remove()
        return redirect(reverse('search'))
    context_data = {'can_delete': can_delete}
    return render(request, 'eats/edit/entity_delete.html', context_data)

@user_passes_test(user_is_editor)
@add_topic_map
def entity_merge (request, topic_map, entity_id):
    try:
        entity = get_topic_or_404(Entity, entity_id)
    except EATSMergedIdentifierException as e:
        return redirect('entity-merge', entity_id=e.new_id, permanent=True)
    context_data = {}
    if request.method == 'POST':
        form = EntityMergeForm(request.POST)
        if form.is_valid():
            merge_entity = form.cleaned_data['merge_entity']
            editable_authorities = request.user.eats_user.editable_authorities.all()
            assertion_getters = ['get_eats_names', 'get_entity_relationships',
                                 'get_entity_types', 'get_existences',
                                 'get_eats_subject_identifiers', 'get_notes']
            can_merge = True
            for assertion_getter in assertion_getters:
                for assertion in getattr(merge_entity, assertion_getter)():
                    if assertion.authority not in editable_authorities:
                        can_merge = False
            if can_merge:
                entity.merge_in(merge_entity)
                return redirect(
                    reverse('entity-change', kwargs={'entity_id': entity_id}))
            else:
                context_data['unauthorised'] = True
    else:
        form = EntityMergeForm()
    context_data['form'] = form
    return render(request, 'eats/edit/entity_merge.html', context_data)

@user_passes_test(user_is_editor)
@add_topic_map
def date_add (request, topic_map, entity_id, assertion_id):
    entity = get_topic_or_404(Entity, entity_id)
    assertion = entity.get_assertion(assertion_id)
    if assertion is None:
        raise Http404
    authority = assertion.authority
    if authority != request.user.eats_user.get_current_authority():
        raise Http404
    calendar_choices = create_choice_list(
        topic_map, Calendar.objects.filter_by_authority(authority))
    date_period_choices = create_choice_list(
        topic_map, DatePeriod.objects.filter_by_authority(authority))
    date_type_choices = create_choice_list(
        topic_map, DateType.objects.filter_by_authority(authority))
    if request.method == 'POST':
        form = DateForm(topic_map, calendar_choices, date_period_choices,
                        date_type_choices, request.POST)
        if form.is_valid():
            date_id = form.save(assertion)
            if '_continue' in form.data:
                redirect_ids = {'assertion_id': assertion_id,
                                'date_id': date_id, 'entity_id': entity_id}
                redirect_url = reverse('date-change', kwargs=redirect_ids)
            else:
                redirect_ids = {'entity_id': entity_id}
                redirect_url = reverse('entity-change', kwargs=redirect_ids)
            return redirect(redirect_url)
    else:
        form = DateForm(topic_map, calendar_choices, date_period_choices,
                        date_type_choices)
    context_data = {'form': form}
    return render(request, 'eats/edit/date_add.html', context_data)

@user_passes_test(user_is_editor)
@add_topic_map
def date_change (request, topic_map, entity_id, assertion_id, date_id):
    entity = get_topic_or_404(Entity, entity_id)
    assertion = entity.get_assertion(assertion_id)
    if assertion is None:
        raise Http404
    date = assertion.get_date(date_id)
    if date is None:
        raise Http404
    authority = assertion.authority
    if authority != request.user.eats_user.get_current_authority():
        raise Http404
    calendar_choices = create_choice_list(
        topic_map, Calendar.objects.filter_by_authority(authority))
    date_period_choices = create_choice_list(
        topic_map, DatePeriod.objects.filter_by_authority(authority))
    date_type_choices = create_choice_list(
        topic_map, DateType.objects.filter_by_authority(authority))
    if request.method == 'POST':
        form = DateForm(topic_map, calendar_choices, date_period_choices,
                        date_type_choices, request.POST, instance=date)
        redirect_ids = {'entity_id': entity_id}
        redirect_url = reverse('entity-change', kwargs=redirect_ids)
        if '_delete' in form.data:
            form.delete()
            return redirect(redirect_url)
        if form.is_valid():
            date_id = form.save()
            if '_continue' in form.data:
                redirect_ids['assertion_id'] = assertion_id
                redirect_ids['date_id'] = date_id
                redirect_url = reverse('date-change', kwargs=redirect_ids)
            return redirect(redirect_url)
    else:
        form = DateForm(topic_map, calendar_choices, date_period_choices,
                        date_type_choices, instance=date)
    context_data = {'form': form}
    return render(request, 'eats/edit/date_change.html', context_data)

@user_passes_test(user_is_editor)
@add_topic_map
def export_eatsml_base (request, topic_map):
    tree = EATSMLExporter(topic_map).export_infrastructure(
        user=request.user.eats_user)
    return serialise_tree(tree)

@user_passes_test(user_is_editor)
@add_topic_map
def export_eatsml_entities (request, topic_map):
    """Exports all entities in EATSML."""
    entities = Entity.objects.all()
    tree = EATSMLExporter(topic_map).export_entities(entities)
    return serialise_tree(tree)

@user_passes_test(user_is_editor)
@add_topic_map
def export_eatsml_entities_by_entity_type (request, topic_map, entity_type_id):
    entity_type = get_topic_or_404(EntityType, entity_type_id)
    entities = Entity.objects.filter_by_entity_type(entity_type)
    tree = EATSMLExporter(topic_map).export_entities(entities)
    return serialise_tree(tree)

@user_passes_test(user_is_editor)
@add_topic_map
def export_eatsml_full (request, topic_map):
    """Exports all EATS data in EATSML."""
    tree = EATSMLExporter(topic_map).export_full()
    return serialise_tree(tree)

def serialise_tree (tree):
    xml = etree.tostring(tree, encoding='utf-8', pretty_print=True)
    return HttpResponse(xml, content_type='text/xml')

@user_passes_test(user_is_editor)
@add_topic_map
def import_eatsml (request, topic_map):
    """Imports a POSTed EATSML file."""
    if request.method == 'POST':
        form = EATSMLImportForm(request.POST, request.FILES)
        user = request.user.eats_user
        if form.is_valid():
            eatsml_file = io.BytesIO()
            for chunk in request.FILES['import_file'].chunks():
                eatsml_file.write(chunk)
            eatsml_file.seek(0)
            # QAZ: After dealing with the uploaded file in chunks
            # above, to prevent overwhelming the system with a huge
            # file, straightaway the whole value is retrieved and
            # passed to the importer.
            eatsml = eatsml_file.getvalue()
            try:
                with transaction.atomic():
                    import_tree, annotated_tree = EATSMLImporter(
                        topic_map).import_xml(eatsml, user)
            except Exception as e:
                response = render(request, '500.html', {'message': e})
                response.status_code = 500
                return response
            description = form.cleaned_data['description']
            imported_xml = etree.tostring(import_tree, encoding='utf-8',
                                          pretty_print=True)
            annotated_xml = etree.tostring(annotated_tree, encoding='utf-8',
                                           pretty_print=True)
            eatsml_import = EATSMLImport(
                importer=user, description=description, raw_xml=imported_xml,
                annotated_xml=annotated_xml)
            eatsml_import.save()
            redirect_url = reverse('display-eatsml-import',
                                   kwargs={'import_id': eatsml_import.id})
            return redirect(redirect_url)
    else:
        form = EATSMLImportForm()
    import_list = EATSMLImport.objects.values('id', 'importer__user__username',
                                              'description', 'import_date')
    paginator = Paginator(import_list, 100)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        imports = paginator.page(page)
    except (EmptyPage, InvalidPage):
        imports = paginator.page(paginator.num_pages)
    context_data = {'form': form, 'imports': imports}
    return render(request, 'eats/edit/eatsml_import.html', context_data)

@user_passes_test(user_is_editor)
def display_eatsml_import (request, import_id):
    eatsml_import = get_object_or_404(EATSMLImport, pk=import_id)
    context_data = {'import': eatsml_import}
    return render(request, 'eats/edit/eatsml_import_display.html', context_data)

@user_passes_test(user_is_editor)
def display_eatsml_import_raw (request, import_id):
    eatsml_import = get_object_or_404(EATSMLImport, pk=import_id)
    return HttpResponse(eatsml_import.raw_xml, content_type='text/xml')

@user_passes_test(user_is_editor)
def display_eatsml_import_annotated (request, import_id):
    eatsml_import = get_object_or_404(EATSMLImport, pk=import_id)
    return HttpResponse(eatsml_import.annotated_xml, content_type='text/xml')
