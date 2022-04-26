import datetime
from django.db import models

from django.utils import timezone


class Executors(models.Model):

    executor_code = models.AutoField('Код исполнителя', primary_key=True)
    organization_name = models.CharField('Название организации', max_length = 250)
    post_index = models.CharField('Почтовый индекс', max_length = 6)
    inn = models.CharField('ИНН', max_length=10)
    kpp = models.CharField('КПП', max_length=9)
    address = models.CharField('Адрес', max_length=100)
    payment_account = models.CharField('Рассчетный счёт', max_length=20)
    bik = models.CharField('БИК', max_length=9, blank=True)
    сorrespondent_bill = models.CharField('Корреспондентский счёт', max_length=20, blank=True)
    ogrn = models.CharField('ОГРН', max_length=13, blank=True)
    fio = models.CharField('Фамилия, имя и отчество', max_length=100, blank=True)
    hide = models.BooleanField('Скрыть исполнителя', default=False,  null=True)
    def __str__(self):
        return self.organization_name

    class Meta:
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"

class Customers(models.Model):

    customer_code = models.AutoField('Код заказчика', primary_key=True)
    organization_name = models.CharField('Название организации', max_length = 250)
    post_index = models.CharField('Почтовый индекс', max_length = 6)
    inn = models.CharField('ИНН', max_length=10)
    kpp = models.CharField('КПП', max_length=9)
    address = models.CharField('Адрес', max_length=100)
    payment_account = models.CharField('Рассчетный счёт', max_length=20)
    bik = models.CharField('БИК', max_length=9, blank=True)
    сorrespondent_bill = models.CharField('Корреспондентский счёт', max_length=20, blank=True)
    ogrn = models.CharField('ОГРН', max_length=13, blank=True)
    fio = models.CharField('Фамилия, имя и отчество', max_length=100, blank=True)
    hide = models.BooleanField('Скрыть заказчика', default=False, null=True)

    def __str__(self):
        return self.organization_name


    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"


class Contracts(models.Model):
    contract_code = models.AutoField('Код договора', primary_key=True)
    contract_number = models.CharField('Номер договора', max_length = 20)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    executor = models.ForeignKey(Executors, on_delete=models.CASCADE)
    description = models.TextField('Наименование')
    contract_date = models.DateField('Дата договора')
    contract_end_date = models.DateField('Дата окончания договора', null=True)
    price = models.DecimalField('Сумма',max_digits= 20, decimal_places=2)
    nds = models.IntegerField('НДС')
    price_with_nds = models.DecimalField('Сумма с НДС',max_digits= 20, decimal_places=2)
    payment = models.BooleanField('Оплата по договору', default=False, null=True)


    def __str__(self):
        return self.contract_number

    def was_pub(self):
        return self.date >= (timezone.now() - datetime.timedelta(days = 7))

    class Meta:
        verbose_name = "Договор"
        verbose_name_plural = "Договоры"


class Employees(models.Model):

    employee_code = models.AutoField('Код сотрудника', primary_key=True)
    fio = models.CharField('Фамилия, имя и отчество', max_length = 100)
    hide = models.BooleanField('Скрыть сотрудника', default=False, null=True)

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class Works(models.Model):

    work_code = models.AutoField('Код работы', primary_key=True)
    type_of_work = models.CharField('Вид работы', max_length = 250, null=True)
    contract_number = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    employee_code = models.ManyToManyField(Employees)
    description = models.TextField('Наименование', null=True)
    work_start_date = models.DateField('Дата начала работы', null=True)
    work_end_date = models.DateField('Дата завершения работы', null=True)
    work_status = models.BooleanField('Статус выполнения работы', default=False, null=True)

    def __str__(self):
        return self.type_of_work

    class Meta:
        verbose_name = "Работа"
        verbose_name_plural = "Работы"


class Estimates(models.Model):

    estimate_code = models.AutoField('Код сметы', primary_key=True)
    estimates_number = models.CharField('Номер сметы', max_length = 20)
    contract_number = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    def __int__(self):
        return self.estimate_code

    class Meta:
        verbose_name = "Смета"
        verbose_name_plural = "Сметы"

class Bills(models.Model):

    bill_code = models.AutoField('Код счета', primary_key=True)
    contract_number=models.ForeignKey(Contracts, on_delete=models.CASCADE)
    bill_number = models.CharField('Номер счета', max_length = 5)
    bill_date = models.DateField('Дата счета')
    payment = models.BooleanField('Оплата по счету', null=True)

    def __str__(self):
        return self.bill_number

    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Счета"

class Acts(models.Model):

    act_code = models.AutoField('Код акта', primary_key=True)
    contract_number = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    act_number = models.CharField('Номер акта', max_length = 5)
    act_date = models.DateField('Дата акта')

    def __int__(self):
        return self.act_number

    class Meta:
        verbose_name = "Акт"
        verbose_name_plural = "Акты"