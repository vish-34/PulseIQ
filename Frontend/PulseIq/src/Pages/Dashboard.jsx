import React, { useState } from "react";
import Navbar from "../components/Navbar";
import VitalStatCard from "../components/VitalStatCard";
import ChatBot from "../components/Chatbot";
import CrashButton from "../components/CrashButton";

import { thresholds } from "../components/VitalsThresholds";
import useLiveVitals from "../components/useLiveVitals";
import { Activity, Zap, Square } from "lucide-react";

export default function Dashboard() {
  const vitals = useLiveVitals();
  window.currentVitals = vitals;

  // 1️⃣ STATE: Track if crash simulation is active
  const [isTriggering, setIsTriggering] = useState(false);

  // -------------------------------
  // 🚀 START CRASH (Trigger Logic)
  // -------------------------------
  const triggerCrash = async () => {
    const friendURL = "https://c7ed05df9ed5.ngrok-free.app/api/trigger/crash";

    try {
      setIsTriggering(true); // Switch button to STOP immediately
      console.log("🚀 Sending crash trigger request...");

      const res = await fetch(friendURL, {
        method: "GET",
        headers: {
          "X-Trigger-Token": "CRASH_BUTTON",
          "Accept": "application/json",
          "ngrok-skip-browser-warning": "true",
        },
      });

      console.log("📡 Response status:", res.status);

      const contentType = res.headers.get("content-type") || "";
      const rawText = await res.text();

      if (!res.ok) throw new Error(`Server Error ${res.status}`);
      if (!contentType.includes("application/json")) throw new Error("Backend returned non-JSON");

      const data = JSON.parse(rawText);
      console.log("✅ Crash triggered successfully:", data);
      
      alert("✅ Crash simulation started!\nIncident ID: " + data.incident_id);

    } catch (err) {
      console.error("❌ Error triggering crash:", err);
      alert("⚠️ Crash trigger failed:\n" + err.message);
      setIsTriggering(false); // Reset button only on error
    }
  };

  // -------------------------------
  // 🛑 STOP CRASH (Cancel Logic)
  // -------------------------------
  const stopCrash = async () => {
    setIsTriggering(false);

    const cancelURL = "https://c7ed05df9ed5.ngrok-free.app/api/trigger/cancel";

    try {
      console.log("🛑 Sending stop request...");
      
      const res = await fetch(cancelURL, {
        method: "GET",
        headers: {
          "X-Trigger-Token": "CRASH_BUTTON",
          "ngrok-skip-browser-warning": "true",
        }
      });

      if (res.ok) {
        console.log("✅ Crash simulation canceled successfully.");
      } else {
        console.error("⚠️ Stop request failed with status:", res.status);
      }
    } catch (err) {
      console.error("❌ Error stopping crash:", err);
    }
  };

  // -------------------------------
  // UI RENDER
  // -------------------------------
  return (
    <div className="h-screen w-full bg-white text-black flex flex-col overflow-hidden relative selection:bg-black selection:text-white font-sans">
      
      {/* Noise background */}
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.03] z-0"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
        }}
      ></div>

      {/* HEADER */}
      <header className="z-10 shrink-0 flex flex-wrap items-center justify-between px-4 py-4 md:px-8 md:py-5 border-b border-black/5 bg-white/80 backdrop-blur-sm gap-4">
        <Navbar />

        <div className="flex items-center gap-4 md:gap-6 ml-auto">
          {/* Status Indicator - Hidden on very small screens, visible on md+ */}
          <div className="hidden md:flex flex-col items-end">
            <span className="text-[10px] font-bold tracking-widest uppercase text-gray-400">
              System Status
            </span>
            <span className="flex items-center gap-1.5 text-xs font-semibold text-green-600">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
              </span>
              Online
            </span>
          </div>

          <div className="h-8 w-[1px] bg-gray-200 hidden md:block"></div>

          {/* 🔘 BUTTON SWITCHER */}
          {!isTriggering ? (
            <CrashButton onCrash={triggerCrash} />
          ) : (
            <button
              onClick={stopCrash}
              className="flex items-center gap-2 px-4 py-2 md:px-6 md:py-3 bg-red-600 text-white font-bold rounded-xl shadow-lg hover:bg-red-700 active:scale-95 transition-all duration-200 border border-red-700 animate-pulse text-sm md:text-base"
            >
              <Square size={18} fill="currentColor" />
              STOP <span className="hidden sm:inline">SIMULATION</span>
            </button>
          )}
        </div>
      </header>

      {/* MAIN CONTENT */}
      {/* Mobile: overflow-y-auto (entire page scrolls). Desktop: overflow-hidden (internal panels scroll) */}
      <main className="flex-1 z-10 min-h-0 flex flex-col lg:flex-row gap-4 md:gap-6 p-4 md:p-6 overflow-y-auto lg:overflow-hidden">
        
        {/* LEFT PANEL — Chatbot */}
        {/* On Mobile: Fixed height (e.g., 500px) so it doesn't collapse. On Desktop: flex-1 */}
        <section className="w-full lg:flex-1 flex flex-col bg-white rounded-3xl border border-gray-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] overflow-hidden relative min-h-[500px] lg:min-h-0 shrink-0">
          <div className="px-5 py-4 md:px-6 md:py-5 border-b border-gray-50 bg-white">
            <h1 className="text-xl md:text-2xl font-bold flex items-center gap-2">
              Friday <Zap size={20} className="text-yellow-500" />
            </h1>
            <p className="text-xs text-gray-400 mt-1">Powered by PulseIQ Neural Engine</p>
          </div>
          <div className="flex-1 bg-gray-50/50 min-h-0 overflow-hidden">
            <ChatBot />
          </div>
        </section>

        {/* RIGHT PANEL — Vitals */}
        {/* On Mobile: w-full. On Desktop: Fixed width 400px. */}
        <aside className="w-full lg:w-[400px] flex flex-col gap-6 shrink-0 pb-10 lg:pb-0">
          <div className="flex-1 bg-white rounded-3xl border border-gray-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] p-5 md:p-6 lg:overflow-y-auto lg:no-scrollbar h-auto lg:h-full">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg md:text-xl font-bold flex items-center gap-2">
                <Activity size={20} /> Biometrics
              </h2>
              <span className="px-3 py-1 bg-black text-white text-[10px] rounded-full uppercase font-bold">
                Live
              </span>
            </div>

            {/* Grid responds to container width */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-3 md:gap-4">
              <VitalStatCard label="Glucose" value={vitals.glucose} unit="mg/dL" thresholds={thresholds.glucose} />
              <VitalStatCard label="Heart Rate" value={vitals.heart_rate} unit="BPM" thresholds={thresholds.heart_rate} />
              <VitalStatCard label="Systolic BP" value={vitals.systolic} unit="mmHg" thresholds={thresholds.systolic} />
              <VitalStatCard label="Diastolic BP" value={vitals.diastolic} unit="mmHg" thresholds={thresholds.diastolic} />
              <VitalStatCard label="Cholesterol" value={vitals.cholesterol} unit="mg/dL" thresholds={thresholds.cholesterol} />
              <VitalStatCard label="SpO₂" value={vitals.spo2} unit="%" thresholds={thresholds.spo2} />
            </div>

            <div className="mt-8 pt-6 border-t border-gray-50 text-center">
              <p className="text-[10px] text-gray-400 uppercase tracking-widest">Last Sync: Just now</p>
            </div>
          </div>
        </aside>
      </main>
    </div>
  );
}