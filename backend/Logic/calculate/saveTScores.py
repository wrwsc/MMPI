from Dal.models import UserTScore
from Dal.tables.table import M_table, delta_table
from django.db import transaction


def save_user_t_scores(user, t_scores, raw_scores, original_t_value=None):
    with transaction.atomic():
        for scale, t in t_scores.items():
            try:
                M_value = M_table[user.sex][scale]
                delta_value = delta_table[user.sex][scale]

                tscore_obj, created = UserTScore.objects.update_or_create(
                    user=user,
                    scale=scale,
                    defaults={
                        'M': M_value,
                        'delta': delta_value,
                        'T': float(t)
                    }
                )

                if created:
                    if original_t_value is not None:
                        tscore_obj.original_T = original_t_value
                    else:
                        user_raw_score = raw_scores.get(scale, 0)
                        tscore_obj.original_T = 50 + 10 * (user_raw_score - M_value) / delta_value

                if tscore_obj.original_M is None:
                    tscore_obj.original_M = M_value
                if tscore_obj.original_delta is None:
                    tscore_obj.original_delta = delta_value

                tscore_obj.save()

            except KeyError:
                print(f"Ошибка: отсутствуют значения для шкалы {scale} в таблицах для {user.sex} пола.")
