import React from "react";

export default function VitalStatCard({ label, value, unit, thresholds }) {
  
  const getColor = () => {
    if (value >= thresholds.danger.min && value <= thresholds.danger.max)
      return "#FF4B4B"; // red

    if (value >= thresholds.warning.min && value <= thresholds.warning.max)
      return "#FFA500"; // orange

    return "#0FA76A"; // green (normal)
  };

  const color = getColor();

  return (
    <div className="
      group
      flex flex-col items-center justify-center 
      p-5 
      rounded-2xl 
      bg-gray-50 border border-gray-100
      hover:bg-white hover:shadow-lg hover:shadow-black/5 hover:border-transparent
      transition-all duration-300 ease-out
    ">
      
      {/* Label: Small, Uppercase, Utility Gray */}
      <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4">
        {label}
      </h2>

      {/* Ring Container */}
      <div 
        className="
          relative 
          w-20 h-20 
          rounded-full 
          flex items-col flex-col items-center justify-center 
          transition-transform duration-300 group-hover:scale-105
        "
        style={{
          border: `4px solid ${color}`, // Thinner border for minimalist look
          // Removed the neon glow box-shadow for a cleaner 'Matte' look
        }}
      >
        {/* Value */}
        <span className="text-2xl font-bold tracking-tight" style={{ color }}>
          {value}
        </span>
        
        {/* Unit (Tucked inside the ring for compactness) */}
        <span className="text-[10px] font-medium text-gray-400 leading-none mt-0.5">
            {unit}
        </span>
      </div>

    </div>
  );
}