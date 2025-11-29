import React from "react";
import { useNavigate } from "react-router-dom";
import { LogOut, User } from "lucide-react";

export default function Navbar() {
  const navigate = useNavigate();

  const handleSignOut = () => {
    localStorage.removeItem("pulse_user");
    navigate("/login");
  };

  return (
    <nav className="flex items-center gap-8 md:gap-12">
      
      {/* Brand / Logo */}
      <div 
        className="flex items-center gap-3 cursor-pointer group"
        onClick={() => navigate("/dashboard")}
      >
        <div className="w-8 h-8 md:w-10 md:h-10 rounded-xl bg-gray-50 border border-gray-200 flex items-center justify-center transition-transform duration-300 group-hover:scale-105">
          {/* Ensure PulseIQ.png is transparent or works on white */}
          <img src="/PulseIQ.png" alt="logo" className="w-5 md:w-6 object-contain opacity-80 group-hover:opacity-100 transition-opacity" />
        </div>

        <div className="flex flex-col">
          <h1 className="text-lg font-bold tracking-tight text-black leading-none group-hover:opacity-70 transition-opacity">
            PulseIQ
          </h1>
          <span className="text-[10px] text-gray-400 font-medium tracking-widest uppercase hidden md:block">
            Dashboard
          </span>
        </div>
      </div>

      {/* Navigation Links */}
      <div className="hidden md:flex items-center gap-6">
        <button
          onClick={() => navigate("/profile")}
          className="text-sm font-medium text-gray-500 hover:text-black transition-colors flex items-center gap-2"
        >
          <User size={16} />
          Profile
        </button>
      </div>

      {/* Sign Out (Mobile & Desktop) */}
      <button
        onClick={handleSignOut}
        className="
          flex items-center gap-2
          px-4 py-2 rounded-full
          bg-gray-100 text-black border border-transparent
          text-xs font-bold uppercase tracking-wide
          hover:bg-black hover:text-white hover:border-black
          transition-all duration-300
        "
      >
        <span>Sign Out</span>
        <LogOut size={14} />
      </button>

    </nav>
  );
}