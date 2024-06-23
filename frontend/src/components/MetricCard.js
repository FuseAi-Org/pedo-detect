import React from 'react';
import './MetricCard.css';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

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


const MetricCard = ({ title, percentage }) => {
  const color = getColor(percentage);

  return (
    <div className="metric-card">
      <CircularProgressbar
        value={percentage}
        text={`${percentage}`}
        styles={buildStyles({
          textSize: '16px',
          pathColor: color,
          textColor: '#000',
          trailColor: '#d6d6d6',
        })}
      />
      <div className="metric-title">{title}</div>
    </div>
  );
};

export default MetricCard;
