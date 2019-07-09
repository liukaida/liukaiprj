# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0002_auto_20181101_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranswer',
            name='quest_type',
            field=models.CharField(max_length=50, verbose_name='\u9898\u76ee\u7c7b\u578b'),
        ),
    ]
