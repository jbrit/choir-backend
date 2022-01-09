# Generated by Django 3.2.6 on 2022-01-09 18:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rehearsal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField(null=True)),
                ('category', models.CharField(choices=[('Suggested', 'Suggested')], max_length=100)),
                ('attendees', models.ManyToManyField(related_name='attended_rehearsals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]