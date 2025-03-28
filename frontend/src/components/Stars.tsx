import React from "react";
import "./Stars.css";

interface StarsBackgroundProps {
    numberOfStars: number;
  }
  
const Stars: React.FC<StarsBackgroundProps> = React.memo(({ numberOfStars }) => {
  const generateStars = () => {
    const stars = [];
    for (let i = 0; i < numberOfStars; i++) {
      const size = Math.random() * 3;
      const left = Math.random() * 100;
      const top = Math.random() * 100;
      const animationDuration = Math.random() * 5 + 5; // Adjusted for slower movement
      const delay = Math.random() * 2;
      const starStyle = {
        width: `${size}px`,
        height: `${size}px`,
        left: `${left}%`,
        top: `${top}%`,
        animationDuration: `${animationDuration}s`,
        animationDelay: `-${delay}s`,
      };
      stars.push(<div key={i} className="star" style={starStyle}></div>);
    }
    return stars;
  };

  return <div className="stars-background">{generateStars()}</div>;
});

export default Stars;
