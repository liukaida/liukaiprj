# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=30, null=True, verbose_name='\u7528\u6237\u540d\u79f0', blank=True)),
                ('question_uuid', models.CharField(max_length=30, null=True, verbose_name='\u5f53\u6b21\u9898\u76ee\u552f\u4e00\u6807\u8bc6', blank=True)),
                ('question_count_total', models.IntegerField(default=0, null=True, verbose_name='\u9898\u76ee\u603b\u6570', blank=True)),
                ('question_count_err', models.IntegerField(default=0, null=True, verbose_name='\u9519\u9898\u603b\u6570', blank=True)),
                ('useranswer_detail', models.TextField(null=True, verbose_name='\u7528\u6237\u7b54\u6848\u8be6\u60c5JSON', blank=True)),
                ('duration', models.CharField(max_length=30, null=True, verbose_name='\u65f6\u957f', blank=True)),
                ('quest_type', models.PositiveSmallIntegerField(verbose_name='\u9898\u76ee\u7c7b\u578b')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('del_flag', models.IntegerField(default=0, verbose_name='\u662f\u5426\u5220\u9664', choices=[(1, '\u662f'), (0, '\u5426')])),
            ],
            options={
                'db_table': 'question_user_answer',
                'verbose_name': '\u7528\u6237\u7b54\u6848',
                'verbose_name_plural': '\u7528\u6237\u7b54\u6848',
            },
        ),
        migrations.AlterField(
            model_name='question',
            name='answer_type',
            field=models.PositiveSmallIntegerField(verbose_name='\u7b54\u6848\u79cd\u7c7b', choices=[(1, '\u5355\u9009'), (2, '\u591a\u9009'), (3, '\u586b\u7a7a')]),
        ),
        migrations.AlterField(
            model_name='question',
            name='title_appendattr',
            field=models.CharField(max_length=30, null=True, verbose_name='\u9898\u76ee\u9644\u52a0\u5c5e\u6027', blank=True),
        ),
    ]
