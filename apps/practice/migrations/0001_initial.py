# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quest_type', models.PositiveSmallIntegerField(verbose_name='\u9898\u76ee\u7c7b\u578b')),
                ('answer_type', models.PositiveSmallIntegerField(verbose_name='\u7b54\u6848\u79cd\u7c7b', choices=[(1, '\u5355\u9009'), (2, '\u591a\u9009'), (2, '\u586b\u7a7a')])),
                ('quest_title', models.TextField(null=True, verbose_name='\u9898\u76ee', blank=True)),
                ('title_appendattr', models.CharField(max_length=30, null=True, verbose_name='\u9898\u76ee\u9644\u4ef6\u5c5e\u6027', blank=True)),
                ('quest_detail', models.TextField(null=True, verbose_name='\u9898\u76ee\u8be6\u60c5JSON', blank=True)),
                ('answer_detail', models.TextField(null=True, verbose_name='\u7b54\u6848\u8be6\u60c5JSON', blank=True)),
                ('weight', models.IntegerField(default=1, null=True, verbose_name='\u6743\u91cd', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('del_flag', models.IntegerField(default=0, verbose_name='\u662f\u5426\u5220\u9664', choices=[(1, '\u662f'), (0, '\u5426')])),
            ],
            options={
                'db_table': 'question_define',
                'verbose_name': '\u9898\u76ee\u5b9a\u4e49\u8868',
                'verbose_name_plural': '\u9898\u76ee\u5b9a\u4e49\u8868',
            },
        ),
    ]
