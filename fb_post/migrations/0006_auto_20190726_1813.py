# Generated by Django 2.2.1 on 2019-07-26 18:13

from django.db import migrations
import uuid


def gen_uuid(apps, schema_editor):
    MyModel = apps.get_model('fb_post', 'Person')
    for row in MyModel.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('fb_post', '0005_person_uuid'),
    ]

    operations = [
        migrations.RunPython(gen_uuid),
    ]