# Generated by Django 5.1.1 on 2024-10-09 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_rename_status_bookrecord_action_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookrecord',
            name='issue_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
