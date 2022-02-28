from django.core.exceptions import ValidationError
from .models import User
import re


special_1 = re.compile('[`~!@#$%^&*()=+{}|;:<>,.?/]')    # -와 _를 제외한 특수문자 포함/미포함
special_2 = re.compile('[`~!@#$%^&*()_=+{}|;:<>,.?/]')   # 특수문자 포함/미포함
reg_1 = re.compile(r'[a-z]')
reg_2 = re.compile(r'[A-Z]')
reg_3 = re.compile(r'[0-9]')

def validate_id(value):
    if special_1.search(value):
        raise ValidationError("아이디는 -와 _를 제외한 특수문자를 포함할 수 없습니다.")

    if reg_1.search(value) and reg_2.search(value):
        pass
    else:
        raise ValidationError("아이디는 영문 대소문자를 모두 포함해야 합니다.")

    try:
        user = User.objects.get(id=value)
    except User.DoesNotExist:
        return
    raise ValidationError("이미 존재하는 아이디입니다.")

def validate_pw(value):
    if reg_1.search(value) and reg_2.search(value) and reg_3.search(value):
        pass
    else:
        raise ValidationError("비밀번호는 숫자, 영어 소문자, 대문자를 모두 포함해야 합니다.")

    if not special_2.search(value):
        raise ValidationError("비밀번호는 1개 이상의 특수문자를 포함해야 합니다.")

def validate_name(value):
    if special_2.search(value):
        raise ValidationError("사용자 이름은 특수문자를 포함할 수 없습니다.")
    try:
        user = User.objects.get(username=value)
    except User.DoesNotExist:
        return
    raise ValidationError("이미 존재하는 이름입니다.")
