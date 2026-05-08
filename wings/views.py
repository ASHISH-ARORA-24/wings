from django.shortcuts import redirect, render


def home(request):
    return render(request, 'home.html')


def google_login_with_role(request, role):
    if role in ('family', 'vendor'):
        request.session['login_role'] = role
    return redirect('/accounts/google/login/')
