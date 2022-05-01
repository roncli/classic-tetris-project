# Generated by Django 3.2.11 on 2022-05-01 07:20

from django.db import migrations, models


def backfill_withdrawals_allowed(apps, schema_editor):
    Event = apps.get_model("classic_tetris_project", "Event")
    Event.objects.update(withdrawals_allowed=models.F("qualifying_open"))


class Migration(migrations.Migration):

    dependencies = [
        ('classic_tetris_project', '0066_match_synced_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='withdrawals_allowed',
            field=models.BooleanField(default=True, help_text='Controls whether users can withdraw their own qualifiers. Automatically disabled when tournaments are seeded.'),
        ),
        migrations.RunPython(backfill_withdrawals_allowed, migrations.RunPython.noop),
    ]
