from django.shortcuts import render # type: ignore
from .models import Book
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Book, Transaction
from datetime import date, timedelta
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, Book


# To display book

def book_list(request):
    books = Book.objects.filter(is_available=True)
    return render(request, 'library/book_list.html', {'books': books})

# To issue
@login_required
def issue_book(request, book_id):
    #if not request.user.is_staff:  # Check if user is admin
        #return redirect('home')
    if not request.user.is_authenticated:  # Check if user is authenticated
        return redirect('login')  # Redirect to login page if not logged in

    book = get_object_or_404(Book, id=book_id)
    
    book = get_object_or_404(Book, id=book_id)
    books = Book.objects.filter(is_available=True)
    
    if request.method == 'POST':
        issued_by = request.POST.get('issued_by')
        issue_date = date.today()
        return_date = issue_date + timedelta(days=15)

        Transaction.objects.create(
            book=book,
            issued_by=issued_by,
            issue_date=issue_date,
            return_date=return_date,
            fine_paid=False
        )

        book.is_available = False
        book.save()

        return HttpResponseRedirect(reverse('book_list'))

    return render(request, 'library/issue_book.html', {'book': book, 'books': books})

# for sign up 

# Sign up view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in user after signup
            return redirect('home')  # Redirect to home after signup
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Get username from POST data
        password = request.POST.get('password')  # Get password from POST data
        user = authenticate(request, username=username, password=password)  # Authenticate user
        if user is not None:
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to homepage after login
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})  # Return error message
    return render(request, 'registration/login.html')


#logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home after logout

#admin view
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')  # Restrict to admin users only
    books = Book.objects.all()
    return render(request, 'library/admin_dashboard.html', {'books': books})

# home page 
def home(request):
    books = Book.objects.filter(is_available=True)
    return render(request, 'library/home.html', {'books': books})

"""""
# return book 
@login_required
def return_book(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    if request.method == 'POST':
        book = transaction.book
        book.is_available = True
        book.save()

        if transaction.return_date < date.today():
            days_overdue = (date.today() - transaction.return_date).days
            fine_amount = days_overdue  
            transaction.fine_paid = fine_amount  
        
        transaction.delete()  
        return redirect('book_list')  

    return render(request, 'library/return_book.html', {'transaction': transaction})
"""

@login_required
def issued_books_view(request):
    transactions = Transaction.objects.filter(issued_by=request.user.username)  # Adjust as necessary
    today_date = date.today()
    
    return render(request, 'library/your_template.html', {
        'transactions': transactions,
        'today_date': today_date,
    })

@login_required
def borrowed_books(request):
    transactions = Transaction.objects.filter(issued_by=request.user.username)
    return render(request, 'library/borrowed_books.html', {'transactions': transactions})

@login_required
def return_book(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, issued_by=request.user.username)

    if request.method == 'POST':
        book = transaction.book
        book.is_available = True
        book.save()

        if transaction.return_date < date.today():
            days_overdue = (date.today() - transaction.return_date).days
            fine_amount = days_overdue
            transaction.fine_paid = fine_amount

        transaction.delete()
        return redirect('borrowed_books')

    return render(request, 'library/return_book.html', {'transaction': transaction})
