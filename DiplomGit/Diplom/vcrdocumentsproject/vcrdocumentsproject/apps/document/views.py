from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.urls import reverse
from docxtpl import DocxTemplate
import os .path
import datetime

from .models import Contracts, Employees, Executors, Customers, Works, Bills, Acts



def index (request):

    return render(request, 'base.html',)
#Contracts
def contract_list(request):
    return HttpResponseRedirect(reverse('contract:contract_list_filter', kwargs={'filter': 'default'}))

def contract_list_filter(request, filter):
    if filter=='default':
        contract_list = Contracts.objects.order_by('-contract_date')
    elif filter=='actual':
        contract_list = Contracts.objects.filter(payment=False)
    else:
        contract_list = Contracts.objects.filter(contract_number__icontains=filter)
        print(contract_list)


    return render(request, 'document/contract_list.html', {'contract_list' : contract_list})

def contract_list_search(request):
    if request.method == "POST":
        search = request.POST.get("search")
    return HttpResponseRedirect(reverse('contract:contract_list_filter', kwargs={'filter': search}))

def contract_add_form(request):
    c = Customers.objects.all()
    d = Executors.objects.all()
    e = Employees.objects.all()

    customer_l = c
    executor_l = d
    employee_l = e
    nds_const = [0, 18, 20]
    work_type_const = ["Освидетельствование", "Диагностирование", "Экспертиза",
                       "Режимная наладка", "Пусковая наладка", "Обследование", "Прочее"]
    all_data = { "customer_l": customer_l, "executor_l": executor_l,
                "employee_l": employee_l,
                "work_type_const": work_type_const,
                "nds_const": nds_const}
    return render(request, 'document/contract_add_form.html', {'contract_add_form': all_data})
def contract_add(request):
    a = Contracts()

    if request.method == "POST":
        a.contract_number = request.POST.get("contract_number")
        a.description = request.POST.get("description")
        a.contract_date = request.POST.get("contract_date")
        a.contract_end_date = request.POST.get("contract_end_date")
        a.customer = Customers.objects.get(customer_code=request.POST.get("customer"))
        a.executor = Executors.objects.get(executor_code=request.POST.get("executor"))
        a.price = float((request.POST.get("price")).replace(',', '.'))

        a.nds = request.POST.get("nds")
        a.price_with_nds = a.price*(100+float(a.nds))/100
        a.save()




        return HttpResponseRedirect(reverse('contract:contract', args=(a.contract_code,)))
    else:
        return render(request, 'document/contract.html', {'contract': a})
def contract(request, contract_code):
    try:
        try:
            b = Works.objects.filter(contract_number=contract_code)


            works = b

        except:
            works=0

        a = Contracts.objects.get(contract_code = contract_code)
        c = Customers.objects.all()
        d = Executors.objects.all()
        e = Employees.objects.all()
        contract_number =  a.contract_number
        customer = a.customer

        executor = a.executor
        contract_code = a.contract_code

        description = a.description
        contract_date = a.contract_date

        contract_end_date = a.contract_end_date
        payment = a.payment
        price = a.price

        nds = a.nds

        nds_const = [0, 18, 20]
        price_with_nds = a.price_with_nds
        for a in nds_const:
            if a == nds:
                price_with_nds = price*(100+a)/100
        customer_l = c
        executor_l = d
        employee_l = e
        work_type_const =  [ "Освидетельствование","Диагностирование", "Экспертиза",
                             "Режимная наладка" ,"Пусковая наладка", "Обследование", "Прочее" ]

        all_data = {"contract_number": contract_number, "customer": customer, "executor": executor,"contract_code": contract_code,"description": description,
             "contract_date": contract_date, "contract_end_date": contract_end_date,"payment": payment,
             "employee": employee, 'works':works ,
            "customer_l": customer_l,"executor_l": executor_l, "employee_l": employee_l,
                    "work_type_const":work_type_const,"price": price, "nds": nds, "price_with_nds":price_with_nds, "nds_const":nds_const}


    except:

        raise Http404("Договор не найден")
    return  render(request, 'document/contract.html', {'contract': all_data})



def contract_save(request, contract_code):
    try:

        a = Contracts.objects.get(contract_code=contract_code)
        b = Works.objects.filter(contract_number=contract_code)

        if request.method == "POST":

            a.contract_number = request.POST.get("contract_number")
            a.description = request.POST.get("description")
            a.contract_date = request.POST.get("contract_date")
            a.contract_end_date = request.POST.get("contract_end_date")
            a.payment = request.POST.get("payment")
            a.customer = Customers.objects.get(customer_code=request.POST.get("customer"))
            a.executor = Executors.objects.get(executor_code=request.POST.get("executor"))
            a.price = float((request.POST.get("price")).replace(',', '.'))
            a.nds = request.POST.get("nds")
            a.price_with_nds = float((request.POST.get("price_with_nds")).replace(',', '.'))
            a.save()
            #request.POST.getlist("employee")
            count = 0
            for work in request.POST.getlist("description_work"):

                temp = Works.objects.get(work_code=b[count].work_code)
                temp.description = request.POST.getlist("description_work")[count]
                temp.work_start_date = request.POST.getlist("work_start_date")[count]

                temp.work_end_date = request.POST.getlist("work_end_date")[count]
                temp.type_of_work = request.POST.getlist("type_of_work")[count]
                temp.type_of_work = request.POST.getlist("type_of_work")[count]
                temp.work_status = request.POST.getlist("work_status")[count]
                #temp.save() #можно удалить?

                for p in temp.employee_code.all():
                    temp.employee_code.remove(Employees.objects.get(employee_code=p.employee_code))

                for c in request.POST.getlist("employee"+str(temp.work_code)):

                    temp.employee_code.add(Employees.objects.get(employee_code=int(c)))
                temp.save()
                count += 1

            return HttpResponseRedirect(reverse('contract:contract_list'))
        else:
            return HttpResponseRedirect(reverse('contract:contract'))

    except:
        raise Http404("Договор не найден")

def contract_print(request, contract_code):
    contract_code = contract_code
    a = Contracts.objects.get(contract_code = contract_code )
    b = Customers.objects.get(customer_code = a.customer.customer_code )
    c = Executors.objects.get(executor_code = a.executor.executor_code )
    d = Works.objects.filter(contract_number = a)
    dir = os.path.abspath(os.getcwd()+"/vcrdocumentsproject/apps/document/Docx/")
    init = b.fio.split()
    customer_fio_short = init[0]+" "+init[1][0]+"." + " " + init[2][0] + "."
    init = c.fio.split()
    executor_fio_short = init[0] + " " + init[1][0] + "." + " " + init[2][0] + "."
    doc = DocxTemplate(dir+"\contract.docx")

    context = {'contract_number': a.contract_number, 'contract_date':a.contract_date, 'customer':a.customer,
               'customer_fio':b.fio,'executor':a.executor,'executor_fio':c.fio,
               'works':d,
               'price':a.price_with_nds, 'nds':a.nds,'nds_price':a.price_with_nds-a.price,
               'contract_end_date':a.contract_end_date,
               'customer_post_index':b.post_index,'customer_inn':b.inn,
               'customer_kpp':b.kpp,'customer_payment_account':b.payment_account,
               'customer_bik': b.bik, 'customer_correspondent_bill':b.сorrespondent_bill,
               'customer_ogrn':b.ogrn,'customer_address':b.address,
               'executor_post_index': c.post_index, 'executor_inn': c.inn,
               'executor_kpp': c.kpp, 'executor_payment_account': c.payment_account,
               'executor_bik': c.bik, 'executor_correspondent_bill': c.сorrespondent_bill,
               'executor_ogrn': c.ogrn, 'executor_address': c.address,
               'customer_fio_short': customer_fio_short, 'executor_fio_short':executor_fio_short,
               }
    doc.render(context)
    doc.save(dir+"\Договор №  " + a.contract_number.replace('/', '_') + ".docx")
    return HttpResponseRedirect(reverse('contract:contract_list_filter', kwargs={'filter': 'default'}))

#Employees
def employee_add_form(request):

    return render(request, 'document/employee_add_form.html')

def employee_add(request):

        a = Employees()

        if request.method == "POST":

            a.fio = request.POST.get("fio")

            a.save()

            return HttpResponseRedirect(reverse('contract:employee_list', args=(a.employee_code,)))
        else:
            return render(request, 'document/employee.html', {'employee': a})

def employee_list(request):
    employee_list = Employees.objects.all()
    return render(request, 'document/employee_list.html', {'employee_list': employee_list})

def employee(request, employee_code):
    try:
        a = Employees.objects.get( employee_code  = employee_code )
    except:
        raise Http404("Сотрудник не найден")
    return  render(request, 'document/employee.html', {'employee': a})




def employee_save(request, employee_code):
    try:
        a = Employees.objects.get(employee_code=employee_code)


        if request.method == "POST":
            a.fio = request.POST.get("fio")

            a.save()

            return HttpResponseRedirect(reverse('contract:employee_list'))
        else:
            return render(request, 'document/employee.html', {'employee': a})
    except:
        raise Http404("Сотрудник не найден")
#Executors
def executor_add_form(request):

    return render(request, 'document/executor_add_form.html')

def executor_add(request):

        a = Executors()

        if request.method == "POST":
            a.organization_name = request.POST.get("organization_name")
            a.post_index = request.POST.get("post_index")
            a.inn = request.POST.get("inn")
            a.kpp = request.POST.get("kpp")
            a.payment_account = request.POST.get("payment_account")
            a.bik = request.POST.get("bik")
            a.ogrn = request.POST.get("ogrn")
            a.address = request.POST.get("address")
            a.сorrespondent_bill = request.POST.get("сorrespondent_bill")
            a.fio = request.POST.get("fio")

            a.save()

            return HttpResponseRedirect(reverse('contract:executor_list'))
        else:
            return render(request, 'document/executor.html', {'executor': a})

def executor_list(request):
    executor_list = Executors.objects.all()

    return render(request, 'document/executor_list.html', {'executor_list' : executor_list})

def executor(request, executor_code):
    try:
        a = Executors.objects.get( executor_code  = executor_code )
    except:
        raise Http404("Исполнитель не найден")
    return  render(request, 'document/executor.html', {'executor': a})

def executor_save(request, executor_code):
    try:
        a = Executors.objects.get(executor_code=executor_code)
        print(a)

        if request.method == "POST":
            a.organization_name = request.POST.get("organization_name")
            a.post_index = request.POST.get("post_index")
            a.inn = request.POST.get("inn")
            a.kpp = request.POST.get("kpp")
            a.payment_account = request.POST.get("payment_account")
            a.bik = request.POST.get("bik")
            a.ogrn = request.POST.get("ogrn")
            a.address = request.POST.get("address")
            a.сorrespondent_bill = request.POST.get("сorrespondent_bill")
            a.fio = request.POST.get("fio")


            a.save()

            return HttpResponseRedirect(reverse('contract:executor_list'))
        else:
            return render(request, 'document/executor.html', {'executor': a})
    except:
        raise Http404("Заказчик не найден")

#Customers
def customer_add_form(request):

    return render(request, 'document/customer_add_form.html')

def customer_add(request):

        a = Customers()

        if request.method == "POST":
            a.organization_name = request.POST.get("organization_name")
            a.post_index = request.POST.get("post_index")
            a.inn = request.POST.get("inn")
            a.kpp = request.POST.get("kpp")
            a.ogrn = request.POST.get("ogrn")
            a.address = request.POST.get("address")
            a.payment_account = request.POST.get("payment_account")
            a.bik = request.POST.get("bik")
            a.сorrespondent_bill = request.POST.get("сorrespondent_bill")
            a.fio = request.POST.get("fio")

            a.save()

            return HttpResponseRedirect(reverse('contract:customer_list'))
        else:
            return render(request, 'document/customer.html', {'customer': a})

def customer_list(request):
    customer_list = Customers.objects.all()

    return render(request, 'document/customer_list.html', {'customer_list' : customer_list})

def customer(request, customer_code):
    try:
        a = Customers.objects.get( customer_code  = customer_code )
    except:
        raise Http404("Заказчик не найден")
    return  render(request, 'document/customer.html', {'customer': a})

def customer_save(request, customer_code):
    try:
        a = Customers.objects.get(customer_code=customer_code)
        if request.method == "POST":
            a.organization_name = request.POST.get("organization_name")
            a.post_index = request.POST.get("post_index")
            a.inn = request.POST.get("inn")
            a.kpp = request.POST.get("kpp")
            a.ogrn = request.POST.get("ogrn")
            a.address = request.POST.get("address")
            a.payment_account = request.POST.get("payment_account")
            a.bik = request.POST.get("bik")
            a.сorrespondent_bill = request.POST.get("сorrespondent_bill")
            a.fio = request.POST.get("fio")


            a.save()

            return HttpResponseRedirect(reverse('contract:customer_list'))
        else:
            return render(request, 'document/customer.html', {'customer': a})
    except:
        raise Http404("Заказчик не найден")

    #works


def work_list_main(request):

    return HttpResponseRedirect(reverse('contract:work_list_filter', kwargs={'filter': 'default'}))


def work_add_form(request):
    contracts = Contracts.objects.all()
    employees = Employees.objects.all()
    work_add_form = {'contracts': contracts,'employees':employees}
    return render(request, 'document/work_add_form.html', {'work_add_form': work_add_form})

def work_add(request):
    a = Works()

    if request.method == "POST":
        a.contract_number = Contracts.objects.get(contract_code=request.POST.get("contract_code"))

        a.type_of_work = request.POST.get("type_of_work")
        a.description = request.POST.get("description")
        a.work_start_date = request.POST.get("work_start_date")
        a.work_end_date = request.POST.get("work_end_date")
        a.save()

        for c in request.POST.getlist("employee"):

            a.employee_code.add(Employees.objects.get(employee_code=int(c)))
            print(a.employee_code)


        a.save()
    return HttpResponseRedirect(reverse('contract:work_list_main',))

def work(request, work_code):
    try:
        a = Works.objects.get( work_code  = work_code )
        contracts = Contracts.objects.all()
        employees = Employees.objects.all()
        work_type_const = ["Освидетельствование", "Диагностирование", "Экспертиза",
                           "Режимная наладка", "Пусковая наладка", "Обследование", "Прочее"]
        work = {'contracts': contracts, 'employees': employees, 'works': a, 'work_type_const':work_type_const}

    except:
        raise Http404("Работа не найдена")
    return  render(request, 'document/work.html', {'work': work})

def work_save(request, work_code):
    try:

        a = Works.objects.get(work_code=work_code)

        if request.method == "POST":
            a.type_of_work = request.POST.get("type_of_work")

            a.contract_number = Contracts.objects.get(contract_code=request.POST.get("contract_code"))
            a.description = request.POST.get("description")
            a.work_start_date = request.POST.get("work_start_date")
            a.work_end_date = request.POST.get("work_end_date")
            a.work_status = request.POST.get("work_status")

            a.save()


            for p in a.employee_code.all():
                a.employee_code.remove(Employees.objects.get(employee_code=p.employee_code))

            for c in request.POST.getlist("employee"):
                a.employee_code.add(Employees.objects.get(employee_code=int(c)))


            a.save()

            return HttpResponseRedirect(reverse('contract:work_list_main'))
        else:
            return render(request, 'document/work.html', {'work': a})
    except:
        raise Http404("Работа не найдена")


def work_list_save_default(request, work_code):
    try:
        print(work_code)
        a = Works.objects.get(work_code=work_code)
        b = Contracts.objects.get(contract_code=a.contract_number.contract_code)
        if request.method == "POST":

            work_status=request.POST.get("work_status")
            payment = request.POST.get("payment")
            if (work_status == 'on'):
                a.work_status = True
            else:
                a.work_status = False
            if (payment == 'on'):
                b.payment = True
            else:
                b.payment = False
            a.save()
            b.save()

            return HttpResponseRedirect(reverse('contract:work_list_filter', kwargs={'filter': 'default'}))
        else:
            return render(request, 'document/work.html', {'work': a})
    except:
        raise Http404("Ошибка")

def work_list_save_actual(request, work_code):
    try:
        print(work_code)
        a = Works.objects.get(work_code=work_code)
        b = Contracts.objects.get(contract_code=a.contract_number.contract_code)
        if request.method == "POST":

            work_status=request.POST.get("work_status")
            payment = request.POST.get("payment")
            if (work_status == 'on'):
                a.work_status = True
            else:
                a.work_status = False
            if (payment == 'on'):
                b.payment = True
            else:
                b.payment = False
            a.save()
            b.save()

            return HttpResponseRedirect(reverse('contract:work_list_filter', kwargs={'filter': 'actual'}))
        else:
            return render(request, 'document/work.html', {'work': a})
    except:
        raise Http404("Ошибка")


def work_list_save_payment(request, work_code):
    try:
        print(work_code)
        a = Works.objects.get(work_code=work_code)
        b = Contracts.objects.get(contract_code=a.contract_number.contract_code)
        if request.method == "POST":

            work_status=request.POST.get("work_status")
            payment = request.POST.get("payment")
            if (work_status == 'on'):
                a.work_status = True
            else:
                a.work_status = False
            if (payment == 'on'):
                b.payment = True
            else:
                b.payment = False
            a.save()
            b.save()

            return HttpResponseRedirect(reverse('contract:work_list_filter', kwargs={'filter': 'payment'}))
        else:
            return render(request, 'document/work.html', {'work': a})
    except:
        raise Http404("Ошибка")

def work_list_filter(request, filter):
    try:
        if filter == 'default':
            works = Works.objects.all()
        elif filter == 'actual':

            works = Works.objects.filter(work_start_date__lte=datetime.date.today(), work_status=False)
        elif filter == 'payment':

            works = Works.objects.filter(contract_number__payment=False )

        else:
            works = Works.objects.filter(description__icontains=filter)
            print(contract_list)

        works1 = {'works':works, "filter":filter}

        return render(request, 'document/work_list_main.html', {'works': works1})
    except:
        raise Http404("Ошибка")




def work_list_search(request):
    if request.method == "POST":
        search = request.POST.get("search")
    return HttpResponseRedirect(reverse('contract:work_list_filter', kwargs={'filter': search}))

#Bills
def bill_add_form(request,filter):
    if filter == 'default':
        contracts = Contracts.objects.all()
        contracts = {'contract_list': contracts, 'filter':filter}
    else:
        filter = Contracts.objects.get(contract_code=filter)
        contracts = {'filter':filter}
    return render(request, 'document/bill_add_form.html', {'contracts': contracts})

def bill_add(request, filter):

        a = Bills()

        if request.method == "POST":
            a.bill_number = request.POST.get("bill_number")
            if filter == 'default':
                a.contract_number = Contracts.objects.get(contract_code=request.POST.get("contract_number"))
            else:
                a.contract_number = Contracts.objects.get(contract_code=filter)
            a.bill_date = request.POST.get("bill_date")
            a.save()

            return HttpResponseRedirect(reverse('contract:bill_list', kwargs={'filter': a.contract_number.contract_code}))
        else:
            return render(request, 'document/bill.html', {'bill': a})

def bill_list(request, filter):
    if filter == 'default':
        bills = Bills.objects.all()
        bill_list = {'bills':bills, 'filter':filter}
    else:
        bills = Bills.objects.filter(contract_number=filter)

        bill_list = {'bills': bills, 'filter': filter}

    return render(request, 'document/bill_list.html', {'bill_list': bill_list})

def bill(request, bill_code):
    try:
        a = Bills.objects.get( bill_code = bill_code )
        contracts = Contracts.objects.all()

        bills = {'bill': a, 'contracts': contracts}
    except:
        raise Http404("Ошибка")
    return  render(request, 'document/bill.html', {'bills': bills})

def bill_save(request, bill_code):
    try:
        a = Bills.objects.get(bill_code=bill_code)
        if request.method == "POST":
            a.bill_number = request.POST.get("bill_number")
            a.contract_number = Contracts.objects.get(contract_code=request.POST.get("contract_number"))
            a.bill_date = request.POST.get("bill_date")
            a.payment = request.POST.get("payment")

            a.save()

            return HttpResponseRedirect(reverse('contract:bill_list', kwargs={'filter': a.contract_number.contract_code}))
        else:
            return render(request, 'document/bill.html', {'bill': a})
    except:
        raise Http404("Ошибка")

#Acts
def act_add_form(request,filter):
    if filter == 'default':
        contracts = Contracts.objects.all()
        contracts = {'contract_list': contracts, 'filter':filter}
    else:
        filter = Contracts.objects.get(contract_code=filter)
        contracts = {'filter':filter}
    return render(request, 'document/act_add_form.html', {'contracts': contracts})

def act_add(request, filter):

        a = Acts()

        if request.method == "POST":
            a.act_number = request.POST.get("act_number")
            if filter == 'default':
                a.contract_number = Contracts.objects.get(contract_code=request.POST.get("contract_number"))
            else:
                a.contract_number = Contracts.objects.get(contract_code=filter)
            a.act_date = request.POST.get("act_date")
            a.save()

            return HttpResponseRedirect(reverse('contract:act_list', kwargs={'filter': a.contract_number.contract_code}))
        else:
            return render(request, 'document/act.html', {'act': a})

def act_list(request, filter):
    if filter == 'default':
        acts = Acts.objects.all()
        act_list = {'acts':acts, 'filter':filter}
    else:
        acts = Acts.objects.filter(contract_number=filter)

        act_list = {'acts': acts, 'filter': filter}

    return render(request, 'document/act_list.html', {'act_list': act_list})

def act(request, act_code):
    try:
        a = Acts.objects.get( act_code = act_code )
        contracts = Contracts.objects.all()

        acts = {'act': a, 'contracts': contracts}
    except:
        raise Http404("Ошибка")
    return  render(request, 'document/act.html', {'acts': acts})

def act_save(request, act_code):
    try:
        a = Acts.objects.get(act_code=act_code)
        if request.method == "POST":
            a.act = request.POST.get("act_number")
            a.contract_number = Contracts.objects.get(contract_code=request.POST.get("contract_number"))
            a.act_date = request.POST.get("act_date")

            a.save()

            return HttpResponseRedirect(reverse('contract:act_list', kwargs={'filter': a.contract_number.contract_code}))
        else:
            return render(request, 'document/act.html', {'act': a})
    except:
        raise Http404("Ошибка")
