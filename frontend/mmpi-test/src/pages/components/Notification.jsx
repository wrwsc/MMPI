import React from 'react';
import '../components/notification.css';

const Notification = ({ message }) => {
  if (!message) return null;

  return (
    <div className="notification">
      <div className="notification-content">
        <p>{message}</p>
      </div>
    </div>
  );
};

export default Notification;
