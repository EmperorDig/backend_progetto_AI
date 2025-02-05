# Generated by Django 5.1.5 on 2025-02-05 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_baseuser_is_staff_alter_baseuser_is_superuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='birth_date',
            field=models.DateField(null=True, verbose_name='data di nascita'),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='nome'),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='cognome'),
        ),
        migrations.AlterField(
            model_name='patientuser',
            name='disease_type',
            field=models.CharField(choices=[('visiva', 'Visiva'), ('uditiva', 'Uditiva'), ('tattile', 'Tattile')], max_length=20, null=True, verbose_name='tipo di malattia'),
        ),
    ]
