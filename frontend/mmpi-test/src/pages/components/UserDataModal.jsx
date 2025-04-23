import React, { useState } from 'react';
import '../components/userModal.css';


const UserDataModal = ({ onClose }) => {
  const [gender, setGender] = useState(null);

  return (
    <div className="modal-overlay">
      <div className={`modal-content ${gender === 'male' ? 'modal-male' : ''}`}>
        <button className="close-btn" onClick={onClose}>×</button>
        <h2>Введите ваши данные</h2>

        <div className="gender-select">
          <label>Укажите ваш пол</label>
          <div className="gender-buttons">
            <button
              className={gender === 'female' ? 'active' : ''}
              onClick={() => setGender('female')}
            >
              Женский
            </button>
            <button
              className={gender === 'male' ? 'active' : ''}
              onClick={() => setGender('male')}
            >
              Мужской
            </button>
          </div>
          <small>Обязательно для заполнения</small>
        </div>

        <div className="input-group">
          <label>Укажите ваш возраст</label>
          <input type="number" placeholder="Например, 18" />
          <small>Обязательно для заполнения</small>
        </div>

        <div className="input-group">
          <label>Укажите ваш электронный адрес</label>
          <input type="email" placeholder="Например: you@mail.ru" />
        </div>

        <button className="continue-btn">Продолжить</button>
      </div>
    </div>
  );
};

export default UserDataModal;