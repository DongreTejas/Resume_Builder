# Generated by Django 4.1.3 on 2023-01-08 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_rename_cskill_profile_csskill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
