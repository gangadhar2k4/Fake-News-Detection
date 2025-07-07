from django.shortcuts import redirect,render
# Home page anyone can Access
def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    return render(request,"index/index.html")