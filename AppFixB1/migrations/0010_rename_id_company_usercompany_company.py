# Generated by Django 4.2.3 on 2023-07-20 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppFixB1', '0009_alter_report_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercompany',
            old_name='id_company',
            new_name='company',
        ),
    ]
