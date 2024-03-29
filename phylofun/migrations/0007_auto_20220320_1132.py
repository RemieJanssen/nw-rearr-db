# Generated by Django 3.2.12 on 2022-03-20 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phylofun', '0006_auto_20220320_1125'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='networkmodel',
            options={'ordering': ['binary', 'number_of_roots', 'number_of_leaves', 'reticulation_number']},
        ),
        migrations.AddField(
            model_name='networkmodel',
            name='reticulation_number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
