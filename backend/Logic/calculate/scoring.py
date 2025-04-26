from Dal.models import UserAnswer
from Dal.scaleKeys import SCALE_KEYS
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import JsonResponse, HttpResponse
from reportlab.lib.utils import ImageReader


def has_completed_all_questions(user):
    user_answers = UserAnswer.objects.filter(user=user).first()
    if not user_answers:
        return False

    for i in range(1, 567):
        answer = getattr(user_answers, f"Вопрос {i}")
        if answer not in ("Да", "Нет"):
            return False

    return True


def calculate_raw_scores(user):
    user_answers = UserAnswer.objects.filter(user=user).first()
    if not user_answers:
        raise ValueError("Ответы пользователя не найдены.")

    answers = {f"Вопрос {i}": getattr(user_answers, f"Вопрос {i}") for i in range(1, 567)}
    raw_scores = {}

    for scale, keys in SCALE_KEYS.items():
        if scale == '5-М' and user.sex == 'Женский':
            continue
        if scale == '5-Ж' and user.sex == 'Мужской':
            continue

        score = 0
        for q in keys.get('Да', []):
            if answers.get(f"Вопрос {q}") == 'Да':
                score += 1
        for q in keys.get('Нет', []):
            if answers.get(f"Вопрос {q}") == 'Нет':
                score += 1

        raw_scores[scale.replace('5-М', '5').replace('5-Ж', '5')] = score

    return raw_scores


def apply_corrections(raw_scores):
    k = raw_scores.get('K', 0)
    corrected_scores = raw_scores.copy()

    corrected_scores['1'] = raw_scores.get('1', 0) + round(0.5 * k)
    corrected_scores['4'] = raw_scores.get('4', 0) + round(0.4 * k)
    corrected_scores['7'] = raw_scores.get('7', 0) + k
    corrected_scores['8'] = raw_scores.get('8', 0) + k
    corrected_scores['9'] = raw_scores.get('9', 0) + round(0.2 * k)

    return corrected_scores


def calculate_t_scores(corrected_scores, M_table, delta_table, sex):
    t_scores = {}

    sex_table_m = M_table["Мужской"] if sex == "Мужской" else M_table["Женский"]
    sex_table_delta = delta_table["Мужской"] if sex == "Мужской" else delta_table["Женский"]

    for scale, raw in corrected_scores.items():
        if scale in sex_table_m and scale in sex_table_delta:
            M = sex_table_m[scale]
            delta = sex_table_delta[scale]
            T = 50 + 10 * (raw - M) / delta
            t_scores[scale] = round(T)
        else:
            print(f"Ошибка: ключ {scale} отсутствует в таблице для {sex} пола")

    return t_scores


def generate_graph(t_scores):
    scales_order = ['L', 'F', 'K', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    scale_labels = ['Л', 'F', 'K', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

    scores = [t_scores.get(scale, 50) for scale in scales_order]

    colors = ['green' if 30 <= score <= 70 else 'red' for score in scores]

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.plot(range(len(scales_order)), scores, color='blue', linewidth=2)

    ax.scatter(range(len(scales_order)), scores, color=colors, s=50, zorder=5)

    for i, score in enumerate(scores):
        ax.text(i + 0.5, score + 1, str(score), ha='center', va='bottom', fontsize=10)

    ax.set_xticks(range(len(scale_labels)))
    ax.set_xticklabels(scale_labels, fontsize=12)

    max_score = max(scores)
    ylim_top = max(120, max_score + 5)
    ax.set_ylim(20, ylim_top)

    ax.set_yticks(range(20, int(ylim_top) + 5, 5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))

    ax.grid(which='major', linestyle='-', linewidth=0.5, color='gray')
    ax.grid(which='minor', linestyle=':', linewidth=0.5, color='lightgray')

    ax.set_xlabel("Шкалы", fontsize=14)
    ax.set_ylabel("T-баллы", fontsize=14)
    ax.set_title("Профиль MMPI", fontsize=16)

    plt.tight_layout()

    graph_file = io.BytesIO()
    plt.savefig(graph_file, format='png')
    graph_file.seek(0)
    plt.close()

    return graph_file




def generate_pdf(graph_file, user):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.drawImage(ImageReader(graph_file), 50, 400, width=500, height=250)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer