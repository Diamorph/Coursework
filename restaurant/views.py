from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404 ,render_to_response
from .models import Cold_Dishes, First_Courses, Salad, Hot_Appetizers, Order
from django.contrib import auth
from .forms import Restaurants_Form
from mysite import settings
import os , json

# Create your views here.

def rest(request):
    result = "Successful add!"
    if request.method == "POST" and request.POST['name'] and request.POST['weight'] and request.POST['price'] and request.POST['consist'] and request.FILES['image']:
        form = Restaurants_Form(request.POST, request.FILES)
        if form.is_valid():
            upload_file(request.FILES['image'])
        Cold_Dishes.objects.create(name=request.POST['name'],
                             weight=request.POST['weight'],
                             price=request.POST['price'],
                             consist=request.POST['consist'],
                             image=request.FILES['image'])
        return render(request,"main.html", {'result': result, 'user' : request.user})
    else:
        if request.method == "GET":
            return render(request,"add.html", {'dishes': Cold_Dishes.objects.all(), 'user' : request.user})


def upload_file(f):
    with open(os.path.join(settings.MEDIA_ROOT,f.name),'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def cold_dishes(request, Cold_Dishes_id):
    return HttpResponse("You're looking at question %s." % Cold_Dishes_id)

def ColdDishes_id(request,id):
    if request.method == "GET":
        return render(request,"Cold_Dishes.html" , {'dishes': [Cold_Dishes.objects.get(id = int(id))], 'user' : request.user})


def Cold_dishes(request):
    args = {}
    if request.method == 'GET':
        return render(request, "Cold_Dishes.html", {'dishes': Cold_Dishes.objects.all(), 'user': request.user})

def First_courses(request):
    if request.method == 'GET':
        return render(request, "First_courses.html", {'first_course': First_Courses.objects.all(), 'user': request.user})

def Hot_appetizers(request):
    if request.method == 'GET':
        return render(request, "Hot_Appetizers.html", {'hot': Hot_Appetizers.objects.all(), 'user': request.user})


def Salad_view(request):
    args = {}
    if request.method == 'GET':
        return render(request, "Salad.html", {'salad': Salad.objects.all(), 'user': request.user})

def Main_view(request):
    if request.method == 'GET':
        return render(request, "Salad.html", {'salad': Salad.objects.all(), 'user': request.user})
        #return HttpResponse(request , "You're looking at question." ,{})



def hot_view(request):
    return render(request, "Hot_Appetizers.html" , {'hot': Hot_Appetizers.objects.all(), 'user': request.user})

def Menu(request):
    if request.method == 'GET':
        return render(request, "menu.html", {'user': request.user})
        #return render_to_response("menu.html", {'username':auth.get_user(request).username}, args)


def search(request):
    rests = Cold_Dishes.objects.none()
    flag = True
    print(rests)
    if 'search' in request.GET:
        search = request.GET['search'].split()
        print(search)
        for val in search:
            if flag:
                newrests = Cold_Dishes.objects.filter(name__icontains=val)
                print(newrests)
                if newrests:
                    rests = newrests
                else:
                    continue
                flag = False
            else:
                newrests = Cold_Dishes.objects.filter(name__icontains=val)
                if newrests:
                    rests = newrests

    return HttpResponse(json.dumps([i.dict() for i in rests]), content_type="application/javascript")

def DelCold_Dishes(request,id):
    result = "Successful del"
    if request.method == "POST":
        Cold_Dishes.objects.get(id=int(id)).delete()
        return render(request,"main.html", {'result': result, 'user' : request.user})


def Orders(request):
    result = "Ваш заказ прийнятий, найближчим часом з вами звяжеться наш менеджер"
    if request.method == "POST" and request.POST['name'] and request.POST['surname'] and request.POST['phone'] and request.POST['email'] and request.POST['number'] and request.POST['date']:
        Order.objects.create(name=request.POST['name'],
                                   surname=request.POST['surname'],
                                   phone=request.POST['phone'],
                                   email=request.POST['email'],
                                   number=request.POST['number'],
                                   date=request.POST['date'])
        return render(request, "main.html", {'result': result, 'user': request.user})
    else:
        if request.method == "GET":
            return render(request, "order.html", {'orders': Order.objects.all(), 'user': request.user})


def Orders_get(request):
    args = {}
    if request.method == 'GET':
        return render(request, "listOfOrders.html", {'orders': Order.objects.all(), 'user': request.user})

def Contact(request):
    if request.method == 'GET':
        return render(request,"Contacts.html",{'user':request.user})