import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowRight, CheckCircle2 } from "lucide-react";

export default function Login() {
  const navigate = useNavigate();

  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const mockUser = {
    email: "test@example.com",
    password: "123456",
  };

  useEffect(() => {
    const user = localStorage.getItem("pulse_user");
    if (user) navigate("/dashboard");
  }, [navigate]);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (isLogin) {
      if (email === mockUser.email && password === mockUser.password) {
        localStorage.setItem("pulse_user", email);
        navigate("/dashboard");
      } else {
        alert("Invalid credentials.");
      }
    } else {
      if (!fullName || !email || !password)
        return alert("Fill all fields.");
      if (password !== confirmPassword)
        return alert("Passwords do not match.");

      alert("Account created! Login now.");
      setIsLogin(true);
      setPassword("");
      setConfirmPassword("");
    }
  };

  return (
    <div className="min-h-screen w-full bg-white flex flex-col items-center justify-center relative selection:bg-black selection:text-white overflow-hidden p-6">
      
      {/* 1. Subtle Grain Texture (Consistent with Landing) */}
      <div className="absolute inset-0 pointer-events-none opacity-[0.03]"
           style={{ backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")` }}>
      </div>

      {/* 2. Brand Header (Top Center) */}
      <div className="absolute top-8 md:top-12 animate-fade-in-down">
        <p className="font-semibold tracking-tight text-sm uppercase text-gray-400 cursor-pointer" onClick={() => navigate("/")}>
          PulseIQ Systems
        </p>
      </div>

      {/* 3. Main Card Container */}
      <div className="w-full max-w-[400px] z-10 animate-fade-in-up">
        
        {/* Header Section */}
        <div className="mb-10 text-center">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tighter text-black mb-3">
            {isLogin ? "Welcome back." : "Join us."}
          </h1>
          <p className="text-gray-400 text-sm">
            {isLogin 
              ? "Access your personal health monitor." 
              : "Start your journey to simpler health."}
          </p>
        </div>

        {/* Form */}
        <form className="space-y-4" onSubmit={handleSubmit}>

          {!isLogin && (
            <div className="group">
              <input
                type="text"
                placeholder="Full Name"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="
                  w-full px-5 py-4 rounded-xl 
                  bg-gray-50 border-2 border-transparent 
                  text-black placeholder-gray-400 font-medium
                  focus:outline-none focus:bg-white focus:border-black/10
                  transition-all duration-300
                "
              />
            </div>
          )}

          <div className="group">
            <input
              type="email"
              placeholder="Email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="
                w-full px-5 py-4 rounded-xl 
                bg-gray-50 border-2 border-transparent 
                text-black placeholder-gray-400 font-medium
                focus:outline-none focus:bg-white focus:border-black/10
                transition-all duration-300
              "
            />
          </div>

          <div className="group">
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="
                w-full px-5 py-4 rounded-xl 
                bg-gray-50 border-2 border-transparent 
                text-black placeholder-gray-400 font-medium
                focus:outline-none focus:bg-white focus:border-black/10
                transition-all duration-300
              "
            />
          </div>

          {!isLogin && (
            <div className="group">
              <input
                type="password"
                placeholder="Confirm Password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="
                  w-full px-5 py-4 rounded-xl 
                  bg-gray-50 border-2 border-transparent 
                  text-black placeholder-gray-400 font-medium
                  focus:outline-none focus:bg-white focus:border-black/10
                  transition-all duration-300
                "
              />
            </div>
          )}

          {/* Action Button */}
          <button
            type="submit"
            className="
              group relative w-full mt-6
              flex items-center justify-between
              px-6 py-4
              bg-black text-white
              rounded-full
              shadow-xl shadow-black/5
              hover:shadow-2xl hover:shadow-black/10
              hover:scale-[1.02]
              transition-all duration-300 ease-out
            "
          >
            <span className="text-base font-medium">
              {isLogin ? "Sign In" : "Create Account"}
            </span>
            
            {/* Animated Icon Circle */}
            <div className="
              flex items-center justify-center
              w-8 h-8
              bg-white rounded-full 
              text-black
              transition-transform duration-500 
              group-hover:rotate-[-45deg]
            ">
              <ArrowRight size={16} />
            </div>
          </button>
        </form>

        {/* Toggle Login/Signup */}
        <div className="mt-8 text-center">
          <p className="text-sm text-gray-400">
            {isLogin ? "New to PulseIQ? " : "Already have an account? "}
            <button
              onClick={() => setIsLogin(!isLogin)}
              className="text-black font-semibold underline underline-offset-4 decoration-1 decoration-gray-300 hover:decoration-black transition-all"
            >
              {isLogin ? "Register here" : "Login here"}
            </button>
          </p>
        </div>

      </div>

      {/* Minimal Footer */}
      <div className="absolute bottom-6 text-[10px] text-gray-300 font-medium tracking-widest uppercase animate-fade-in">
        Secure Encryption • HIPAA Compliant
      </div>

    </div>
  );
}