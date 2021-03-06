# Generated by Django 4.0.6 on 2022-07-14 15:21

from django.db import migrations, models
import products.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Item full name', max_length=1000, unique=True)),
                ('cost', models.PositiveIntegerField(help_text='Cost per product in cents', validators=[products.validators.validate_cost])),
                ('amount_available', models.PositiveIntegerField(default=0, help_text='Amount of items (default:0)')),
                ('seller_id', models.CharField(help_text='Seller identifier', max_length=100)),
            ],
        ),
    ]
