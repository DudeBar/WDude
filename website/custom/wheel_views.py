# coding=utf-8
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from website.models import Customer, WheelCustomer

def _customers_can_launch():
    return not WheelCustomer.objects.filter(is_active=True).exists()

@login_required()
def add_customer_wheel(request):
    if request.method == 'POST':
        customer = Customer.objects.get(pk=request.POST['customer_id'])
        WheelCustomer.objects.create(customer=customer)
        return redirect('add_fidelity', customer_id=customer.pk)
    else:
        return redirect('home')

def launch_wheel(request):
    if 'customer_id' in request.session:
        customer = Customer.objects.get(pk=request.session['customer_id'])
        if request.method == 'POST':
            wheel_session = WheelCustomer.objects.get(is_active=True)
            if wheel_session.customer != customer:
                return redirect('customer_account')
            else:
                wheel_session.launch = True
                wheel_session.save()
            return redirect("customer_account")

        elif _customers_can_launch():
            can_launch = _customers_can_launch()

            wheel_session = WheelCustomer.objects.filter(customer=customer)[0]
            wheel_session.is_active = True
            wheel_session.save()

            return render(request, 'launch_wheel.html',
                {
                    'customer': customer,
                    'can_launch': can_launch
                }
            )
        else:
            messages.error(request, "il y à déjà un joueur connecté")
            return redirect("customer_account")
    else:
        return redirect('home')


def wheel_launcher(request):
    if request.is_ajax():
        if WheelCustomer.objects.filter(launch=True).exists():
            wheel_session = WheelCustomer.objects.get(launch=True)
            return HttpResponse(json.dumps({'launch':1,'customer':wheel_session.customer.login}))
        elif WheelCustomer.objects.filter(is_active=True).exists():
            wheel_session = WheelCustomer.objects.get(is_active=True)
            return HttpResponse(json.dumps({'launch':0,'customer':wheel_session.customer.login}))
        else:
            return HttpResponse(json.dumps({'launch':0,'customer':""}))
    else:
        redirect('home')

@login_required()
def wheel_ended(request):
        WheelCustomer.objects.get(launch=True).delete()