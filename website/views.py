# coding=utf-8
from datetime import datetime
import json
import urllib2
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from website.custom.wheel_views import _customers_can_launch
from website.form import CreateCustomerForm, LoginForm, BillingForm
from website.models import Customer, Command, Product, ProductQuantity, FbAppAccount, WheelCustomer, Commerces, \
    MusicTrack, MusicTrackAlreadyRegistered


def home(request):
    return render(request, "home.html", {"nav_id":"home"})

def actu(request):
    articles = []

    try:
        fb_access = FbAppAccount.objects.get(pk=1)
        access_token = urllib2.urlopen("""https://graph.facebook.com/oauth/access_token?client_id=%s&client_secret=%s&grant_type=client_credentials"""%(fb_access.client_id, fb_access.client_secret)).read()
        fb_posts = urllib2.urlopen("""https://graph.facebook.com/dudebar.fr/posts?%s"""%access_token).read()
        table_post = json.loads(fb_posts)

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
    except ObjectDoesNotExist:
        pass

    return render(request, "actu.html",{"articles":articles, "nav_id":"actu"})


def logout(request):
    if "customer_id" in request.session:
        #request.session.flush()
        #request.session.clear()
        del request.session['customer_id']
        del request.session['customer_name']
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
        WheelCustomer.objects.filter(customer=customer).update(is_active=False)
        command_list = Command.objects.filter(customer=customer).order_by("-date")
        quantity_total = customer.quantity_litre
        nb_bade = customer.bade
        can_launch = False
        if customer.nb_wheel > 0 and _customers_can_launch():
            can_launch = True
        return render(request, "customer_account.html",
                      {
                          'customer_name': customer.login,
                          'customer_url': request.build_absolute_uri(reverse("add_fidelity", args=(customer.pk,))),
                          'command_list': command_list,
                          'quantity_total': quantity_total,
                          'nb_bade': nb_bade,
                          'due_bade': customer.due_bade,
                          'nav_id':'customer',
                          'can_launch': can_launch
                      }
        )
    else:
        return redirect("home")

def customer_ajax_info(request):
    if 'customer_id' in request.session:
        if request.is_ajax():
            customer = Customer.objects.get(pk=request.session['customer_id'])
            can_launch = 0
            if customer.nb_wheel > 0 and _customers_can_launch():
                can_launch = 1
            customer_info = {
                'id':customer.pk,
                'litre': round(customer.quantity_litre,2),
                'due_bade': customer.due_bade,
                'bade': customer.bade,
                'can_launch':can_launch
            }
            return HttpResponse(json.dumps(customer_info))
    else:
        return HttpResponse(json.dumps(["authentication required"]))

@csrf_exempt
def add_command(request):
    def add_commands(command_list):
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

    return use_billing_data(request, add_commands)


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
        'customer_name':customer.login,
        'quantity_litre':customer.quantity_litre,
        'wheel_fortune': customer.nb_wheel
    })

@login_required()
def bade_fidelity(request):
    if request.method == 'POST':
        customer = Customer.objects.get(pk=request.POST['customer_id'])
        customer.bade += 1
        customer.save()
    return redirect('add_fidelity', customer_id=customer.pk)

@login_required()
def barman_account(request):
    customers = sorted(Customer.objects.all(), key=lambda t: t.quantity_litre, reverse=True)
    return render(request, "barman_account.html",{
        "customers": customers
    })

@login_required()
def customer_detail(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    commands = Command.objects.filter(customer=customer).order_by("-id")
    return render(request, "customer_detail.html", {
        "customer": customer,
        "commands": commands
    })

def get_day_litre(request):
    if request.is_ajax():
        today = datetime.today()
        quantity = Product.objects.filter(command__date__year=today.year,command__date__month=today.month,command__date__day=today.day).aggregate(quantity=Sum('quantity__quantity'))
        return HttpResponse(json.dumps({"litre":quantity['quantity']}))
    else:
        return redirect('home')

def get_day_customer(request):
    if request.is_ajax():
        best_customers = []
        customers = sorted(Customer.objects.all(), key=lambda t: t.quantity_day_litre, reverse=True)
        if not WheelCustomer.objects.filter(customer__pk=9, is_active=True).exists():
            for customer in customers[:3]:
                if customer.quantity_day_litre > 0:
                    best_customers.append(customer.login)
                else:
                    best_customers.append("")
        else:
            best_customers = ["manz", "manz", "manz"]
        return HttpResponse(json.dumps({"customer":[best_customers[0],best_customers[1],best_customers[2]]}))
    else:
        return redirect('home')

@login_required()
def wheel(request):
    return render(request, "wheel.html")


def quartier(request):
    commerces = Commerces.objects.all().order_by('ordre')
    return render(request, "quartier.html", {
        'commerces': commerces,
        'nav_id': "Beaux Arts"
    })


def redirect_quartier(request):
    return redirect('quartier')


def use_billing_data(request, callback):
    form = BillingForm(request.POST or {})

    if request.method == 'POST':
        if form.is_valid():
            data = json.loads(form.cleaned_data['data'])
            callback(data)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
    else:
        form = BillingForm()
        return render(request, "temp_command.html", {'form': form})

@csrf_exempt
def add_music_track(request):
    def put_music_track(data):
        try:
            track = MusicTrack.from_sonos_json(data)
            track.save()

            tracks = MusicTrack.objects.all().order_by('pk')[:21]
            if len(tracks) == 21:
                tracks[0].delete()
        except MusicTrackAlreadyRegistered:
            pass

    return use_billing_data(request, put_music_track)


def get_last_music_track(request):
    track = MusicTrack.objects.all().order_by('-pk').first()
    return render(request, "current_track.html", {'track': track})


def get_registered_tracks(request):
    tracks = MusicTrack.objects.all().order_by('-pk')
    return render(request, "current_tracks.html", {'tracks': tracks})
