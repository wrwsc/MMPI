import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/test.css';
import mansQuestions from '../data/mans.txt';
import womansQuestions from '../data/womans.txt';
import backgroundImage from '../img/test-page.png';

const Test = () => {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [buttonsDisabled, setButtonsDisabled] = useState(false);
  const [gender, setGender] = useState(null); // ключевое изменение

  const navigate = useNavigate();
  const userId = localStorage.getItem('user_id');
  const token = localStorage.getItem('auth_token');

  // Загружаем пол из localStorage при инициализации
  useEffect(() => {
    const storedGender = localStorage.getItem('gender');
    if (storedGender === 'Мужской' || storedGender === 'Женский') {
      setGender(storedGender);
    } else {
      setGender('Мужской'); // по умолчанию
    }
  }, []);

  // Загружаем вопросы и данные пользователя только после определения пола
  useEffect(() => {
    if (!gender) return;

    console.log('[INFO] Открытие страницы теста с полом:', gender);

    const filePath = gender === 'Женский' ? womansQuestions : mansQuestions;

    fetch(filePath)
      .then((res) => res.text())
      .then((text) => {
        const list = text.split('\n').map(line => line.trim()).filter(Boolean);
        setQuestions(list);
        console.log(`[INFO] Загружено ${list.length} вопросов`);

        return fetch(`http://127.0.0.1:8000/api/answer-get/${userId}/`, {
          method: 'GET',
          headers: {
            'Authorization': `Token ${token}`,
          },
        })
          .then(res => res.json())
          .then((data) => {
            console.log('[INFO] Загружены данные ответов пользователя');
            const firstUnanswered = list.findIndex((_, index) => data[`Вопрос ${index + 1}`] == null);
            setCurrentIndex(firstUnanswered >= 0 ? firstUnanswered : list.length);
            setAnswers(Object.values(data));
          });

      })
      .catch((error) => {
        console.error('[ERROR] Ошибка при загрузке теста или ответов:', error);
      })
      .finally(() => {
        setLoading(false);
      });

  }, [gender, userId, token]);

  const handleAnswer = async (answer) => {
    if (buttonsDisabled) return;
    setButtonsDisabled(true);

    const questionNumber = currentIndex + 1;
    console.log(`[ACTION] Ответ на вопрос ${questionNumber}: ${answer}`);

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/answer-post/${userId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${token}`,
        },
        body: JSON.stringify({
          user_id: parseInt(userId),
          question_number: questionNumber,
          answer: answer,
        }),
      });

      if (!response.ok) {
        throw new Error(`Ошибка ответа: ${response.status}`);
      }

      const data = await response.json();
      console.log(`[INFO] Ответ на вопрос ${questionNumber} успешно отправлен`);

      const newAnswers = [...answers, answer];
      setAnswers(newAnswers);
      setCurrentIndex(prev => prev + 1);

      localStorage.setItem('answers', JSON.stringify(newAnswers));
      localStorage.setItem('currentIndex', currentIndex + 1);

      if (currentIndex + 1 === questions.length) {
        console.log('[INFO] Тест завершен. Перенаправление на страницу результатов');
        navigate('/results', { state: { answers: newAnswers } });
      }
    } catch (error) {
      console.error('[ERROR] Не удалось отправить ответ:', error);
    } finally {
      setTimeout(() => setButtonsDisabled(false), 300);
    }
  };

  if (loading || !gender) {
    return <div className="test-container">Загрузка...</div>;
  }

  if (currentIndex >= questions.length) {
    return null;
  }

  console.log(`[STATE] currentIndex = ${currentIndex}, questions.length = ${questions.length}`);

  return (
    <div
      className="test-container"
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      }}
    >
      <div className="progress-wrapper">
        <div className="progress-bar-background">
          <div className="progress-bar-fill" style={{ width: `${(currentIndex + 1) * 1.65}px` }}></div>
          <div className="progress-bar-text">{currentIndex + 1}/{questions.length}</div>
        </div>
      </div>

      <div className="question-box">
        <p>{questions[currentIndex]}</p>
      </div>

      <div className="buttons">
        <button className="btn yes" onClick={() => handleAnswer('Да')} disabled={buttonsDisabled}>Да</button>
        <button className="btn no" onClick={() => handleAnswer('Нет')} disabled={buttonsDisabled}>Нет</button>
      </div>
    </div>
  );
};

export default Test;
