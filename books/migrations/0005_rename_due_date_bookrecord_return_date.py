# Generated by Django 5.1.1 on 2024-10-09 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_bookrecord_issue_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookrecord',
            old_name='due_date',
            new_name='return_date',
        ),
    ]
