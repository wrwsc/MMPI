import React, { useState } from 'react';
import { } from 'react-router-dom';
import '../styles/main.css';
import { useNavigate } from 'react-router-dom';
import UserDataModal from './components/UserDataModal';
import backgroundImage from '../img/background.png';
import titleImage from '../img/testing-title.png';

const Home = ({ showError }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [showHint1, setShowHint1] = useState(false);
  const [showHint2, setShowHint2] = useState(false);
  const navigate = useNavigate();
  const openModal = () => {
    try {
      setIsModalOpen(true);
    } catch (error) {
      showError(error);
    }
  };
  const continueTest = () => {
    const userId = localStorage.getItem('user_id');
    const token = localStorage.getItem('auth_token');

    if (userId && token) {
      navigate('/test');
    } else {
      showError('Сначала начните тест!');
    }
  };
  const closeModal = () => setIsModalOpen(false);

  return (
    <div
      className="home-container"
      style={{ backgroundImage: `url(${backgroundImage})` }}
    >
      <div className="title-wrapper">
        <img src={titleImage} alt="Тестирование MMPI" className="title-image" />
      </div>

      <div className="content-wrapper">
        <div className="description-box">
          <h2>
            MMPI<br />
            (Minnesota Multiphasic Personality Inventory)
          </h2>
          <p>
            Миннесотский многоаспектный личностный опросник, разработанный в начале 1940-х годов в университете Миннесоты, - это наиболее изученная и одна из самых популярных психодиагностических методик, предназначенная для исследования индивидуальных особенностей и психических состояний личности.
            <br /><br />
            Тест позволяет получить детальный профиль личности, оценить уровень тревожности, депрессии, социальную адаптацию и другие важные психологические параметры.
          </p>
        </div>
      </div>

      <div className="instructions">
        <h2>Инструкция по прохождению теста</h2>
        <p>
          Опросник состоит из 566 утверждений, с каждым из которых вам необходимо либо согласиться, либо нет. Оценивая каждое утверждение, не тратьте много времени на раздумья.
Если утверждение верно по отношению к вам в одних ситуациях и неверно в других, выбирайте тот вариант ответа, который больше подходит в настоящий момент.<br /><br />

Обратите внимание на то, что переход к следующему утверждению осуществляется автоматически при выборе варианта ответа на текущей странице. Нажимайте на ответ только тогда, когда вы уверены в своём выборе.
Также учтите, что возвращаться к предыдущим утверждениям нельзя. После выбора варианта ответа на последней странице произойдёт автоматический переход на страницу с результатами.<br /><br />

Не волнуйтесь, отвечая на достаточно интимные вопросы, ваши ответы не доступны для чтения в открытом доступе, обработка данных ведется автоматически.<br />

Прохождение опросника занимает немало времени, убедитесь, что в ближайшее время вас ничего не потревожит и вы сможете дойти до конца тестирования.
        </p>

      </div>

      <div className="start">
  <p className="time-note">Примерное время прохождения – 2 часа</p>

  <div className="button-with-hint">
    <button className="start-btn" onClick={openModal}>
      Начать тест
    </button>
    <div
      className="hint-icon"
      onMouseEnter={() => setShowHint1(true)}
      onMouseLeave={() => setShowHint1(false)}
    >
      ?
      {showHint1 && (
        <div className="hint-text">
          Прогресс будет сброшен
        </div>
      )}
    </div>
  </div>

  <div className="button-with-hint">
  <button className="continue-test-btn" onClick={continueTest}>
    Продолжить тестирование
  </button>
  <div
    className="hint-icon"
    onMouseEnter={() => setShowHint2(true)}
    onMouseLeave={() => setShowHint2(false)}
  >
    ?
    {showHint2 && (
      <div className="hint-text">
        Вы вернётесь к незавершённым вопросам или результатам тестирования
      </div>
    )}
  </div>
</div>
</div>

      {isModalOpen && <UserDataModal onClose={closeModal} />}
    </div>
  );
};

export default Home;
