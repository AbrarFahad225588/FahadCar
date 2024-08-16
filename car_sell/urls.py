from django.urls import path
from . import views
from django.contrib.auth.views import LoginView 
urlpatterns = [
    path('register/',views.SignUpView.as_view(),name='register'),
    path('login/',views.UserLoginView.as_view() ,name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('profile/edit/',views.edit_profile,name='edit_profile'),
    path('changePass/',views.change_password,name='change_password'),
    path('', views.UserHomeView.as_view(), name='home'),
    path('brand/<slug:brand_slug>/', views.UserHomeView.as_view(), name='brand'),
    path('car/<int:pk>/',views.CarDetailsView.as_view(), name='car_details'),
     path('buy/<int:car_id>/', views.buy_car, name='buy_car'),
    path('history/', views.purchase_history, name='purchase_history'),
    
]
