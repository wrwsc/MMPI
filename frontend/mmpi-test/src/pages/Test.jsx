import React, { useEffect, useState } from 'react';
import '../styles/test.css';
import mansQuestions from '../data/mans.txt';
import womansQuestions from '../data/womans.txt';
import backgroundImage from '../img/test-page.png';

const Test = ({ gender = 'Мужской' }) => {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState([]);
  
  useEffect(() => {
    const filePath = gender === 'Женский' ? womansQuestions : mansQuestions;
    fetch(filePath)
      .then((res) => res.text())
      .then((text) => {
        const list = text.split('\n').map(line => line.trim()).filter(Boolean);
        setQuestions(list);
      });
  }, [gender]);

  const handleAnswer = async (answer) => {
  const userId = localStorage.getItem('user_id');
  const token = localStorage.getItem('auth_token');
  const questionNumber = currentIndex + 1;

  // Отправка на бэкенд
  fetch(`http://127.0.0.1:8000/api/answer-post/${userId}/`, {
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
})
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    console.log("Ответ успешно отправлен:", data);
  })
  .catch(error => {
    console.error("Ошибка при отправке ответа:", error);
  });

  // Обновляем локальное состояние
  setAnswers(prev => [...prev, answer]);
  setCurrentIndex(prev => prev + 1);
};


  if (currentIndex >= questions.length) {
    return <div className="test-container">Спасибо за прохождение теста!</div>;
  }

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
          <div className="progress-bar-text">{currentIndex + 1}/566</div>
        </div>
      </div>

      <div className="question-box">
        <p>{questions[currentIndex]}</p>
      </div>

      <div className="buttons">
        <button className="btn yes" onClick={() => handleAnswer('Да')}>Да</button>
        <button className="btn no" onClick={() => handleAnswer('Нет')}>Нет</button>
      </div>
    </div>
  );
};

export default Test;
