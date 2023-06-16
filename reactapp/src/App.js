import React from 'react';
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const MyComponent = () => {
  const [games, setGames] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/xbox_games/')
      .then(response => {
        setGames(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  return (
    <div>
      {games.map(game => (
        <div key={game.id}>
          <h2>{game.title}</h2>
          <p>Product ID: {game.product_id}</p>
          <p>Base Price: ${game.base_price}</p>
          <p>Discounted Price: ${game.discounted_price}</p>
          <img src={game.img} alt={game.title} />
        </div>
      ))}
    </div>
  );
}

export default MyComponent;
