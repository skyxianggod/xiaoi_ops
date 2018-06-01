from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
# Create your views here.


@login_required(login_url="login.html")
def index(request):

    return  render(request,'index/index.html',)


def login_view(request):
    error_msg = "请登录"
    error_msg1 = "用户名密码错误，或被禁用"

    if request.method == "GET":
        return render(request,'index/login.html',{'error_msg': error_msg, })

    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request,username=u,password=p)
        if user is not None:
            if user.is_active:
                login(request,user)
                request.session['is_login'] = True
                return redirect('index.html')
        else:
            return render(request, 'index/login.html',
                          {'error_msg': error_msg1, })


def logout_view(request):
    request.session.clear()
    return redirect('/login.html')
