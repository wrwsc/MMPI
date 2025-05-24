import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Test from './pages/Test';
import Results from './pages/Results';
import Notification from './pages/components/Notification';
import NotFound from './pages/NotFound';

function App() {
  const [error, setError] = useState(null);

  const showError = (error) => {
    console.error('[ERROR]', error);

    const errorMsg = typeof error === 'object' && error?.query?.value
      ? error.query.value
      : (error?.message || error || 'Произошла неизвестная ошибка');

    setError(errorMsg);

    setTimeout(() => setError(null), 3000);
  };

  return (
    <Router>
      <Notification message={error} onClose={() => setError(null)} />

      <Routes>
        <Route path="/" element={<Home showError={showError} />} />
        <Route path="/test" element={<Test showError={showError} />} />
        <Route path="/results" element={<Results showError={showError} />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;
