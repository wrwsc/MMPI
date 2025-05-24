// App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Test from './pages/Test';
import Results from './pages/Results';
import Notification from '../src/pages/components/Notification';
import NotFound from './pages/NotFound'; // компонент-заглушка 404

function App() {
  const [error, setError] = useState(null);

  const showError = (error) => {
    console.error('[ERROR]', error);

    // Пытаемся получить поле "query.value" из ответа, если есть
    const errorMsg = typeof error === 'object' && error?.query?.value
      ? error.query.value
      : (error?.message || 'Произошла неизвестная ошибка');

    setError(errorMsg);

    // Показываем уведомление, не перенаправляем
    setTimeout(() => setError(null), 4000);
  };

  return (
    <Router>
      {error && <div className="error-notification">{error}</div>}

      <Routes>
        <Route path="/" element={<Home showError={showError} />} />
        <Route path="/test" element={<Test showError={showError} />} />
        <Route path="/results" element={<Results showError={showError} />} />
        <Route path="*" element={<NotFound />} /> {/* Заглушка 404 */}
      </Routes>
    </Router>
  );
}

export default App;
