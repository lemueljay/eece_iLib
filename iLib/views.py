from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from iLib.models import *

# Create your views here.


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'GET':
        message = None
        return render(request, 'login.html', {'message': message})
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/dashboard/')
        else:
            message = "Sorry. Your username and password did not match."
            return render(request, 'login.html', {'message': message})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password = request.POST['password']
        user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, password=password)
        user.is_staff = False
        user.save()
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        return HttpResponseRedirect('/dashboard/')


def dashboard(request):
    if request.user.is_authenticated():
        user = request.user
        user.full_name = user.get_full_name()
        books = Book.objects.all().order_by('title')
        logs = Log.objects.filter(user=user)
        return render(request, 'dashboard.html', {'user': user, 'books': books, 'logs': logs})
    else:
        return HttpResponseRedirect('/login/')


def addbooks(request):
    if request.method == 'GET':
        user = request.user
        if user.is_staff:
            message = None
            return render(request, 'addbooks.html', {'message': message})
        else:
            return HttpResponseRedirect('/dashboard/')
    elif request.method == 'POST':
        title = request.POST['title'].strip(' \t\n\r')
        author = request.POST['author'].strip(' \t\n\r')
        abstract = request.POST['abstract'].strip(' \t\n\r')
        datepub = request.POST['datepublished']
        if (title != '') and (author != '') and (abstract != ''):
            query = Book(title=title, author=author, abstract=abstract, date_published=datepub)
            query.save()
            message = {'status': True, 'message': 'Book successfully added!'}
            return render(request, 'addbooks.html', {'message': message})
        else:
            message = {'status': False, 'message': 'There was an error in your information!'}
            return render(request, 'addbooks.html', {'message': message})


def editbook(request):
    if request.method == 'GET':
        bookid = request.GET['bookid']
        book = Book.objects.get(id=bookid)
        message = None
        return render(request, 'editbook.html', {'message': message, 'book': book})
    elif request.method == 'POST':
        bookid = request.POST['bookid']
        book = Book.objects.get(id=bookid)
        title = request.POST['title'].strip(' \t\n\r')
        author = request.POST['author'].strip(' \t\n\r')
        abstract = request.POST['abstract'].strip(' \t\n\r')
        if (title != '') and (author != '') and (abstract != ''):
            book.title = title
            book.author = author
            book.abstract = abstract
            book.save()
            return HttpResponseRedirect('/dashboard/')
        else:
            message = {'status': False, 'message': 'There was an error in updating!'}
            return render(request, 'editbook.html', {'message': message, 'book': book})


def deletebook(request):
    if request.method == 'POST':
        bookid = request.POST['bookid']
        book = Book.objects.get(id=bookid)
        book.delete()
        return HttpResponseRedirect('/dashboard/')


def borrow(request):
    if request.method == 'POST':
        bookid = request.POST['bookid']
        book = Book.objects.get(id=bookid)
        book.stat = False
        book.save()
        user = request.user
        query = Log(user=user, book=book)
        query.save()
        return HttpResponseRedirect('/dashboard/')


def cancel(request):
    if request.method == 'POST':
        bookid = request.POST['bookid']
        book = Book.objects.get(id=bookid)
        book.stat = True
        book.save()
        log = Log.objects.get(book=book)
        log.delete()
        return HttpResponseRedirect('/logs/')


def accept(request):
    if request.method == 'POST':
        bookid = request.POST['bookid']
        book = Book.objects.get(id=bookid)
        book.reads += 1
        book.save()
        logid = request.POST['logid']
        log = Log.objects.get(id=logid)
        log.request_status = False
        log.return_status = True
        log.save()
        return HttpResponseRedirect('/logs/')


def returned(request):
    if request.method == 'POST':
        bookid = request.POST['bookid']
        book = Book.objects.get(id=bookid)
        book.stat = True
        book.save()
        logid = request.POST['logid']
        log = Log.objects.get(id=logid)
        log.delete()
        return HttpResponseRedirect('/logs/')


def logs(request):
    logs = Log.objects.all()
    for x in logs:
        x.full_name = x.user.get_full_name()
    return render(request, 'logs.html', {'logs': logs})


class Account(View):
    def get(self, request):
        user = request.user
        message = ""
        return render(request, 'account.html', {"user": user, "message": message})

    def post(self, request):
        id = request.POST['id']
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        user = User.objects.get(id=id)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        user = request.user
        message = "Changes successfully saved!"
        return render(request, 'account.html', {"user": user, "message": message})


def account_password(request):
    if request.method == 'POST':
        oldp = request.POST['oldp']
        newp = request.POST['newp']
        conp = request.POST['conp']
        user = request.user
        wews = True
        message = "LEMUEL GWAPO"
        pusher = auth.authenticate(username=user.username, password=oldp)
        if pusher is not None:
            if newp == conp:
                user.set_password(newp)
                user.save()
                message = "GWAPO KO! WOOOOH! PASSWORD SET!"
                return render(request, 'account-password.html', {'message': message, 'wews': wews})
            else:
                message = "Password did not match!"
                return render(request, 'account-password.html', {'message': message, 'wews': wews})
        else:
            message = "Password did not match!"
            return render(request, 'account-password.html', {'message': message, 'wews': wews})

    else:
        wews = False
        message = "LEMUEL GWAPO!"
        return render(request, 'account-password.html', {'message': message, 'wews': wews})


def about(request):
    if request.user.is_authenticated():
        auth = True
    else:
        auth = False
    return render(request, 'about-us.html', {"auth": auth})


def search(request):
    if request.method == 'POST':
        keyword = request.POST['search']
        books = Book.objects.filter(title__contains=keyword).order_by('title')
        user = request.user
        user.full_name = user.get_full_name()
        logs = Log.objects.filter(user=user)
        return render(request, 'dashboard.html', {'user': user, 'books': books, 'logs': logs})