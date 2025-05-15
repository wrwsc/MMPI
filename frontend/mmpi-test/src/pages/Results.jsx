import React from 'react';
import { useLocation } from 'react-router-dom';

const Results = () => {
  const location = useLocation();
  const { answers } = location.state || {}; // Получаем данные из состояния

  return (
    <div className="results-container">
      <h2>Ваши результаты:</h2>
      <ul>
        {answers && answers.map((answer, index) => (
          <li key={index}>Вопрос {index + 1}: {answer}</li>
        ))}
      </ul>
    </div>
  );
};

export default Results;
