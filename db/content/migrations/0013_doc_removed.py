# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0012_markdowntype_deprecated'),
    ]

    operations = [
        migrations.AddField(
            model_name='doc',
            name='removed',
            field=models.BooleanField(default=False),
        ),
    ]
