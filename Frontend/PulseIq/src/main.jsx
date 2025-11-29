import React from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { ActivityProvider } from "./context/ActivityContext";
import App from "./App.jsx";

const root = createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <ActivityProvider>
      <App />
    </ActivityProvider>
  </React.StrictMode>
);
