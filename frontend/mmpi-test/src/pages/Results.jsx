import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/results.css';
import CheckIcon from '../img/check-icon.png';
import ClinicalScalesImage from '../img/clinical-scales.png';
import EvaluativeScalesImage from '../img/evaluative-scales.png';
import RoundingScalesImage from '../img/rounding-scales.png';
import СonstantsScalesImage from '../img/constants-scales.png';

const Result = () => {
  const navigate = useNavigate();
  const [graphUrl, setGraphUrl] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const userId = localStorage.getItem('user_id');
    const token = localStorage.getItem('auth_token');

    if (!userId || !token) {
      navigate('/');
      return;
    }

    fetch(`https://mmpi.stk8s.66bit.ru/api/test-status/${userId}/`, {
      headers: {
        'Authorization': `Token ${token}`,
      },
    })
      .then(res => {
        if (!res.ok) throw new Error('Ошибка при проверке статуса теста');
        return res.json();
      })
      .then(async data => {
        if (data.answered < 566) {
          navigate('/test');
        } else {
          const response = await fetch(`https://mmpi.stk8s.66bit.ru/api/graph/image/${userId}/`, {
            headers: {
              'Authorization': `Token ${token}`,
            },
          });
          if (!response.ok) throw new Error('Ошибка при загрузке графика');

          const blob = await response.blob();
          const url = URL.createObjectURL(blob);
          setGraphUrl(url);

          localStorage.setItem('test_completed', 'true');
        }
      })
      .catch(err => {
        console.error('Ошибка:', err);
        navigate('/');
      })
      .finally(() => setLoading(false));
  }, [navigate]);


  const handleDownload = async () => {
    const userId = localStorage.getItem('user_id');
    const token = localStorage.getItem('auth_token');

    try {
      const response = await fetch(`https://mmpi.stk8s.66bit.ru/api/graph/image/${userId}/`, {
        headers: {
          'Authorization': `Token ${token}`,
        },
      });
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'Результаты_MMPI.png');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Ошибка при скачивании графика:', error);
    }
  };

  if (loading) return <div>Загрузка...</div>;

  return (
    <div className="result-container">
      <div className="go-home-button-wrapper">
        <button className="go-home-button" onClick={() => navigate('/')}>
          На главную
        </button>
      </div>

      <div className="result-header">
        <img src={CheckIcon} alt="Успех" className="result-check-icon" />
        <h1 className="result-title">
          Поздравляем с успешным<br />прохождением тестирования!
        </h1>
      </div>

      <div className="result-buttons">
        <div className="button-with-note">
          <button className="result-btn save-button" onClick={handleDownload}>
            Сохранить результат
          </button>
          <p className="result-note">Результат сохранится в формате PNG на ваше устройство</p>
        </div>
        {/* <div className="button-with-note">
          <button className="result-btn send-button">Отправить результат</button>
          <p className="result-note">Результат будет отправлен на электронную почту</p>
        </div> */}
      </div>

      <h3 className="first-subtitle result-subtitle ">Ниже вы можете увидеть график с результатами</h3>
      {graphUrl ? (
        <img src={graphUrl} alt="График результатов" className="result-graph" />
      ) : (
        <div className="placeholder">Загрузка графика...</div>
      )}

      <p className="result-description">
        Перед вами результаты по 10 основным шкалам. Красным отмечены шкалы, которые выходят за пределы коридора нормы (норма от 30T - до 70T).<br /><br />
        В узком коридоре нормы — в пределах 46 — 55 Т — колебания профиля трудно интерпретируемые, так как они не выявляют достаточно выраженных индивидуально-личностных свойств и характерны для полностью сбалансированной личности.<br /><br />
        В широком коридоре нормы (от 30 до 70 Т) в профиле нормы каждой тенденции противопоставлена противоположная по направленности «антитенденция», а чувства и поведение подчинены контролю сознания (или эмоции настолько умеренны, что минимальный контроль над ними оказывается вполне достаточным).<br /><br />
        Повышения, колеблющиеся в пределах 56 — 66 Т, выявляют те ведущие тенденции, которые определяют характерологические особенности индивида.<br /><br />
        Более высокие показатели разных базисных шкал (67-75 Т) выделяют те акцентуированные (сильно выраженные) черты, которые временами затрудняют социально-психологическую адаптацию человека.<br /><br />
        Показатели выше 75 Т свидетельствуют о нарушенной адаптации и об отклонении состояния индивида от нормального. Это могут быть психопатические черты характера, состояние стресса, вызванное экстремальной ситуацией, невротические расстройства и, наконец, психопатология, о наличии которой может судить только патопсихолог или психиатр по совокупности данных психодиагностического, экспериментально-психологического и клинического исследования.
      </p>

      <h3 className="result-subtitle">Ниже вы можете ознакомиться с описанием основных шкал</h3>

      <h4 className="scale-section-title">Клинические шкалы и их значения</h4>
      <img src={ClinicalScalesImage} alt="Клинические шкалы" className="result-scale-image" />

      <h4 className="scale-section-title">Оценочные шкалы и их значения</h4>
      <img src={EvaluativeScalesImage} alt="Оценочные шкалы" className="result-scale-image" />

      <p className="result-formula">
        Баллы рассчитывались по следующей формуле:<br />
        <strong>T = 50 + 10 × (X - M) / σ</strong>, где:<br />
        X — "сырой" балл испытуемого по шкале<br />
        M — среднее значение по нормативной выборке<br />
        σ — стандартное отклонение по нормативной выборке<br /><br />
        Пример:<br />
        Допустим, по шкале 2 испытуемый набрал 25 сырых баллов. Подставляя в формулу, получаем:<br />
        <strong>T = 50 + 10 × (25 - 18.9) / 5 = 62.2</strong> — данный результат соответствует норме.
      </p>
      <h4 className="scale-section-title">Произведения округлялись в соответствии со следующей таблицей:</h4>
      <img src={RoundingScalesImage} alt="Оценочные шкалы" className="round-scale-image" />
      <h4 className="scale-section-title">Значения констант:</h4>
      <img src={СonstantsScalesImage} alt="Оценочные шкалы" className="result-scale-image" />
      <p className="result-description">Пример:<br />
        Допустим, по шкале 2 испытуемый набрал 25 сырых баллов. Подставляя в формулу получаем: T = 50 + 10*(25 - 18.9)/5 = 62.2 - данный результат соответствует норме.</p>
      <p className="result-footer">
        Результаты тестирования могут показать наличие проблем, но должны интерпретироваться исключительно специалистом.
      </p>
    </div>
  );
};

export default Result;
