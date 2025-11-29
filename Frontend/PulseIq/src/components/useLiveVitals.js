// components/useLiveVitals.js
import { useState, useEffect } from "react";

export default function useLiveVitals() {
  const [vitals, setVitals] = useState({
    glucose: 100,
    systolic: 145,
    diastolic: 92,
    heart_rate: 110,
    cholesterol: 240,
    spo2: 92,
    bmi: 27,
  });

  const fluctuate = (value, min, max, step = 5) => {
    const change = Math.floor(Math.random() * step * 2) - step;
    const updated = value + change;
    return Math.max(min, Math.min(max, updated));
  };

  useEffect(() => {
    const interval = setInterval(() => {
      setVitals((prev) => {
        const updated = {
          glucose: fluctuate(prev.glucose, 80, 250, 8),
          systolic: fluctuate(prev.systolic, 100, 180, 5),
          diastolic: fluctuate(prev.diastolic, 60, 120, 3),
          heart_rate: fluctuate(prev.heart_rate, 50, 160, 7),
          cholesterol: fluctuate(prev.cholesterol, 150, 330, 7),
          spo2: fluctuate(prev.spo2, 85, 100, 1),
          bmi: fluctuate(prev.bmi, 18, 35, 1),
        };

        console.log("🔄 Sending vitals to backend:", updated);

        // Send to backend
        fetch("http://127.0.0.1:5000/update_vitals", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(updated),
        })
          .then((res) => res.json())
          .then((data) => console.log("✅ Server response:", data))
          .catch((err) => console.error("❌ Error sending vitals:", err));

        return updated;
      });
    }, 30000); // 🔥 update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  return vitals;
}
