# Generated by Django 4.2.4 on 2023-08-22 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=20, unique=True)),
                ('invite_code', models.CharField(blank=True, max_length=6, null=True, unique=True)),
                ('used_invite_code', models.CharField(blank=True, max_length=20, null=True)),
                ('invited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.user')),
            ],
        ),
    ]
