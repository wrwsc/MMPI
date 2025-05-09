from random import choices
from django.contrib.auth.models import User as DjangoUser
from django.db import models
from Dal.scaleKeys import SCALE_KEYS


class User(models.Model):
    SEX_CHOICE = [
        ("Мужской", "Man"),
        ("Женский", "Woman")
    ]

    django_user = models.OneToOneField(
        DjangoUser,
        on_delete=models.CASCADE,
        primary_key=True
    )
    user_id = models.PositiveIntegerField(editable=False, unique=True, null=False, default=0)
    sex = models.CharField(max_length=7, choices=SEX_CHOICE)
    age = models.IntegerField(null=True, blank=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"Пользователь {self.django_user.username} ({self.django_user_id})"

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self.django_user_id
        super().save(*args, **kwargs)

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers", null=True)
    ANSWER_CHOICE = [
        (True, "Да"),
        (False, "Нет")
    ]
    for i in range(1, 567):
        locals()[f"Вопрос {i}"] = models.CharField(max_length=5, choices=ANSWER_CHOICE, null=True) # type: ignore


class UserTScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tscore_settings")
    scale = models.CharField(max_length=5)
    M = models.FloatField()
    delta = models.FloatField()
    T = models.FloatField(null=True, blank=True)
    original_T = models.FloatField(null=True, blank=True)
    original_M = models.FloatField(null=True, blank=True)
    original_delta = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'scale')

    def __str__(self):
        return f"{self.user.django_user.username} - {self.scale}"

    def calculate_t(self):
        return 50 + 10 * (self.user_answer - self.M) / self.delta

    @property
    def user_answer(self):
        user_answers = UserAnswer.objects.filter(user=self.user).first()
        if not user_answers:
            return 0

        answers = {f"Вопрос {i}": getattr(user_answers, f"Вопрос {i}") for i in range(1, 567)}
        raw_score = 0

        if self.scale == '5' and self.user.sex == 'Женский':
            keys = SCALE_KEYS.get('5-Ж', {})
        elif self.scale == '5' and self.user.sex == 'Мужской':
            keys = SCALE_KEYS.get('5-М', {})
        else:
            keys = SCALE_KEYS.get(self.scale, {})

        for q in keys.get('Да', []):
            if answers.get(f"Вопрос {q}") == "Да":
                raw_score += 1
        for q in keys.get('Нет', []):
            if answers.get(f"Вопрос {q}") == "Нет":
                raw_score += 1

        return raw_score

    def save(self, *args, **kwargs):
        if self.M and self.delta:
            if self.original_T is None:
                self.original_T = 50 + 10 * (self.user_answer - self.M) / self.delta
            if self.original_M is None:
                self.original_M = self.M
            if self.original_delta is None:
                self.original_delta = self.delta
            self.T = 50 + 10 * (self.user_answer - self.M) / self.delta
        super().save(*args, **kwargs)