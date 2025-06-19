import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/test.css';
import mansQuestions from '../data/mans.txt';
import womansQuestions from '../data/womans.txt';
import backgroundImage from '../img/test-page.png';

const Test = ({ showError }) => {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [buttonsDisabled, setButtonsDisabled] = useState(false);
  const [gender, setGender] = useState(null);

  const navigate = useNavigate();
  const userId = localStorage.getItem('user_id');
  const token = localStorage.getItem('auth_token');

  useEffect(() => {
    const storedGender = localStorage.getItem('gender');
    if (storedGender === 'Мужской' || storedGender === 'Женский') {
      setGender(storedGender);
    } else {
      setGender('Мужской');
    }
  }, []);

  useEffect(() => {
    const completed = localStorage.getItem('test_completed');
    if (completed === 'true') {
      navigate('/');
    }
  }, [navigate]);

  useEffect(() => {
    if (!gender || !userId || !token) return;

    let isMounted = true;

    const filePath = gender === 'Женский' ? womansQuestions : mansQuestions;

    fetch(filePath)
      .then((res) => res.text())
      .then((text) => {
        const list = text.split('\n').map(line => line.trim()).filter(Boolean);
        if (isMounted) setQuestions(list);

        return fetch(`https://mmpi.stk8s.66bit.ru/api/test-status/${userId}/`, {
          headers: {
            'Authorization': `Token ${token}`,
          },
        });
      })
      .then(async (statusRes) => {
        if (!statusRes.ok) throw await statusRes.json();

        const statusData = await statusRes.json();
        const answeredCount = statusData.answered;

        if (answeredCount === 566) {
          localStorage.setItem('test_completed', 'true');
          navigate('/results');
          return;
        }

        const continueRes = await fetch(`https://mmpi.stk8s.66bit.ru/api/test-continue/${userId}/`, {
          headers: {
            'Authorization': `Token ${token}`,
          },
        });

        if (!continueRes.ok) throw await continueRes.json();

        const continueData = await continueRes.json();
        const next = continueData.next_question_number;

        if (isMounted) {
          setCurrentIndex(next !== null ? next - 1 : 0);
        }
      })
      .catch((error) => {
        console.error('[ERROR]', error);
        showError(error);
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [gender, userId, token, navigate, showError]);

  const handleAnswer = async (answer) => {
    if (buttonsDisabled) return;
    setButtonsDisabled(true);

    const questionNumber = currentIndex + 1;

    try {
      const response = await fetch(`https://mmpi.stk8s.66bit.ru/api/answer-post/${userId}/`, {
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

      if (!response.ok) throw await response.json();

      if (currentIndex + 1 === questions.length) {
        localStorage.setItem('test_completed', 'true');
        navigate('/results');
      } else {
        setCurrentIndex(prev => prev + 1);
      }
    } catch (error) {
      console.error('[ERROR]', error);
      showError(error);
    } finally {
      setTimeout(() => setButtonsDisabled(false), 30);
    }
  };

  if (loading || !gender) return <div className="test-container">Загрузка...</div>;
  if (currentIndex >= questions.length) return null;

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
        <p className="progress-text">Прогресс</p>
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
