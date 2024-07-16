from enum import unique

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from enumfields import Enum, EnumField

from common.models import TimeRecordingMixin


@unique
class MemberState(Enum):
    ACTIVE = "ACTIVE"  # 활성화
    INACTIVE = "INACTIVE"  # 비활성화
    WITHDRAWN = "WITHDRAWN"  # 탈퇴회원


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email or not password:
            raise ValueError("이메일 또는 비밀번호가 유효하지 않습니다.")

        if User.objects.filter(email=email).exists():
            raise ValueError("중복되는 이메일입니다.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeRecordingMixin):
    email = models.EmailField(unique=True, verbose_name='email')
    nickname = models.CharField(max_length=50, unique=True, verbose_name='nickname')
    status = EnumField(MemberState, default=MemberState.ACTIVE, verbose_name='status', max_length=20)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.email

