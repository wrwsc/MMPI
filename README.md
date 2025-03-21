# MMPI

## Установка зависимостей

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/wrwsc/MMPI.git
    ```

2. Перейдите в директорию проекта:
    ```bash
    cd backend
    ```

3. Создайте виртуальное окружение:
    ```bash
    python -m venv venv
    ```

4. Активируйте виртуальное окружение:
    - Для **Windows**:
      ```bash
      venv\Scripts\activate
      ```
    - Для **macOS/Linux**:
      ```bash
      source venv/bin/activate
      ```

5. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```
6. Запустите docker desktop и активируйте конфигурацию:
   ```bash
   docker compose ud -d
   ```

## Настройка PyCharm

1. Откройте проект в **PyCharm**.
2. Перейдите в **File > Settings > Project: MMPI > Python Interpreter**.
3. Нажмите **Add** и выберите **Existing environment**, затем укажите путь к вашему виртуальному окружению (`venv/Scripts/python` для Windows или `venv/bin/python` для macOS/Linux).
4. Создайте конфигурацию для запуска Django сервера (Run > Edit Configurations > StartUpBackend).

## Настройка VS Code

1. Убедитесь, что у вас установлен **VS Code** и плагин Python.
2. Откройте проект в **VS Code**.
3. Убедитесь, что виртуальное окружение активировано, и настройки конфигурации `settings.json`, `launch.json`, и `tasks.json` присутствуют в папке `.vscode/`.
4. Вы можете запустить сервер с помощью кнопки **Run** или горячей клавиши **F5**.


