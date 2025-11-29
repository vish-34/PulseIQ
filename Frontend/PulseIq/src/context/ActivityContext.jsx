import React, { createContext, useContext, useEffect, useState } from "react";

const ActivityContext = createContext();

export function ActivityProvider({ children }) {
  const [activities, setActivities] = useState(() => {
    try {
      const raw = localStorage.getItem("pulse_activities");
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem("pulse_activities", JSON.stringify(activities));
    } catch (e) {
      console.error("Failed to persist activities", e);
    }
  }, [activities]);

  function addActivity(text) {
    const timestamp = new Date().toISOString();
    const item = { id: Date.now(), text, timestamp };
    // newest first
    setActivities(prev => [item, ...prev]);
  }

  function clearActivities() {
    setActivities([]);
  }

  return (
    <ActivityContext.Provider value={{ activities, addActivity, clearActivities }}>
      {children}
    </ActivityContext.Provider>
  );
}

export function useActivity() {
  const ctx = useContext(ActivityContext);
  if (!ctx) throw new Error("useActivity must be used inside ActivityProvider");
  return ctx;
}
