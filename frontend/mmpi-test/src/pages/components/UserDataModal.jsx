import React, { useState, useEffect } from 'react'; 
import '../components/userModal.css';

const UserDataModal = ({ onClose }) => {
  const [selectedGender, setSelectedGender] = useState(null);
  const [age, setAge] = useState('');
  const [email, setEmail] = useState('');
  const [isClosing, setIsClosing] = useState(false);
  const [genderError, setGenderError] = useState(false);
  const [ageError, setAgeError] = useState(false);
  const [emailError, setEmailError] = useState(false);

  const handleGenderSelect = (gender) => {
    setSelectedGender(gender);
    setGenderError(false); // сбрасываем ошибку при изменении
  };

  const handleAgeChange = (e) => {
    const value = e.target.value;
    setAge(value);
    if (value) setAgeError(false); // сбрасываем ошибку при изменении
  };

  const handleEmailChange = (e) => {
    const value = e.target.value;
    setEmail(value);
    if (value) setEmailError(false); // сбрасываем ошибку при изменении
  };

  const handleContinue = () => {
    let hasError = false;

    // Gender
    if (!selectedGender) {
      setGenderError(true);
      hasError = true;
    }

    // Age
    const numericAge = parseInt(age, 10);
    if (!age) {
      setAgeError("Обязательное поле");
      hasError = true;
    } else if (isNaN(numericAge) || numericAge < 18 || numericAge > 120) {
      setAgeError("Возраст должен быть от 18 до 120");
      hasError = true;
    }

    // Email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email) {
      setEmailError("Обязательное поле");
      hasError = true;
    } else if (!emailRegex.test(email)) {
      setEmailError("Введите адрес электронной почты правильно");
      hasError = true;
    }

    if (hasError) return;

    console.log('Данные пользователя:', { selectedGender, age, email });
    handleClose();
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
          <div className={`gender-toggle ${genderError ? 'error-border' : ''}`}>
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
          {genderError && <div className="error-container">Обязательное поле</div>}
        </div>

        <div className="input-field">
          <label className="text-label">УКАЖИТЕ ВАШ ВОЗРАСТ</label>
          <input
            className={`age-input ${ageError ? 'error-border' : ''}`}
            type="number"
            placeholder="Например: 18"
            value={age}
            onChange={handleAgeChange}
          />
          {ageError && <div className="error-container">{ageError}</div>}
        </div>

        <div className="input-field">
          <label className="text-label">УКАЖИТЕ ВАШ ЭЛЕКТРОННЫЙ АДРЕС</label>
          <input
            className={`email-input ${emailError ? 'error-border' : ''}`}
            type="email"
            placeholder="Например: mmpi@test.ru"
            value={email}
            onChange={handleEmailChange}
          />
          {emailError && <div className="error-container">{emailError}</div>}
        </div>

        <button className="continue-btn" onClick={handleContinue}>
          Продолжить
        </button>
      </div>
    </div>
  );
};

export default UserDataModal;
