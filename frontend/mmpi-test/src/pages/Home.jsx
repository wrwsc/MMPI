import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/main.css';
import UserDataModal from './components/UserDataModal';
import backgroundImage from '../img/background.png';
import titleImage from '../img/testing-title.png';

const Home = () => {
  const navigate = useNavigate();
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

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
          Опросник состоит из 566 утверждений, с каждым из которых вам необходимо либо согласиться, либо нет. Оценивая каждое утверждение, не тратьте много времени на раздумья. Если утверждение верно по отношению к вам в одних ситуациях и неверно в других, выбирайте тот вариант ответа, который больше подходит в настоящий момент.<br /><br />
          Не волнуйтесь, отвечая на достаточно интимные вопросы, ваши ответы не доступны для чтения в открытом доступе, обработка данных ведётся автоматически.<br /><br />
          Прохождение опросника занимает немало времени. Убедитесь, что в ближайшее время вас ничего не потревожит и вы сможете дойти до конца тестирования.
        </p>

      </div>
      <div className="start">
        <p className="time-note">Примерное время прохождения – 2 часа</p>
        <button className="start-btn" onClick={openModal}>
          Начать тест
        </button>
      </div>
      {isModalOpen && <UserDataModal onClose={closeModal} />}
    </div>

  );
};

export default Home;
