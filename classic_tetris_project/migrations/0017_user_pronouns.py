# Generated by Django 2.2.4 on 2020-04-01 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classic_tetris_project', '0016_auto_20200318_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pronouns',
            field=models.CharField(choices=[('he', 'He/him/his'), ('she', 'She/her/hers'), ('they', 'They/them/theirs')], default='they', max_length=16),
        ),
    ]