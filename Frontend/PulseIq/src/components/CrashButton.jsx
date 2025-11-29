import React from "react";

export default function CrashButton({ onCrash }) {
  return (
    <button
      onClick={onCrash}
      className="px-5 py-3 rounded-xl bg-red-500 text-white font-semibold 
      hover:bg-red-600 hover:scale-105 transition shadow-lg"
    >
      Trigger Crash
    </button>
  );
}