# Generated by Django 4.1 on 2022-09-02 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_tags_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipes',
            old_name='description',
            new_name='text',
        ),
    ]
