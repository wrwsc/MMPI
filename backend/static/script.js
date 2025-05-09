document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("register-form");
    if (registerForm) {
        registerForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const email = document.getElementById("email").value;
            const sex = document.querySelector('input[name="sex"]:checked').value;
            const age = document.getElementById("age").value;

            const userData = { email, sex, age };

            try {
                const response = await fetch("http://127.0.0.1:8000/api/register/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(userData),
                });

                const responseData = await response.json();

                if (!response.ok) {
                    alert("Ошибка регистрации: " + JSON.stringify(responseData));
                    return;
                }

                if (!responseData.token) {
                    alert("Ошибка: отсутствует токен.");
                    return;
                }

                localStorage.setItem("user", JSON.stringify({
                    user_id: responseData.user_id,
                    email: responseData.email,
                    token: responseData.token,
                }));

                console.log("Пользователь сохранен:", localStorage.getItem("user"));
                window.location.href = "/test/";
            } catch (error) {
                console.error("Ошибка сети:", error);
                alert("Ошибка сети при регистрации.");
            }
        });
    }

    const testForm = document.getElementById("test-form");
    if (testForm) {
        testForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const userDataRaw = localStorage.getItem("user");
            if (!userDataRaw) {
                alert("Вы не вошли в систему. Пожалуйста, авторизуйтесь.");
                return;
            }

            const user = JSON.parse(userDataRaw);
            const token = user.token;
            const user_id = user.user_id;

            if (!token || !user_id) {
                alert("Недопустимые данные авторизации.");
                return;
            }

            const formData = new FormData(testForm);
            const answers = [];

            formData.forEach((value, key) => {
                const match = key.match(/^answer_(\d+)$/);
                if (match) {
                    const question_number = 1;
                    answers.push({
                        user_id,
                        question_number,
                        answer: value,
                    });
                }
            });

            console.log("Подготовленные ответы:", answers);

            for (const answer of answers) {
                try {
                    const response = await fetch(`/api/answer-post/${user_id}/`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": `Token ${token}`,
                        },
                        body: JSON.stringify(answer),
                    });

                    const responseData = await response.json();

                    if (!response.ok) {
                        console.error(`Ошибка отправки ответа ${answer.question_number}:`, responseData);
                        alert(`Ошибка при отправке ответа на вопрос ${answer.question_number}: ${JSON.stringify(responseData)}`);
                        return;
                    }

                    console.log(`Ответ на вопрос ${answer.question_number} успешно сохранен.`);
                } catch (error) {
                    console.error(`Сетевая ошибка при ответе на вопрос ${answer.question_number}:`, error);
                    alert("Сетевая ошибка. Повторите попытку.");
                    return;
                }
            }

            alert("Все ответы успешно отправлены!");
        });
    }
});
