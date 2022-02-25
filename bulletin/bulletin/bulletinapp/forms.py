from django import forms
from datetime import datetime
from .models import User, Post


class LoginForm(forms.Form):
    id = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def login_validate(self):
        user_id = self.cleaned_data['id']
        user_password = self.cleaned_data['password']
        try:
            user = User.objects.get(id=user_id)
            user_b = User.objects.get(password=user_password)
        except Exception:
            return False
        if user == user_b:
            return True
        return False


class JoinForm(forms.Form):
    id = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField()
    email = forms.EmailField()


    def join_validate(self):
        validation_1 = validation_2 = False
        user_id = self.cleaned_data['id']
        pw = self.cleaned_data['password']
        pw_conf = self.cleaned_data['password_confirm']
        name = self.cleaned_data['username']
        user_email = self.cleaned_data['email']

        if pw != pw_conf:
            return "비밀번호와 비밀번호 확인필드가 일치하지 않습니다."
        try:
            user = User.objects.get(id=user_id)
        except Exception:
            validation_1 = True
        try:
            user = User.objects.get(username=name)
        except Exception:
            validation_2 = True

        if validation_1 and validation_2:
            new_user = User.objects.create(
                id=user_id,
                password=pw,
                username=name,
                email=user_email,
                sign_up_date=datetime.now(),
            )
            return "회원가입이 완료되었습니다."
        elif not validation_1:
            return "중복되는 아이디입니다."
        elif not validation_2:
            return "중복되는 사용자 이름입니다."


class CreateForm(forms.Form):
    title = forms.CharField(max_length=50)
    content = forms.CharField(widget=forms.Textarea(attrs={'size': '500'}))

    def create_post(self, post_id, writer_id):
        try:
            new_post = Post.objects.create(
                id=post_id,
                writer=writer_id,
                date=datetime.now(),
                title=self.cleaned_data['title'],
                content=self.cleaned_data['content'],
            )
            new_post.save()
            return True
        except Exception:
            return False


class ChangePasswordForm(forms.Form):
    original_pw = forms.CharField(max_length=20, widget=forms.PasswordInput)
    new_pw = forms.CharField(max_length=20, widget=forms.PasswordInput)
    new_pw_confirm = forms.CharField(max_length=20, widget=forms.PasswordInput)

    def validate_data(self):
        original_pw = self.cleaned_data['original_pw']
        new_pw = self.cleaned_data['new_pw']
        new_pw_confirm = self.cleaned_data['new_pw_confirm']
        try:
            user = User.objects.get(password=original_pw)
        except Exception:
            return False
        if new_pw == new_pw_confirm:
            user.password = new_pw
            user.save()
            return True
        return False

class ChangeNameForm(forms.Form):
    original_name = forms.CharField(max_length=20)
    new_name = forms.CharField(max_length=20)

    def validate_data(self):
        original_name = self.cleaned_data['original_name']
        new_name = self.cleaned_data['new_name']
        try:
            user = User.objects.get(username=original_name)
        except Exception:
            return False
        user.username = new_name
        user.save()
        return True


class ChangeEmailForm(forms.Form):
    original_email = forms.EmailField()
    new_email = forms.EmailField()

    def validate_data(self):
        original_email = self.cleaned_data['original_email']
        new_email = self.cleaned_data['new_email']
        try:
            user = User.objects.get(email=original_email)
        except Exception:
            return False
        user.email = new_email
        user.save()
        return True


class DeleteUserForm(forms.Form):
    id = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User

    @staticmethod
    def delete_validate(user_id, user_pw):
        user1 = user2 = None
        try:
            user1 = User.objects.get(id=user_id)
            user2 = User.objects.get(password=user_pw)
            if user1 != user2:
                return False
        except Exception:
            return False
        post_list = Post.objects.filter(writer_id=user_id)
        post_list.delete()
        user1.delete()
        return True


