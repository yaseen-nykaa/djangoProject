# Generated by Django 3.2.4 on 2021-06-30 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='qty',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]
