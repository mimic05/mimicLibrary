from django.urls import path # type: ignore
from . import views
from .views import issue_book, return_book

urlpatterns = [

    #for home page
    path('', views.home, name='home'),

    #for admin 
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
 
    #for login
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # for logout
    path('logout/', views.logout_view, name='logout'),

    #for books handling
    path('books/', views.book_list, name='book_list'),
    path('issue/<int:book_id>/', views.issue_book, name='issue_book'),

    path('return/<int:transaction_id>/', views.return_book, name='return_book'),
    path('borrowed/', views.borrowed_books, name='borrowed_books'),

]
