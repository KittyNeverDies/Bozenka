# Generated by Django 5.0.7 on 2024-07-28 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0003_community_short_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='icon',
            field=models.ImageField(upload_to='images/community_icons', verbose_name='Icon'),
        ),
        migrations.AlterField(
            model_name='communitymanager',
            name='avatar',
            field=models.ImageField(upload_to='images\\manager_avatars', verbose_name='Avatar'),
        ),
    ]
