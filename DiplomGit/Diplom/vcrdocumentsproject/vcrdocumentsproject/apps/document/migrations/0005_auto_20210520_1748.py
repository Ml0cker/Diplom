# Generated by Django 3.1.7 on 2021-05-20 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0004_auto_20210520_0837'),
    ]

    operations = [
        migrations.AddField(
            model_name='contracts',
            name='nds',
            field=models.IntegerField(default=20, verbose_name='НДС'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contracts',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1000, max_digits=20, verbose_name='Сумма'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contracts',
            name='price_with_nds',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=20, verbose_name='Сумма с НДС'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customers',
            name='hide',
            field=models.BooleanField(default=False, null=True, verbose_name='Скрыть заказчика'),
        ),
        migrations.AddField(
            model_name='estimates',
            name='hide',
            field=models.BooleanField(default=False, null=True, verbose_name='Скрыть исполнителя'),
        ),
        migrations.AddField(
            model_name='executors',
            name='hide',
            field=models.BooleanField(default=False, null=True, verbose_name='Скрыть исполнителя'),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='payment',
            field=models.BooleanField(default=False, null=True, verbose_name='Оплата по договору'),
        ),
    ]