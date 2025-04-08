from random import choices

from django.db import models


class User(models.Model):
    SEX_CHOICE= [
        ("Мужской", "Man"),
        ("Женский", "Woman")
    ]
    sex = models.CharField(max_length=7, choices=SEX_CHOICE)
    birth_date = models.DateField()
    email = models.EmailField(blank=True, null=True)


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers", null=True)
    ANSWER_CHOICE = [
        (True, "Да"),
        (False, "Нет")
    ]
    for i in range(1, 567):
        locals()[f"Вопрос {i}"] = models.CharField(max_length=5, choices=ANSWER_CHOICE, null=True)