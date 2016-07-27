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
    return HttpResponseRedirect('/login/')


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
        if (title != '') and (author != '') and (abstract != ''):
            query = Book(title=title, author=author, abstract=abstract)
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
        logid = request.POST['logid']
        log = Log.objects.get(id=logid)
        log.delete()
        return HttpResponseRedirect('/dashboard/')


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


def search(request):
    if request.method == 'POST':
        keyword = request.POST['search']
        books = Book.objects.filter(title__contains=keyword).order_by('title')
        user = request.user
        user.full_name = user.get_full_name()
        logs = Log.objects.filter(user=user)
        return render(request, 'dashboard.html', {'user': user, 'books': books, 'logs': logs})