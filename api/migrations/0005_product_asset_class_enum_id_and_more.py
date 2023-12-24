# Generated by Django 4.2.8 on 2023-12-22 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_orderheader_approved_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='asset_class_enum_id',
            field=models.CharField(blank=True, default=None, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='asset_type_enum_id',
            field=models.CharField(blank=True, default=None, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_type_enum_id',
            field=models.CharField(blank=True, default=None, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='orderheader',
            name='order_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
