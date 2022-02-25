from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.views import View
from rest_framework import viewsets
from rest_framework import permissions

from .models import *
from .forms import *
from .serializers import *

post_number = len(Post.objects.all()) + 1


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class LoginView(View):
    form_class = LoginForm
    template_name = 'bulletinapp/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            if form.login_validate():
                request.session['id'] = form.cleaned_data['id']
                return redirect('/')
        return render(request, self.template_name,
                      {'form': self.form_class(), 'msg': "아이디나 비밀번호가 잘못되었습니다. 다시 입력해 주세요."})


class JoinView(View):
    form_class = JoinForm
    template_name = 'bulletinapp/join.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        msg = ""
        form = self.form_class(request.POST)
        if form.is_valid():
            msg = form.join_validate()
            return render(request, self.template_name, {'form': form, 'msg': msg})
        return render(request, self.template_name, {'form': self.form_class(), 'msg': "입력값이 유효하지 않습니다."})


class MainView(View):
    main_template = 'bulletinapp/main.html'
    welcome_template = 'bulletinapp/welcome.html'

    def get(self, request):
        if login_state(request):
            user = User.objects.get(id=request.session.get('id'))
            post_list = Post.objects.all()
            return render(request, self.main_template, {'user': user, 'post_list': post_list})
        return render(request, self.welcome_template)


class MyPageView(View):
    template_name = 'bulletinapp/my_page.html'

    def get(self, request):
        user = get_object_or_404(User, pk=request.session.get('id'))
        return render(request, self.template_name, {'user': user})


class MyContentView(View):
    template_name = 'bulletinapp/my_post.html'

    def get(self, request):
        user_id = request.session.get('id')
        user = get_object_or_404(User, pk=user_id)
        post_list = Post.objects.filter(writer_id=user_id)
        return render(request, self.template_name, {'user': user, 'post_list': post_list})


class ChangeInfoView(View):
    template_name = 'bulletinapp/change_info.html'
    pw_class = ChangePasswordForm
    name_class = ChangeNameForm
    email_class = ChangeEmailForm

    def get(self, request, data):
        user = get_object_or_404(User, pk=request.session.get('id'))
        if data == 'password':
            form = self.pw_class()
        elif data == 'username':
            form = self.name_class()
        elif data == 'email':
            form = self.email_class()
        else:
            raise Http404('잘못된 주소입니다. 다시 시도해 주세요.')
        return render(request, self.template_name, {'user': user, 'form': form})

    def post(self, request, data):
        user = get_object_or_404(User, pk=request.session.get('id'))
        if data == 'password':
            form = self.pw_class(request.POST)
            empty_form = self.pw_class()
        elif data == 'username':
            form = self.name_class(request.POST)
            empty_form = self.name_class()
        elif data == 'email':
            form = self.email_class(request.POST)
            empty_form = self.email_class()
        else:
            raise Http404('잘못된 입력입니다. 다시 입력해 주세요.')

        if form.is_valid():
            if form.validate_data():
                return render(request, self.template_name, {'user': user, 'ok_msg': "성공적으로 변경되었습니다."})
        return render(request, self.template_name,
                      {'user': user, 'form': empty_form, 'no_msg': "입력이 잘못되었습니다. 다시 입력해 주세요."})


class CreateView(View):
    form_class = CreateForm
    template_name = 'bulletinapp/create.html'

    def get(self, request):
        form = self.form_class()
        user_id = request.session.get('id')
        user = get_object_or_404(User, pk=user_id)
        return render(request, self.template_name, {'user': user, 'form': form})

    def post(self, request):
        user_id = request.session.get('id')
        user = get_object_or_404(User, pk=user_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            if form.create_post(post_number, user):
                return render(request, self.template_name, {'user': user, 'form': form, 'ok_msg': "게시물이 저장되었습니다."})
        return render(request, self.template_name,
                      {'user': user, 'form': self.form_class(), 'no_msg': "게시물 저장이 되지 않았습니다. 다시 작성해 주세요."})


class ContentView(View):
    template_name = 'bulletinapp/post_content.html'

    def get(self, request, post_id):
        user_id = request.session.get('id')
        user = get_object_or_404(User, pk=user_id)
        post = get_object_or_404(Post, pk=post_id)
        return render(request, self.template_name, {'user': user, 'post': post})


# backend logic

# 로그인 된 상태인지 확인
def login_state(request):
    try:
        user_id = request.session.get('id')
    except Exception:
        return False
    if user_id is None:
        return False
    return True


# 세션에서 저장된 정보 외 유저의 다른 정보 불러옴
def session_info(request):
    user_data = {}
    user_id = request.session.get('id')
    if user_id:
        user = get_object_or_404(User, pk=user_id)
        user_data['pw'] = user.password
        user_data['username'] = user.username
        user_data['email'] = user.email
    return user_data


# mixin 배우고나면 url에 할당하지 않고 mixin 기능으로 해당 페이지에서 처리할 예정 1
def logout(request):
    if request.session.get('id'):
        del (request.session['id'])
    return redirect('/')


# mixin 배우고나면 url에 할당하지 않고 mixin 기능으로 해당 페이지에서 처리할 예정 2
def account_withdrawal(request):
    if request.method == 'GET':
        form = DeleteUserForm()
        return render(request, 'bulletinapp/withdrawal.html', {'form': form})
    elif request.method == 'POST':
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['id']
            user_pw = form.cleaned_data['password']
            if form.delete_validate(user_id, user_pw):
                return render(request, 'bulletinapp/withdrawal.html', {'msg_ok': "회원 탈퇴가 완료되었습니다."})
        return render(request, 'bulletinapp/withdrawal.html', {'msg_no': "잘못된 정보를 입력하였습니다."})
