# coding=utf-8
from datetime import datetime
import json
import urllib2
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Count

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from website.form import CreateCustomerForm, LoginForm, CommandBillingForm
from website.models import Customer, Command, Product, ProductQuantity, FbAppAccount


def home(request):
    return render(request, "home.html", {"nav_id":"home"})

def actu(request):
    fb_access = FbAppAccount.objects.get(pk=1)
    access_token = urllib2.urlopen("""https://graph.facebook.com/oauth/access_token?client_id=%s&client_secret=%s&grant_type=client_credentials"""%(fb_access.client_id, fb_access.client_secret)).read()
    fb_posts = urllib2.urlopen("""https://graph.facebook.com/dudebar.fr/posts?%s"""%access_token).read()
    table_post = json.loads(fb_posts)
    articles = []
    for post in table_post["data"][:10]:
        message=None
        link=None
        picture=None
        if post["type"]=="status" or post["type"]=="photo":
            if "message" in post:
                message=post["message"]
            if "link" in post:
                link=post["link"]
            if 'picture' in post:
                picture=post["picture"]
            if message or picture:
                articles.append({
                    "message":message,
                    "link":link,
                    "date":datetime.strptime(post["created_time"][:10], "%Y-%m-%d"),
                    "picture":picture
                })

    return render(request, "actu.html",{"articles":articles, "nav_id":"actu"})


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
            messages.success(request, "Votre compte a bien été créé")
            return redirect("customer_account")
        return render(request, "customer_create.html", {'form': form, 'nav_id':'customer'})
    else:
        form = CreateCustomerForm()
        return render(request, "customer_create.html", {'form': form, 'nav_id':'customer'})


def customer_account(request):
    if 'customer_id' in request.session:
        customer = Customer.objects.get(pk=request.session['customer_id'])
        command_list = Command.objects.filter(customer=customer).order_by("-date")
        quantity_total = customer.quantity_litre
        nb_bade = customer.bade
        return render(request, "customer_account.html",
                      {
                          'customer_name': customer.login,
                          'customer_url': request.build_absolute_uri(reverse("add_fidelity", args=(customer.pk,))),
                          'command_list': command_list,
                          'quantity_total': quantity_total,
                          'nb_bade': nb_bade,
                          'due_bade': customer.due_bade,
                          'nav_id':'customer'
                      }
        )
    else:
        return redirect("home")

@csrf_exempt
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
                quantity = ProductQuantity.objects.get(type=product["type"])
                Product.objects.create(
                    product_id=product['id'],
                    name=product['name'],
                    price=product['price'],
                    quantity=quantity,
                    command=command
                )
            command.total = total_command
            command.save()

        else:
            return False
    else:
        form = CommandBillingForm()
        return render(request, "temp_command.html", {'form': form})


@login_required()
def new_fidelity(request):
    if request.method == 'POST':
        command = Command.objects.get(pk=request.POST['command_id'])
        customer = Customer.objects.get(pk=request.POST['customer_id'])
        command.customer = customer
        command.save()
        return redirect('add_fidelity', customer_id=customer.pk)
    else:
        redirect('home')

@login_required()
def add_fidelity(request, customer_id):
    command_list = Command.objects.filter(customer=None).order_by('-id')[:10]
    customer = Customer.objects.get(pk=customer_id)
    customer_products = Product.objects.filter(command__customer=customer).values("name").annotate(count=Count("product_id")).order_by("-count")[:5]
    return render(request, 'add_fidelity.html', {
        'command_list': command_list,
        'customer_id': customer_id,
        'due_bade': customer.due_bade,
        'customer_products': customer_products,
        'customer_name':customer.login
    })

@login_required()
def bade_fidelity(request):
    if request.method == 'POST':
        customer = Customer.objects.get(pk=request.POST['customer_id'])
        customer.bade += 1
        customer.save()
    return redirect('add_fidelity', customer_id=customer.pk)
