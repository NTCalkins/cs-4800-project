# Generated by Django 2.2.11 on 2020-04-14 04:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eaterie', '0002_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='eaterie.Customer')),
                ('total_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('menu_items', models.ManyToManyField(blank=True, to='eaterie.MenuItem')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='order_cancelled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 14, 4, 26, 22, 924168)),
        ),
        migrations.AddField(
            model_name='order',
            name='order_fulfilled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='special_instruction',
            field=models.CharField(blank=True, max_length=512),
        ),
        migrations.CreateModel(
            name='CartEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('cart', models.ForeignKey(null=True, on_delete='CASCADE', to='eaterie.Cart')),
                ('menu_item', models.ForeignKey(null=True, on_delete='CASCADE', to='eaterie.MenuItem')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('menu_item', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='eaterie.MenuItem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eaterie.Order')),
            ],
            options={
                'unique_together': {('order', 'menu_item')},
            },
        ),
    ]