from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages



# Create your views here.

#def home(request):
#    return render(request, 'app/index.html')
def about(request):
    return render(request, 'app/about.html')
def help(request):
    if request.user.is_authenticated:
        return render(request, 'app/homehelp.html')
    else:
        return render(request, 'app/indexhelp.html')
def contact(request):
    if request.user.is_authenticated:
        return render(request, 'app/homecontact.html')
    else:
        return render(request, 'app/indexcontact.html')


def home(request):
    if request.user.is_authenticated:
        return render(request, 'app/home.html')
    else:
        return render(request, 'app/index.html')
    
def myprofile(request):
    return render(request, 'app/myprofile.html')

def aboutus(request):
    return render(request, 'app/aboutus.html')


@login_required(login_url='signin')
def findbus(request):
    context = {}
    if request.method == 'POST':
        source_r = request.POST.get('source')
        dest_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        bus_list = Bus.objects.filter(source=source_r, dest=dest_r, date=date_r)
        if bus_list:
            return render(request, 'app/list.html', locals())
        else:
            messages.error(request,"Sorry no buses availiable")
            return render(request, 'app/home.html', context)
    else:
        return render(request, 'app/home.html')
    
@login_required(login_url='signin')    
def booking(request,id):
    d=Bus.objects.get(id=id)
    return render(request,'app/booking.html',{'u':d})

@login_required(login_url='signin')
def booked(request,id):
    context = {}
    if request.method == 'POST':
        #id_r = request.POST.get('bus_id')
        passenger = request.POST.get('passenger')
        seats_r = int(request.POST.get('no_seats'))
        bus = Bus.objects.get(id=id)
        if bus:
            if bus.rem > int(seats_r):
                name_r = bus.bus_name
                cost_r = int(seats_r) * bus.price
                source_r = bus.source
                dest_r = bus.dest
                nos_r = Decimal(bus.nos)
                price_r = bus.price
                date_r = bus.date
                time_r = bus.time
                username_r = request.user.username
                email_r = request.user.email
                userid_r = request.user.id
                rem_r = bus.rem - seats_r
                Bus.objects.filter(id=id).update(rem=rem_r)
                book = Book.objects.create(name=passenger, email=email_r, userid=userid_r,bus_name=name_r,
                                           source=source_r, busid=id,
                                           dest=dest_r, price=price_r,cost=cost_r, nos=seats_r, date=date_r, time=time_r,
                                           status='BOOKED')
                print('------------book id-----------', book.id)
                #book.save()
                return render(request, 'app/booked.html', locals())
                
            else:
                messages.error(request,"Sorry Select Fewer Number of Seats")
                d=Bus.objects.get(id=id)
                return render(request,'app/booking.html',{'u':d})
               #return render(request, 'app/booking.html', context)

    else:
        return render(request, 'app/home.html')
    
    
@login_required(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        #seats_r = int(request.POST.get('no_seats'))

        try:
            book = Book.objects.get(id=id_r)
            bus = Bus.objects.get(id=book.busid)
            rem_r = bus.rem + book.nos
            Bus.objects.filter(id=book.busid).update(rem=rem_r)
            #nos_r = book.nos - seats_r
            Book.objects.filter(id=id_r).update(status='CANCELLED')
            Book.objects.filter(id=id_r).update(nos=0)
            messages.success(request," Your Ticket Has Been Cancel")
            return redirect(seebookings)
        
        except Book.DoesNotExist:
            messages.error(request,"Sorry You have not booked that bus")
            return render(request, 'app/error.html', context)
    else:
        return render(request, 'app/home.html')

@login_required(login_url='signin')    
def seebookings(request,new={}):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(userid=id_r)
    if book_list:
        return render(request, 'app/booklist.html', locals())
    else:
        messages.error(request,"Sorry no buses booked")
        return render(request, 'app/home.html', context)
    
def signup(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        password_r = request.POST.get('password')
        user = User.objects.create_user(name_r, email_r, password_r, )
        if user:
            login(request, user)
            return render(request, 'app/thank.html')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'app/index.html', context)
    else:
        return render(request, 'app/index.html', context)


def signin(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user = authenticate(request, username=name_r, password=password_r)
        if user:
            login(request, user)
            # username = request.session['username']
            context["user"] = name_r
            context["id"] = request.user.id
            return render(request, 'app/success.html', context)
            # return HttpResponseRedirect('success')
        else:
            messages.error(request,"Please Enter Correct ID/Password")
            return render(request, 'app/index.html', context)
    else:
        messages.error(request,"You are not logged in")
        return render(request, 'app/index.html', context)


def signout(request):
    context = {}
    logout(request)
    messages.error(request,"You Log Out")
    return render(request, 'app/index.html', context)


def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'app/success.html', context)

@login_required(login_url='signin') 
def cancel(request,id):
    d=Book.objects.get(id=id)
    return render(request,'app/cancel.html',{'c':d})

@login_required(login_url='signin')    
def detail(request,id):
    d=Book.objects.get(id=id)
    return render(request,'app/detail.html',{'l':d})
