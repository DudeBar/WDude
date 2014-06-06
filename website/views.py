# coding=utf-8
import json

from django.shortcuts import render, redirect
from website.form import CreateCustomerForm, LoginForm, CommandBillingForm
from website.models import Customer, Command, Product


def home(request):
	return render(request, "home.html")

def logout(request):
	if "customer_id" in request.session:
		request.session.flush()
		request.session.clear()
	return redirect("home")

def login(request):
	if "customer_id" not in request.session:
		if request.method == 'POST':
			form = LoginForm(request.POST)
			if form.is_valid():
				customer = Customer.objects.get(login=form.cleaned_data['login'])
				request.session['customer_id'] = customer.pk
				request.session['customer_name'] = customer.login
				return redirect("customer_account")
			return render(request, "login.html", {'form': form})
		else:
			form = LoginForm()
			return render(request, "login.html", {'form': form})
	else:
		return redirect("home")

def customer_create(request):
	if request.method == 'POST':
		form = CreateCustomerForm(request.POST)
		if form.is_valid():
			customer = Customer(login=form.cleaned_data['login'], password=form.cleaned_data['password'])
			customer.save()
			request.session['customer_id'] = customer.pk
			request.session['customer_name'] = customer.login
			return redirect("home")
		return render(request, "customer_create.html", {'form':form})
	else:
		form = CreateCustomerForm()
		return render(request, "customer_create.html", {'form':form})

def customer_account(request):
	if 'customer_id' in request.session:
		customer = Customer.objects.get(pk=request.session['customer_id'])
		return render(request, "customer_account.html", {'customer_name': customer.login})
	else:
		return redirect("home")

def add_command(request):
	if request.method == 'POST':
		form = CommandBillingForm(request.POST)
		if form.is_valid():
			command_list = json.loads(form.cleaned_data['command'])
			total_command = 0
			command = Command(total=total_command)
			command.save()
			for product in command_list:
				total_command += product['price']
				Product.objects.create(
					product_id=product['id'],
					name=product['name'],
					price=product['price'],
					command=command
				)
			command.total = total_command
			command.save()

		else:
			return False
	else:
		form = CommandBillingForm()
		return render(request, "temp_command.html", {'form':form})