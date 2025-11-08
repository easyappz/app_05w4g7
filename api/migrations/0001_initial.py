# Generated migration

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(help_text="Guest username like 'Гость-1234'", max_length=50)),
                ('message_text', models.TextField(help_text='Message text, max 1000 characters', validators=[django.core.validators.MaxLengthValidator(1000)])),
                ('timestamp', models.DateTimeField(auto_now_add=True, help_text='Message creation timestamp')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ActiveUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(help_text='Unique session identifier', max_length=255, unique=True)),
                ('username', models.CharField(help_text='Guest username', max_length=50)),
                ('last_activity', models.DateTimeField(auto_now=True, help_text='Last activity timestamp')),
            ],
            options={
                'verbose_name': 'Active User',
                'verbose_name_plural': 'Active Users',
            },
        ),
    ]
