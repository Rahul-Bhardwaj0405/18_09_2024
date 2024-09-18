# Generated by Django 5.1.1 on 2024-09-17 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookingData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(choices=[('hdfc', 'HDFC'), ('icici', 'ICICI'), ('karur_vysya', 'Karur Vysya Bank')], max_length=50)),
                ('year', models.IntegerField()),
                ('month', models.CharField(max_length=20)),
                ('sale_total', models.IntegerField()),
                ('date', models.DateField()),
                ('sale_amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='RefundData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
