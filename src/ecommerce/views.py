# authentication. Note: "login" is a function; therefore, we use login_page as our url request instead of login
from django.contrib.auth import authenticate, login, get_user_model

from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import ContactForm, LoginForm, RegisterForm

def home_page(request):
	context = {
		"title":"Hello World!",
		"content":"Welcome to the homepage",
	}
	# shows premium content if user is logged in
	if request.user.is_authenticated():
		context["premium_content"] = "YEAHHHHHH"
	return render(request, "home_page.html", context)


def about_page(request):
	context = {
		"title":"about_page",
		"content": "Welcome to the about page"
	}
	return render(request, "home_page.html", context)

def contact_page(request):
	contact_form = ContactForm(request.POST or None)
	context = {
		"title":"Contact_page",
		"content": "Welcome to the contact page",
		"form": contact_form
		# "brand": "new Brand Name"
	}
	if contact_form.is_valid():
		print(contact_form.cleaned_data)
	# if request.method == "POST":
	# 	print(request.POST)
	# 	print(request.POST.get('fullname'))
	# 	print(request.POST['fullname'])
		
	return render(request, "contact/view.html", context)



def login_page(request):
	# form is equal to instance: LoginForm
	form = LoginForm(request.POST or None)
	context = {
		"form": form
	}

	print("User logged in")
	# built in to Django so don't have to worry about this necessarily (prints true/false)
	# print(request.user.is_authenticated())

	if form.is_valid():
		# prints out clean data from username/pw field
		print(form.cleaned_data)
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		# handles authentication for us. Makes sure username/pw are real and sets it to user, to login.
		user = authenticate(request, username=username, password=password)
		print(user)
		print(request.user.is_authenticated())
		if user is not None:
			print(request.user.is_authenticated())
			login(request, user)
			# redirect to a success page
			context['form'] = LoginForm() # new instance that clears out form
			return redirect("/")
		else:
			# return an 'invalid login' error message
			print("Error")
	return render(request, "auth/login.html", context)



User = get_user_model()
def register_page(request):
	form = RegisterForm(request.POST or None)
	context = {
		"form": form
	}
	if form.is_valid():
		print(form.cleaned_data)
		username = form.cleaned_data.get("username")
		email = form.cleaned_data.get('email')
		password = form.cleaned_data.get("password")
		new_user = User.objects.create_user(username, email, password)
		print(new_user)
	return render(request, "auth/register.html", context)

# def home_page_old(request):
# 	return HttpResponse("<h1>Hello World</h1>") 