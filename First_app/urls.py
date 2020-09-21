from django.urls import path
from . import views

# SET THE NAMESPACE!
app_name = 'First_app'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    path('register/',views.registered,name='registered'),
    path('user_login/',views.user_login,name='user_login'),
    
]
