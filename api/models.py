from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.postgres.indexes import GinIndex, OpClass
from django.db import models
from django.db.models.functions import Upper

import api.config as config


class UserManager(BaseUserManager):
    def create_user(self, name: str, password: str) -> 'UserEntity':
        user = self.model(name=name)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name: str, password: str | None = ...) -> 'UserEntity':
        user = self.create_user(
            name=name,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserEntity(AbstractBaseUser):
    name = models.CharField(max_length=config.USER_NAME_LENGTH, unique=True)
    outcoming_invites = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='incoming_invites'
    )
    friends = models.ManyToManyField('self', symmetrical=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        indexes = [
            GinIndex(
                OpClass(Upper('name'), name='gin_trgm_ops'),
                name='user_name_gin_idx'
            ),
            models.Index(fields=('name',))
        ]
