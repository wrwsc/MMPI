import React, { useState } from 'react';
import '../components/userModal.css';

const UserDataModal = ({ onClose }) => {
  const [selectedGender, setSelectedGender] = useState(null);
  const [age, setAge] = useState('');
  const [email, setEmail] = useState('');

  const handleGenderSelect = (gender) => {
    setSelectedGender(gender);
  };

  const handleContinue = () => {
    if (!selectedGender || !age || !email) {
      alert('Пожалуйста, заполните все поля.');
      return;
    }
    console.log('Данные пользователя:', { selectedGender, age, email });
    onClose();
  };

  // Выбираем стиль фона в зависимости от пола
  const getBackgroundStyle = () => {
    if (selectedGender === 'Женский') {
      return { background: 'rgba(187, 160, 153, 0.39)', backdropFilter: 'blur(10px)' };
    }
    if (selectedGender === 'Мужской') {
      return { background: 'rgba(153, 165, 187, 0.36)', backdropFilter: 'blur(10px)' };
    }
    return { background: 'rgba(50, 50, 50, 0.8)', backdropFilter: 'blur(10px)' }; // фон по умолчанию
  };

  return (
    <div className="modal-container">
      <div className="modal-content" style={getBackgroundStyle()}>
        <button className="close-btn" onClick={onClose}>×</button>
        <h2>ВВЕДИТЕ ВАШИ ДАННЫЕ</h2>

        <div className="gender-selection">
          <label class='text-label'>УКАЖИТЕ ВАШ ПОЛ</label>
          <div className="gender-toggle">
            <div
              className={`toggle-option ${selectedGender === 'Женский' ? 'active female' : ''}`}
              onClick={() => handleGenderSelect('Женский')}
            >
              ЖЕНСКИЙ
            </div>
            <div
              className={`toggle-option ${selectedGender === 'Мужской' ? 'active male' : ''}`}
              onClick={() => handleGenderSelect('Мужской')}
            >
              МУЖСКОЙ
            </div>
          </div>
          <div className="required-note">Обязательное для заполнения поле</div>
        </div>

        <div className="input-field">
          <label class='text-label'>УКАЖИТЕ ВАШ ВОЗРАСТ</label>
          <input class='age-input'
            type="number"
            placeholder="Например: 18"
            value={age}
            onChange={(e) => setAge(e.target.value)}
          />
          <div className="required-note">Обязательное для заполнения поле</div>
        </div>

        <div className="input-field">
          <label class='text-label'>УКАЖИТЕ ВАШ ЭЛЕКТРОННЫЙ АДРЕС</label>
          <input class='email-input'
            type="email"
            placeholder="Например: mmpi@test.ru"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <div className="required-note">Обязательное для заполнения поле</div>
        </div>


        <button className="continue-btn" onClick={handleContinue}>
          Продолжить
        </button>
      </div>
    </div>
  );
};

export default UserDataModal;
