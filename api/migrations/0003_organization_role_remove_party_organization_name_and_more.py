# Generated by Django 4.2.8 on 2023-12-22 03:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_party_organization_name_party_owner_party_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('organization_name', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_type_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='party',
            name='organization_name',
        ),
        migrations.RemoveField(
            model_name='party',
            name='role_type_id',
        ),
        migrations.AddField(
            model_name='party',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.organization'),
        ),
        migrations.AddField(
            model_name='party',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.role'),
        ),
    ]
