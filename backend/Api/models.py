from django.contrib import admin
from Dal.models import UserAnswer

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user',)

    search_fields = ('user__email',)

    readonly_fields = ['user'] + [f"question_with_answer_{i}" for i in range(1, 567)]

    @staticmethod
    def question_with_answer(obj, i):
        question = f"Вопрос {i}"
        answer = getattr(obj, question)
        return f"{question}: {answer if answer is not None else "-"}"

    @staticmethod
    def get_readonly_fields(request, obj=None):
        return ['user'] + [f"question_with_answer_{i}" for i in range(1, 567)]

    @staticmethod
    def get_fieldsets(request, obj=None):
        fields = [f"question_with_answer_{i}" for i in range(1, 567)]
        return [(None, {'fields': ['user']}), ('Ответы на вопросы', {'fields': fields})]

    for i in range(1, 567):
        exec(f"""
def question_with_answer_{i}(self, obj):
    return self.question_with_answer(obj, {i})
question_with_answer_{i}.short_description = "{i}"
        """)
