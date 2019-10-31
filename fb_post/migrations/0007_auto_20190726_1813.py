# Generated by Django 2.2.1 on 2019-07-26 18:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('fb_post', '0006_auto_20190726_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
            preserve_default=False,
        ),
    ]