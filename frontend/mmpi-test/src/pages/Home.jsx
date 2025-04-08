import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/main.css';

const Home = () => {
  const navigate = useNavigate();

  const startTest = () => {
    navigate('/test');
  };

  return (
    <div className="home-container">
      <header className="home-header">
        <h1>ТЕСТИРОВАНИЕ</h1>
        <h2>MMPI</h2>
      </header>

      <div className="illustration">
        <span className="choice left">Да</span>
        <div className="image-block"></div>
        <span className="choice right">Нет</span>
      </div>

      <div className="test-content">
        <section className="test-description">
          <h3>Описание теста</h3>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse at erat at lacus hendrerit vulputate. Proin porttitor dui ut aliquam congue. Mauris tempus molestie porta. Donec suscipit mauris id suscipit suscipit. Sed efficitur nibh sed elit dignissim, suscipit dictum dui porttitor. Sed feugiat dolor nibh, at dictum ipsum cursus non. Vivamus arcu tellus, sollicitudin non lacus vitae, aliquam tincidunt turpis. Aliquam feugiat massa elit, in suscipit lacus mattis vitae. Sed placerat orci in eros aliquet, a ultrices ante rutrum. Donec convallis eros felis, sit amet sollicitudin massa interdum eu. Curabitur fringilla eget tellus id accumsan. Aenean vulputate lorem nisl.
          </p>
          <p>
            Sed fringilla nisi aliquet orci euismod, eget blandit lacus tincidunt. Nam rutrum pulvinar ex, sit amet tincidunt dolor feugiat vel. Praesent blandit nec elit sed aliquam. Maecenas aliquet neque sollicitudin vehicula luctus. Mauris sodales at dolor id iaculis. Aliquam erat volutpat. Nunc elementum ornare augue, eu malesuada ligula aliquam quis. Sed imperdiet vestibulum tellus, eget fermentum felis. Praesent imperdiet ullamcorper nunc, id maximus enim laoreet at. Nullam urna est, laoreet ac venenatis in, laoreet et augue. Donec ipsum massa, ultricies sodales posuere et, venenatis nec magna. In bibendum nisl orci, eu faucibus ipsum efficitur sed. Curabitur eget leo leo. Fusce tellus elit, laoreet in nisl sit amet, tristique scelerisque orci.
          </p>
        </section>

        <section className="test-instructions">
          <h3>Инструкция по прохождению теста</h3>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse at erat at lacus hendrerit vulputate. Proin porttitor dui ut aliquam congue. Mauris tempus molestie porta. Donec suscipit mauris id suscipit suscipit. Sed efficitur nibh sed elit dignissim, suscipit dictum dui porttitor. Sed feugiat dolor nibh, at dictum ipsum cursus non. Vivamus arcu tellus, sollicitudin non lacus vitae, aliquam tincidunt turpis. Aliquam feugiat massa elit, in suscipit lacus mattis vitae. Sed placerat orci in eros aliquet, a ultrices ante rutrum. Donec convallis eros felis, sit amet sollicitudin massa interdum eu. Curabitur fringilla eget tellus id accumsan. Aenean vulputate lorem nisl.
          </p>
        </section>
      </div>




      <div className="test-duration">
        Примерное время прохождения - 2 часа
      </div>

      <button className="start-test-button" onClick={startTest}>
        Начать тест
      </button>
    </div>
  );
};

export default Home;
