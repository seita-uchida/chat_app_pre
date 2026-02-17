from django.contrib import auth 
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, LoginForm
from .models import User, Talk

def index(request):
    return render(request, 'main/index.html')

def signup(request):
    if request.method == "GET":
        form = SignUpForm()
    elif request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            # モデルフォームは form の値を models にそのまま格納できる
            # save() メソッドがあるので便利
            form.save()

            # フォームから username と password を読み取る
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            # 認証情報のセットを検証するには authenticate() を利用します。
            # このメソッドは認証情報をキーワード引数として受け取ります。
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)

            return redirect("index")

    context = {"form": form}
    return render(request, "main/signup.html", context)

class LoginView(auth_views.LoginView):
    authentication_form = LoginForm  # ログイン用のフォームを指定
    template_name = "main/login.html"  # テンプレートを指定

@login_required
def friends(request):
    # 自分以外のユーザーを取得
    friends = User.objects.exclude(id=request.user.id)
    print(friends)
    context = {"friends": friends}
    return render(request, "main/friends.html", context)


@login_required
def settings(request):
    return render(request, "main/settings.html")

@login_required
def talk_room(request, friend_id):
    # get_object_or_404 は、第一引数にモデル名、その後任意の数のキーワードを受け取り、
    # もし合致するデータが存在するならそのデータを、存在しないなら 404 エラーを発生させます。
    friend = get_object_or_404(User, id=friend_id)

    # 自分が送信者で上の friend が受信者であるデータ、または friend が送信者で friend が受信者であるデータをすべて取得します。
    talks = Talk.objects.filter(
        Q(sender=request.user, receiver=friend)
        | Q(sender=friend, receiver=request.user)
    ).order_by("time")

    context = {
        "friend": friend,
        "talks": talks,
    }
    return render(request, "main/talk_room.html", context)