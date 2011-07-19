from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from eats.lib.property_assertions import EntityRelationshipPropertyAssertions, EntityTypePropertyAssertions, ExistencePropertyAssertions, NamePropertyAssertions, NotePropertyAssertions
from eats.decorators import add_topic_map
from eats.forms.edit import CreateEntityForm, create_choice_list, DateForm
from eats.models import Authority, Calendar, DatePeriod, DateType, EATSUser, Entity


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
            return HttpResponseRedirect(redirect_url)
    else:
        form = CreateEntityForm(topic_map, authorities)
    context_data = {'form': form}
    return render_to_response('eats/edit/entity_add.html', context_data,
                              context_instance=RequestContext(request))

@user_passes_test(user_is_editor)
@add_topic_map
def entity_change (request, topic_map, entity_id):
    try:
        entity = Entity.objects.get_by_identifier(entity_id)
    except Entity.DoesNotExist:
        raise Http404
    context_data = {'entity': entity}
    authority = request.user.eats_user.get_current_authority()
    data = request.POST or None
    existences = ExistencePropertyAssertions(topic_map, entity, authority, data)
    entity_types = EntityTypePropertyAssertions(topic_map, entity, authority,
                                                data)
    names = NamePropertyAssertions(topic_map, entity, authority, data)
    notes = NotePropertyAssertions(topic_map, entity, authority, data)
    entity_relationships = EntityRelationshipPropertyAssertions(
        topic_map, entity, authority, data)
    existences_formset = existences.formset
    entity_types_formset = entity_types.formset
    names_formset = names.formset
    notes_formset = notes.formset
    entity_relationships_formset = entity_relationships.formset
    if request.method == 'POST':
        is_valid = False
        for formset in (existences_formset, entity_types_formset, names_formset,
                        notes_formset, entity_relationships_formset):
            is_valid = formset.is_valid()
            if not is_valid:
                break
        if is_valid:
            for formset in (existences_formset, entity_types_formset,
                            names_formset, notes_formset,
                            entity_relationships_formset):
                formset.save()
            redirect_url = reverse('entity-change',
                                   kwargs={'entity_id': entity_id})
            return HttpResponseRedirect(redirect_url)
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
    return render_to_response('eats/edit/entity_change.html', context_data,
                              context_instance=RequestContext(request))

@user_passes_test(user_is_editor)
@add_topic_map
def date_add (request, topic_map, entity_id, assertion_id):
    try:
        entity = Entity.objects.get_by_identifier(entity_id)
    except Entity.DoesNotExist:
        raise Http404
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
            return HttpResponseRedirect(redirect_url)
    else:
        form = DateForm(topic_map, calendar_choices, date_period_choices,
                        date_type_choices)
    context_data = {'form': form}
    return render_to_response('eats/edit/date_add.html', context_data,
                              context_instance=RequestContext(request))

@user_passes_test(user_is_editor)
@add_topic_map
def date_change (request, topic_map, entity_id, assertion_id, date_id):
    try:
        entity = Entity.objects.get_by_identifier(entity_id)
    except Entity.DoesNotExist:
        raise Http404
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
            return HttpResponseRedirect(redirect_url)
        if form.is_valid():
            date_id = form.save()
            if '_continue' in form.data:
                redirect_ids['assertion_id'] = assertion_id
                redirect_ids['date_id'] = date_id
                redirect_url = reverse('date-change', kwargs=redirect_ids)
            return HttpResponseRedirect(redirect_url)
    else:
        form = DateForm(topic_map, calendar_choices, date_period_choices,
                        date_type_choices, instance=date)
    context_data = {'form': form}
    return render_to_response('eats/edit/date_change.html', context_data,
                              context_instance=RequestContext(request))
