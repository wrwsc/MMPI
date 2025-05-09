from Dal.models import User, UserAnswer
import random

def fill_random_answers(user_id):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return

    user_answer = UserAnswer.objects.filter(user=user).first()
    if not user_answer:
        user_answer = UserAnswer.objects.create(user=user)

    for i in range(1, 567):
        random_answer = random.choice(["Да", "Нет"])
        setattr(user_answer, f"Вопрос {i}", random_answer)

    user_answer.save()
    print(f"Ответы для пользователя {user_id} успешно заполнены.")
