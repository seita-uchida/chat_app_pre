from django.contrib import auth 
from django.shortcuts import render, redirect

from .forms import SignUpForm

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

            # 検証する対象はデフォルトでは username と password であり、
            # その組み合わせを個々の認証バックエンドに対して問い合わせ、
            # 認証バックエンドで認証情報が有効とされれば User オブジェクトを返します。
            # もしいずれの認証バックエンドでも認証情報が有効と判定されなければ
            # PermissionDenied エラーが送出され、None が返されます。
            # つまり、autenticate メソッドは"username"と"password"を受け取り、
            # その組み合わせが存在すればその User を返し、不正であれば None を返します。
            if user:
                # あるユーザーをログインさせる場合は、login() を利用します。
                # この関数は HttpRequest オブジェクトと User オブジェクトを受け取ります。
                # ここでの User は認証バックエンド属性を持ってる必要があり、
                # authenticate() が返す User は user.backend（認証バックエンド属性）を持つので連携可能。
                auth.login(request, user)

            return redirect("index")

    context = {"form": form}
    return render(request, "main/signup.html", context)

def login(request):
    return render(request, 'main/login.html')