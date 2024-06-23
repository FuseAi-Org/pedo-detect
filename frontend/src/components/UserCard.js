import React from 'react';
import './UserCard.css';

// Function to generate a random blueish-purple color
const getRandomBluePurpleColor = () => {
  const hues = [240, 250, 260, 270, 280, 290]; // Hue values for blue to purple range
  const hue = hues[Math.floor(Math.random() * hues.length)];
  const saturation = Math.floor(Math.random() * 50) + 50; // 50-100%
  const lightness = Math.floor(Math.random() * 30) + 40; // 40-70%

  return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
};

// Function to get a color based on the percentage
// Function to get a dulled color based on the percentage
// Function to get a dulled and light color based on the percentage
const getColor = (percentage) => {
  const r = percentage > 50 ? 255 : Math.floor((percentage / 50) * 255);
  const g = percentage < 50 ? 255 : Math.floor(((100 - percentage) / 50) * 255);
  
  // Blend the color with white to lighten it
  const blendWithWhite = (colorValue) => Math.floor((colorValue + 255) / 2);

  return `rgb(${blendWithWhite(r)}, ${blendWithWhite(g)}, ${blendWithWhite(0)})`;
};


const UserCard = ({ name, initial, percentage }) => {
  const circleColor = getRandomBluePurpleColor(); // Generate random blueish-purple color
  const metricColor = getColor(percentage); // Generate color based on percentage

  return (
    <div className="user-card">
      <div className="user-initial" style={{ backgroundColor: circleColor }}>
        {initial}
      </div>
      <div className="user-name">{name}</div>
      <div className="user-metric" style={{ backgroundColor: metricColor }}>
        {percentage}
      </div>
    </div>
  );
};

export default UserCard;
