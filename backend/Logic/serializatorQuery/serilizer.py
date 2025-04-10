from rest_framework import serializers
from Dal.models import UserAnswer, User

class UserAnswerSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False) 
    question_number = serializers.IntegerField(min_value=1, max_value=566)
    answer = serializers.ChoiceField(choices=[('Да', 'Да'), ('Нет', 'Нет')])

    @staticmethod
    def create(validated_data):
        question_field = f"Вопрос {validated_data['question_number']}"
        user_id = validated_data.get('user_id', None)
        
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise serializers.ValidationError(f"Пользователь с ID {user_id} не существует.")
        else:
            user = User.objects.create(
                sex="Unknown",
                birth_date="2000-01-10",
                email="XXXX@XXX" 
            )
        
        answer_value = "Да" if validated_data['answer'] else "Нет"

        answer_obj, _ = UserAnswer.objects.get_or_create(user=user)
        
        setattr(answer_obj, question_field, answer_value)
        answer_obj.save()
        
        return answer_obj
