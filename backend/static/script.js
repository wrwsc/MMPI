document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("register-form");
    if (registerForm) {
        registerForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const email = document.getElementById("email").value;
            const sex = document.querySelector('input[name="sex"]:checked').value;
            const birthDate = document.getElementById("birth_date").value;

            const userData = { email, sex, birth_date: birthDate };

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

exportGraphButton.addEventListener("click", async () => {
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

    try {
        const response = await fetch(`http://127.0.0.1:8000/api/export-graph/${user_id}/`, {
            method: "GET",
            headers: {
                "Authorization": `${token}`,
            },
        });

        if (!response.ok) {
            const responseData = await response.json();
            alert("Ошибка: " + JSON.stringify(responseData));
            return;
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'test_results.pdf';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        alert("График успешно экспортирован!");

    } catch (error) {
        console.error("Ошибка при экспорте графика:", error);
        alert("Ошибка сети при экспорте графика.");
    }
});
