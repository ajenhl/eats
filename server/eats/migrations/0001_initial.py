# -*- coding: utf-8 -*-


from django.db import models, migrations
import eats.models.infrastructure
from django.conf import settings
import eats.models.property_assertion
import eats.models.name_element


class Migration(migrations.Migration):

    dependencies = [
        ('tmapi', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='EATSMLImport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
                ('raw_xml', models.TextField()),
                ('annotated_xml', models.TextField()),
                ('import_date', models.DateTimeField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='EATSUser',
            fields=[
                ('user', models.OneToOneField(related_name='eats_user', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NameCache',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('form', models.CharField(max_length=800)),
                ('is_preferred', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='NameIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('form', models.CharField(max_length=800)),
            ],
        ),
        migrations.CreateModel(
            name='Authority',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': 'authorities',
            },
            bases=('tmapi.topic', eats.models.infrastructure.Infrastructure),
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.topic', eats.models.infrastructure.Infrastructure),
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.topic',),
        ),
        migrations.CreateModel(
            name='DatePart',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.name',),
        ),
        migrations.CreateModel(
            name='DatePeriod',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.topic', eats.models.infrastructure.Infrastructure),
        ),
        migrations.CreateModel(
            name='DateType',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.topic', eats.models.infrastructure.Infrastructure),
        ),
        migrations.CreateModel(
            name='EATSTopicMap',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.topicmap',),
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.topic',),
        ),
        migrations.CreateModel(
            name='EntityRelationshipPropertyAssertion',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.association', eats.models.property_assertion.PropertyAssertion),
        ),
        migrations.CreateModel(
            name='EntityRelationshipType',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.topic', eats.models.infrastructure.Infrastructure),
        ),
        migrations.CreateModel(
            name='EntityType',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.topic', eats.models.infrastructure.Infrastructure),
        ),
        migrations.CreateModel(
            name='EntityTypePropertyAssertion',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.association', eats.models.property_assertion.PropertyAssertion),
        ),
        migrations.CreateModel(
            name='ExistencePropertyAssertion',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.association', eats.models.property_assertion.PropertyAssertion),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.topic', eats.models.infrastructure.Infrastructure),
        ),
        migrations.CreateModel(
            name='Name',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.topic', eats.models.name_element.NameElement),
        ),
        migrations.CreateModel(
            name='NamePart',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.topic', eats.models.name_element.NameElement),
        ),
        migrations.CreateModel(
            name='NamePartType',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.topic', eats.models.infrastructure.Infrastructure),
        ),
        migrations.CreateModel(
            name='NamePropertyAssertion',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.association', eats.models.property_assertion.PropertyAssertion),
        ),
        migrations.CreateModel(
            name='NameType',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.topic', eats.models.infrastructure.Infrastructure),
        ),
        migrations.CreateModel(
            name='NotePropertyAssertion',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.occurrence', eats.models.property_assertion.PropertyAssertion),
        ),
        migrations.CreateModel(
            name='Script',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.topic', eats.models.infrastructure.Infrastructure),
        ),
        migrations.CreateModel(
            name='SubjectIdentifierPropertyAssertion',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tmapi.occurrence', eats.models.property_assertion.PropertyAssertion),
        ),
        migrations.CreateModel(
            name='EntityRelationshipCache',
            fields=[
                ('entity_relationship', models.OneToOneField(related_name='cached_relationship', primary_key=True, serialize=False, to='eats.EntityRelationshipPropertyAssertion')),
                ('forward_relationship_name', models.TextField()),
                ('reverse_relationship_name', models.TextField()),
                ('authority', models.ForeignKey(related_name='cached_entity_relationships', to='eats.Authority')),
                ('domain_entity', models.ForeignKey(related_name='domain_relationships', to='eats.Entity')),
                ('range_entity', models.ForeignKey(related_name='range_relationships', to='eats.Entity')),
                ('relationship_type', models.ForeignKey(related_name='cached_relationships', to='eats.EntityRelationshipType')),
            ],
        ),
        migrations.AddField(
            model_name='nameindex',
            name='entity',
            field=models.ForeignKey(related_name='indexed_names', to='eats.Entity'),
        ),
        migrations.AddField(
            model_name='nameindex',
            name='name',
            field=models.ForeignKey(related_name='indexed_name_forms', to='eats.Name'),
        ),
        migrations.AddField(
            model_name='nameindex',
            name='name_part',
            field=models.ForeignKey(related_name='indexed_name_part_forms', blank=True, to='eats.NamePart', null=True),
        ),
        migrations.AddField(
            model_name='namecache',
            name='assertion',
            field=models.OneToOneField(related_name='cached_name', to='eats.NamePropertyAssertion'),
        ),
        migrations.AddField(
            model_name='namecache',
            name='authority',
            field=models.ForeignKey(to='eats.Authority'),
        ),
        migrations.AddField(
            model_name='namecache',
            name='entity',
            field=models.ForeignKey(related_name='cached_names', to='eats.Entity'),
        ),
        migrations.AddField(
            model_name='namecache',
            name='language',
            field=models.ForeignKey(to='eats.Language'),
        ),
        migrations.AddField(
            model_name='namecache',
            name='name',
            field=models.OneToOneField(related_name='cached_name', to='eats.Name'),
        ),
        migrations.AddField(
            model_name='namecache',
            name='script',
            field=models.ForeignKey(to='eats.Script'),
        ),
        migrations.AddField(
            model_name='eatsuser',
            name='authority',
            field=models.ForeignKey(related_name='authority_users', to='eats.Authority', null=True),
        ),
        migrations.AddField(
            model_name='eatsuser',
            name='current_authority',
            field=models.ForeignKey(related_name='current_editors', to='eats.Authority', null=True),
        ),
        migrations.AddField(
            model_name='eatsuser',
            name='editable_authorities',
            field=models.ManyToManyField(related_name='editors', to='eats.Authority'),
        ),
        migrations.AddField(
            model_name='eatsuser',
            name='language',
            field=models.ForeignKey(related_name='language_users', to='eats.Language', null=True),
        ),
        migrations.AddField(
            model_name='eatsuser',
            name='script',
            field=models.ForeignKey(related_name='script_users', to='eats.Script', null=True),
        ),
        migrations.AddField(
            model_name='eatsmlimport',
            name='importer',
            field=models.ForeignKey(related_name='eatsml_imports', to='eats.EATSUser'),
        ),
    ]
