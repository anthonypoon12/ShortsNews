# Generated by Django 5.0.1 on 2024-01-28 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Headline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_one', models.CharField(max_length=200)),
                ('link_two', models.CharField(max_length=200)),
                ('link_three', models.CharField(max_length=200)),
                ('link_four', models.CharField(max_length=200)),
                ('link_five', models.CharField(max_length=200)),
            ],
        ),
    ]