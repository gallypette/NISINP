# Generated by Django 4.2 on 2023-08-28 07:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import parler.fields
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='Administrator')),
                ('phone_number', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('email', models.EmailField(error_messages={'unique': 'A user is already registered with this email address'}, max_length=254, unique=True, verbose_name='email address')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_regulator', models.BooleanField(default=False, verbose_name='Regulator')),
                ('identifier', models.CharField(max_length=64, verbose_name='Identifier')),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('country', models.CharField(max_length=64, verbose_name='country')),
                ('address', models.CharField(max_length=255, verbose_name='address')),
                ('email', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='email address')),
                ('phone_number', models.CharField(blank=True, default=None, max_length=30, null=True, verbose_name='phone number')),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='Impact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_generic_impact', models.BooleanField(default=False, verbose_name='Generic Impact')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PredifinedAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allowed_additional_answer', models.BooleanField(default=False, verbose_name='Additional Answer')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='QuestionCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Question Category',
                'verbose_name_plural': 'Question Categories',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RegulationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accronym', models.CharField(blank=True, default=None, max_length=4, null=True)),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='nisinp.sector', verbose_name='parent')),
                ('specific_impact', models.ManyToManyField(default=None, to='nisinp.impact')),
            ],
            options={
                'verbose_name': 'Sector',
                'verbose_name_plural': 'Sectors',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nisinp.sector')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(choices=[('FREETEXT', 'Freetext'), ('MULTI', 'Multiple Choice'), ('SO', 'Single Option Choice'), ('MT', 'Multiple Choice + Free Text'), ('ST', 'Single Choice + Free Text'), ('CL', 'Countries list'), ('DATE', 'Date picker')], default='FREETEXT', max_length=10)),
                ('is_mandatory', models.BooleanField(default=False, verbose_name='Mandatory')),
                ('is_preliminary', models.BooleanField(default=False, verbose_name='Preliminary')),
                ('position', models.IntegerField()),
                ('category', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nisinp.questioncategory')),
                ('predifined_answers', models.ManyToManyField(blank=True, to='nisinp.predifinedanswer')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ïncident_id', models.CharField(max_length=22, verbose_name='Incident identifier')),
                ('preliminary_notification_date', models.DateField(default=datetime.date.today)),
                ('company_name', models.CharField(max_length=100, verbose_name='Company name')),
                ('contact_lastname', models.CharField(max_length=100, verbose_name='contact lastname')),
                ('contact_firstname', models.CharField(max_length=100, verbose_name='contact firstname')),
                ('contact_title', models.CharField(max_length=100, verbose_name='contact title')),
                ('contact_email', models.CharField(max_length=100, verbose_name='contact email')),
                ('contact_telephone', models.CharField(max_length=100, verbose_name='contact telephone')),
                ('technical_lastname', models.CharField(max_length=100, verbose_name='technical lastname')),
                ('technical_firstname', models.CharField(max_length=100, verbose_name='technical firstname')),
                ('technical_title', models.CharField(max_length=100, verbose_name='technical title')),
                ('technical_email', models.CharField(max_length=100, verbose_name='technical email')),
                ('technical_telephone', models.CharField(max_length=100, verbose_name='technical telephone')),
                ('incident_reference', models.CharField(max_length=255)),
                ('complaint_reference', models.CharField(max_length=255)),
                ('final_notification_date', models.DateField(blank=True, null=True)),
                ('is_significative_impact', models.BooleanField(default=False, verbose_name='Significative impact')),
                ('affected_services', models.ManyToManyField(to='nisinp.services')),
                ('company', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nisinp.company')),
                ('contact_user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('impacts', models.ManyToManyField(default=None, to='nisinp.impact')),
                ('regulations', models.ManyToManyField(to='nisinp.regulationtype')),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='sectors',
            field=models.ManyToManyField(to='nisinp.sector'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(blank=True, null=True)),
                ('PredifinedAnswer', models.ManyToManyField(blank=True, to='nisinp.predifinedanswer')),
                ('incident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nisinp.incident')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nisinp.question')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='companies',
            field=models.ManyToManyField(to='nisinp.company'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='sectors',
            field=models.ManyToManyField(to='nisinp.sector'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='ServicesTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=100)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='nisinp.services')),
            ],
            options={
                'verbose_name': 'Service Translation',
                'db_table': 'nisinp_services_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SectorTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=100)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='nisinp.sector')),
            ],
            options={
                'verbose_name': 'Sector Translation',
                'db_table': 'nisinp_sector_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RegulationTypeTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('label', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='nisinp.regulationtype')),
            ],
            options={
                'verbose_name': 'regulation type Translation',
                'db_table': 'nisinp_regulationtype_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='QuestionTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('label', models.TextField()),
                ('tooltip', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='nisinp.question')),
            ],
            options={
                'verbose_name': 'question Translation',
                'db_table': 'nisinp_question_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='QuestionCategoryTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('label', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='nisinp.questioncategory')),
            ],
            options={
                'verbose_name': 'Question Category Translation',
                'db_table': 'nisinp_questioncategory_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PredifinedAnswerTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('predifined_answer', models.TextField()),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='nisinp.predifinedanswer')),
            ],
            options={
                'verbose_name': 'predifined answer Translation',
                'db_table': 'nisinp_predifinedanswer_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ImpactTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('label', models.TextField()),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='nisinp.impact')),
            ],
            options={
                'verbose_name': 'impact Translation',
                'db_table': 'nisinp_impact_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
