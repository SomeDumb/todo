# Generated by Django 4.0.6 on 2022-07-12 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_todolist_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='order',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
    ]
