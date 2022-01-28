# Generated by Django 3.2.8 on 2021-10-21 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phylofun', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NetworkModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nodes', models.TextField()),
                ('edges', models.TextField()),
                ('labels', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='RearrangementProblemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('move_type', models.SmallIntegerField(choices=[(0, 'no moves'), (1, 'tail moves'), (2, 'head moves'), (3, 'rSPR moves')], verbose_name='move type')),
                ('vertical_allowed', models.BooleanField(default=False)),
                ('network1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems1', to='phylofun.networkmodel')),
                ('network2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems2', to='phylofun.networkmodel')),
            ],
        ),
        migrations.RemoveField(
            model_name='rearrangementproblem',
            name='network1',
        ),
        migrations.RemoveField(
            model_name='rearrangementproblem',
            name='network2',
        ),
        migrations.RenameModel(
            old_name='Solution',
            new_name='SolutionModel',
        ),
        migrations.DeleteModel(
            name='Network',
        ),
        migrations.DeleteModel(
            name='RearrangementProblem',
        ),
        migrations.AlterField(
            model_name='solutionmodel',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='phylofun.rearrangementproblemmodel'),
        ),
    ]
