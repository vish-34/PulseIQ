import React from "react";
import { useNavigate } from "react-router-dom";
import { ArrowRight } from "lucide-react";

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen w-full bg-white flex flex-col items-center justify-center relative selection:bg-black selection:text-white overflow-hidden">
      
      {/* 1. Subtle Grain Texture (Optional: Adds tactile feel to the white) */}
      <div className="absolute inset-0 pointer-events-none opacity-[0.02]"
           style={{ backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")` }}>
      </div>

      {/* 2. Minimal Brand Identifier (Top Center) */}
      <div className="absolute top-8 md:top-12 animate-fade-in-down">
        <p className="font-semibold tracking-tight text-sm uppercase text-gray-400">
          PulseIQ Systems
        </p>
      </div>

      {/* 3. Main Content - The "Hero" */}
      <div className="z-10 flex flex-col items-center gap-10 md:gap-14 animate-fade-in-up">
        
        {/* Massive Typography - Stark Black on White */}
        <img src="PulseIQ.png" alt="" className="w-[15em]"/>
        <h1 className="text-2xl md:text-8xl font-bold tracking-tighter text-black text-center leading-[0.9]">
          Pulse.
          <span className="text-gray-300">IQ</span>
        </h1>

        {/* 4. The "Get Started" Button */}
        <button
          onClick={() => navigate("/login")}
          className="
            group relative
            flex items-center justify-between
            pl-8 pr-6 py-4 md:py-5
            bg-black text-white
            rounded-full
            w-[200px] hover:w-[260px]
            transition-all duration-500 ease-in-out
          "
        >
          <span className="text-lg font-medium whitespace-nowrap">
            Get Started
          </span>
          
          {/* Animated Circle Icon */}
          <div className="
            flex items-center justify-center
            w-8 h-8 md:w-10 md:h-10 
            bg-white rounded-full 
            text-black
            transition-transform duration-500 
            group-hover:rotate-[-45deg] group-hover:scale-110
          ">
            <ArrowRight size={18} />
          </div>
        </button>
      </div>

      {/* 5. Minimal Footer */}
      <div className="absolute bottom-8 text-xs text-gray-400 font-medium tracking-wide animate-fade-in">
        © 2024 PULSEIQ
      </div>
    </div>
  );
}