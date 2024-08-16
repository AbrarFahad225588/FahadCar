from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserRegisterForm,CommentForm
from . import forms
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import update_session_auth_hash,logout
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Car, Brand,PurchaseHistory
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class UserHomeView(View):
    def get(self, request, brand_slug=None):
        brands = Brand.objects.all()
        cars = Car.objects.all()
        if brand_slug:
            brand = get_object_or_404(Brand, slug=brand_slug)
            cars = cars.filter(brand=brand)
        return render(request, 'home.html', {'brands': brands, 'cars': cars})    



class SignUpView(SuccessMessageMixin, CreateView):
  template_name = 'register.html'
  success_url = reverse_lazy('home')
  form_class = UserRegisterForm
  success_message = "Your profile was created successfully"

class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
    
class UserLoginView(LoginView):
    template_name='login.html'
    # success_url=reverse_lazy('profile')
    def get_success_url(self):
        return reverse_lazy('home')
    def form_valid(self, form):
        messages.success(self.request,'Logged in Successfully')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.success(self.request,'Login information  Incorrect!!')
        return super().form_invalid(form)
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['first_name'] = user.first_name
        context['last_name'] = user.last_name
        context['username'] = user.username
        context['email'] = user.email
        return context
@login_required   
def edit_profile(request):
    if request.method=='POST':
        profile_form=forms.userChangeData(request.POST,instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request,'Profile Updated succesfully')
            return redirect('profile')
    else:
        profile_form=forms.userChangeData(instance=request.user)    
    return render(request,'update_profile.html',{'form':profile_form})
@login_required        
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_pass.html', {'form': form,'type':'Password Change'})     


class CarDetailsView(View):
    def get(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        comments = car.comments.all()
        comment_form = CommentForm()
        return render(request, 'car_detailes.html', {'car': car, 'comments': comments, 'comment_form': comment_form})

    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.car = car
            comment.save()
        return redirect('car_details', pk=car.pk)

@login_required
def buy_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    car.buy(request.user)
    return redirect('purchase_history')

@login_required
def purchase_history(request):
    history = PurchaseHistory.objects.filter(user=request.user)
    return render(request, 'purchase_history.html', {'history': history})    
    