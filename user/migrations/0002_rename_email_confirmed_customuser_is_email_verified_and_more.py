# Generated by Django 5.1.6 on 2025-03-05 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='email_confirmed',
            new_name='is_email_verified',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='activation_key',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='key_expires',
        ),
    ]
