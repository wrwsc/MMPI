import React from 'react';
import '../components/notification.css';

const Notification = ({ message, onClose }) => {
  if (!message) return null;

  return (
    <div className="notification">
      <div className="notification-content">
        <p>{message}</p>
        <button onClick={onClose}>Закрыть</button>
      </div>
    </div>
  );
};

export default Notification;
