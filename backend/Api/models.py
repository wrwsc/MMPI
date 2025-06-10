from django.contrib import admin
import base64

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, path
from django.utils.html import format_html
from Dal.models import User, UserTScore
from Dal.utils.load_questions import load_questions
from Logic.calculate.scoring import generate_graph
from Dal.models import UserAnswer
from simple_history.models import HistoricalRecords

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user',)

    search_fields = ('user__email',)

    readonly_fields = ['user'] + [f"question_with_answer_{i}" for i in range(1, 567)]

    @staticmethod
    def question_with_answer(obj, i):
        sex = getattr(obj.user, 'sex', 'Мужской')
        questions = load_questions(sex)
        question_text = questions[i - 1] if i <= len(questions) else "—"
        answer = getattr(obj, f"Вопрос {i}")
        return f"Вопрос {i} ({question_text}): {answer if answer is not None else '-'}"

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


class UserTScoreInline(admin.TabularInline):
    model = UserTScore
    extra = 0
    fields = ('scale', 'M', 'delta', 'T', 'original_T', 'formula_display', 'restore_button')
    readonly_fields = ('scale', 'T', 'original_T', 'formula_display', 'restore_button')
    can_delete = False
    history = HistoricalRecords()

    def has_add_permission(self, request, obj=None):
        return False

    def formula_display(self, obj):
        if obj.M and obj.delta:
            formula = f"T = 50 + 10 * ({obj.user_answer} - {obj.M}) / {obj.delta}"
            return format_html(f"<b>{formula}</b> = {obj.T}")
        return "Недостаточно данных"
    formula_display.short_description = "Формула и результат"

    def restore_button(self, obj):
        if obj.original_T is not None:
            url = reverse('admin:restore_tscore', args=[obj.id])
            return format_html(
                '<a class="button" style="padding:2px 6px; background:#5cb85c; color:white;" '
                'href="{}" onclick="return confirm(\'Установить T = original_T?\')">Сбросить изменения</a>',
                url
            )
        return "-"
    restore_button.short_description = 'Сбросить изменения'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [UserTScoreInline]
    readonly_fields = ('t_score_graph',)
    list_display = ('django_user', 'email', 'age', 'get_sex_display', 'user_id')

    def get_sex_display(self, obj):
        mapping = {
            "Мужской": "Мужской",
            "Женский": "Женский"
        }
        return mapping.get(obj.sex, obj.sex)

    get_sex_display.short_description = 'Пол'

    def t_score_graph(self, obj):
        try:
            scores = UserTScore.objects.filter(user=obj)
            t_scores = {}

            for s in scores:
                if s.T is not None:
                    t_scores[s.scale] = round(s.T)

            if not t_scores:
                return format_html("<p style='color:red;'>Нет сохранённых T-баллов</p>")

            graph_file = generate_graph(t_scores)
            encoded = base64.b64encode(graph_file.getvalue()).decode('utf-8')
            html = f'<img src="data:image/png;base64,{encoded}" style="max-width:100%; height:auto;" />'
            return format_html(html)

        except Exception as e:
            return format_html(f"<p style='color:red;'>Ошибка: {str(e)}</p>")

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                'restore_tscore/<int:tscore_id>/',
                self.admin_site.admin_view(self.restore_tscore),
                name='restore_tscore'
            ),
        ]
        return custom + urls

    def restore_tscore(self, request, tscore_id):
        tscore = get_object_or_404(UserTScore, pk=tscore_id)

        if tscore.original_T is not None:
            tscore.T = tscore.original_T
            tscore.M = tscore.original_M
            tscore.delta = tscore.original_delta
            tscore.save(update_fields=['T', 'M', 'delta'])
            tscore.save()

            self.message_user(request, f"T для шкалы {tscore.scale} обновлён до original_T = {tscore.T}")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('admin:index')))