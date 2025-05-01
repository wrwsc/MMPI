import React, { useState, useEffect } from 'react';
import '../components/userModal.css';

const UserDataModal = ({ onClose }) => {
  const [selectedGender, setSelectedGender] = useState(null);
  const [age, setAge] = useState('');
  const [email, setEmail] = useState('');
  const [isClosing, setIsClosing] = useState(false);

  const handleGenderSelect = (gender) => {
    setSelectedGender(gender);
  };

  const handleContinue = () => {
    if (!selectedGender || !age || !email) {
      return;
    }
    console.log('Данные пользователя:', { selectedGender, age, email });
    handleClose(); // Плавно закрыть
  };

  const handleClose = () => {
    setIsClosing(true);
    setTimeout(() => {
      onClose(); // Закрываем после завершения анимации
    }, 200);
  };

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        handleClose();
      }
    };
  
    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  const getBackgroundStyle = () => {
    if (selectedGender === 'Женский') {
      return { background: 'rgba(187, 160, 153, 0.55)', backdropFilter: 'blur(10px)' };
    }
    if (selectedGender === 'Мужской') {
      return { background: 'rgba(153, 165, 187, 0.55)', backdropFilter: 'blur(10px)' };
    }
    return { background: 'rgba(157, 149, 146, 0.55)', backdropFilter: 'blur(10px)' };
  };

  return (
    <div className="modal-container">
      <div
        className={`modal-content ${isClosing ? 'closing' : ''}`}
        style={getBackgroundStyle()}
      >
        <button className="close-btn" onClick={handleClose}>×</button>
        <h2>ВВЕДИТЕ ВАШИ ДАННЫЕ</h2>

        <div className="gender-selection">
          <label className="text-label">УКАЖИТЕ ВАШ ПОЛ</label>
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
          <label className="text-label">УКАЖИТЕ ВАШ ВОЗРАСТ</label>
          <input
            className="age-input"
            type="number"
            placeholder="Например: 18"
            value={age}
            onChange={(e) => setAge(e.target.value)}
          />
          <div className="required-note">Обязательное для заполнения поле</div>
        </div>

        <div className="input-field">
          <label className="text-label">УКАЖИТЕ ВАШ ЭЛЕКТРОННЫЙ АДРЕС</label>
          <input
            className="email-input"
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
