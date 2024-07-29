from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from .filters import DetectionFilter
from .models import UploadAlert

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user) 
				return redirect('home')
			else:
				messages.info(request, 'Usuario o contraseña incorrectos')
		context = {}
		return render(request, 'detection/login.html', context)
	
def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Cuenta creada con éxito: ' + user)
				return redirect('login')
		context = {'form':form}
		return render(request, 'detection/register.html', context)
	
@login_required(login_url='login')
def home(request):
	token = Token.objects.get(user=request.user)
	uploadAlert = UploadAlert.objects.filter(user_ID=token)

	if 'reporte_del_dia' in request.GET:
		today = timezone.now().date()
		uploadAlert = uploadAlert.filter(date_created__date=today)
	
	myFilter = DetectionFilter(request.GET, queryset=uploadAlert)
	uploadAlert = myFilter.qs
	context = {'myFilter':myFilter, 'uploadAlert':uploadAlert}
	return render(request, 'detection/dashboard.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

def alert(request, pk):
	uploadAlert = UploadAlert.objects.all()
	uploadAlert = UploadAlert.objects.filter(image__iexact=str(pk) + ".jpg")
	myFilter = DetectionFilter(request.GET, queryset=uploadAlert)
	uploadAlert = myFilter.qs
	context = {
		'myFilter': myFilter,
		'uploadAlert': uploadAlert
	}
	return render(request, 'detection/alert.html', context)
