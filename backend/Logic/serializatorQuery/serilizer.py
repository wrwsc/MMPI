from rest_framework import serializers
from Dal.models import UserAnswer, User


class UserAnswerSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    question_number = serializers.IntegerField(min_value=1, max_value=566)
    answer = serializers.ChoiceField(choices=['Да', 'Нет'])

    def create(self, validated_data):
        user_id = validated_data['user_id']
        question_field = f"Вопрос {validated_data['question_number']}"
        django_user = self.context['request'].user

        try:
            user = User.objects.get(django_user=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError(f"Пользователь с ID {django_user.id} не существует.")

        answer_value = validated_data['answer']

        answer_obj, _ = UserAnswer.objects.get_or_create(user=user)
        
        setattr(answer_obj, question_field, answer_value)
        answer_obj.save()
        
        return answer_obj
