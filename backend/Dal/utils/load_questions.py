import os

def load_questions(sex):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "mans.txt" if sex == "Мужской" else "womans.txt"
    path = os.path.join(base_dir, "../questions", filename)

    try:
        with open(path, encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []
