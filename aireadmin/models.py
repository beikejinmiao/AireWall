from django.db import models
from conf.env import TABLE_PREFIX


class User(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    username = models.CharField(max_length=150, unique=True, db_index=True, verbose_name="用户账号",
                                help_text="用户账号")
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=40, verbose_name="姓名", help_text="姓名")
    GENDER_CHOICES = (
        (0, "未知"),
        (1, "男"),
        (2, "女"),
    )
    gender = models.IntegerField(
        choices=GENDER_CHOICES, default=0, verbose_name="性别", null=True, blank=True, help_text="性别"
    )
    USER_TYPE = (
        (0, "系统用户"),
        (1, "个人用户"),
        (2, "企业用户"),
    )
    user_type = models.IntegerField(
        choices=USER_TYPE, default=1, verbose_name="用户类型", null=True, blank=True, help_text="用户类型"
    )
    email = models.EmailField(max_length=255, verbose_name="邮箱", null=True, blank=True, help_text="邮箱")
    mobile = models.CharField(max_length=255, verbose_name="电话", null=True, blank=True, help_text="电话")

    status = models.IntegerField(default=1)
    create_time = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="创建时间", help_text="创建时间"
    )

    def __str__(self):
        return self.username

    class Meta:
        db_table = TABLE_PREFIX + "system_users"
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]


class APIKey(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    username = models.CharField(
        max_length=150, unique=True, db_index=True, verbose_name="用户账号", help_text="用户账号"
    )
    apikey = models.CharField(
        max_length=127, unique=True, db_index=True, verbose_name="APIKey", help_text="APIKey"
    )
    num_usable = models.IntegerField(
        default=100, verbose_name="剩余可调用次数", help_text="剩余可调用次数"
    )
    num_day_usable = models.IntegerField(
        default=100, verbose_name="今日可调用次数", help_text="今日可调用次数"
    )
    create_time = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="创建时间", help_text="创建时间"
    )
    invoke_time = models.DateTimeField(
        auto_now_add=True, verbose_name="最近调用时间", help_text="最近调用时间"
    )

    def __str__(self):
        return self.apikey

    class Meta:
        db_table = TABLE_PREFIX + "system_apikey"
        verbose_name = "APIKey"
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]

