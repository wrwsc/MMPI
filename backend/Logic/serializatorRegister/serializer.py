from rest_framework import serializers
from django.core.exceptions import ValidationError
from Dal.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User as DjangoUser


class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    sex = serializers.ChoiceField(choices=[("Мужской", "Мужской"), ("Женский", "Женский")])
    age = serializers.IntegerField()

    def create(self, validated_data):
        email = validated_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        django_user = DjangoUser.objects.create_user(username=email, email=email)

        sex = validated_data['sex']
        age = validated_data['age']
        dal_user = User.objects.create(
            sex=sex,
            age=age,
            email=email,
            django_user=django_user
        )
        dal_user.django_user = django_user
        dal_user.save()
        token, _ = Token.objects.get_or_create(user=django_user)

        return dal_user, token
