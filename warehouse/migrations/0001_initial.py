# Generated by Django 2.2.6 on 2019-11-11 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StorageUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='StorageUnitComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='WarehouseComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('storage', models.ManyToManyField(through='warehouse.StorageUnitComponent', to='warehouse.StorageUnit')),
            ],
        ),
        migrations.CreateModel(
            name='WarehouseItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='WarehouseItemComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='warehouse.WarehouseComponent')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='warehouse_components', to='warehouse.WarehouseItem')),
            ],
        ),
        migrations.AddField(
            model_name='warehouseitem',
            name='components',
            field=models.ManyToManyField(through='warehouse.WarehouseItemComponent', to='warehouse.WarehouseComponent'),
        ),
        migrations.AddField(
            model_name='warehouseitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='warehouse_items', to='shop.Product'),
        ),
        migrations.AddField(
            model_name='storageunitcomponent',
            name='component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='storage_units', to='warehouse.WarehouseComponent'),
        ),
        migrations.AddField(
            model_name='storageunitcomponent',
            name='storage_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='components', to='warehouse.StorageUnit'),
        ),
    ]
