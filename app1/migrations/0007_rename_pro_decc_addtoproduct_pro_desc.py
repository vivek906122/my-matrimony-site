# Generated by Django 5.1.1 on 2024-09-20 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_addtoproduct_pro_decc'),
    ]

    operations = [
        migrations.RenameField(
            model_name='addtoproduct',
            old_name='pro_decc',
            new_name='pro_desc',
        ),
    ]
