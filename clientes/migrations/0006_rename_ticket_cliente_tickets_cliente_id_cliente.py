# Generated by Django 5.0.8 on 2024-08-08 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0005_alter_cliente_cpf'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cliente',
            old_name='ticket',
            new_name='tickets',
        ),
        migrations.AddField(
            model_name='cliente',
            name='id_cliente',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
