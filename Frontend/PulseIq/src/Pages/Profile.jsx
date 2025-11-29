import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom"; 
import useLiveVitals from "../components/useLiveVitals";
import Navbar from "../components/Navbar"; 
import { 
  User, Mail, Droplet, Phone, Clock, 
  Edit2, Save, X, MapPin, Activity, 
  Settings, Shield, ArrowLeft 
} from "lucide-react";

export default function Profile() {
  const navigate = useNavigate(); 
  const vitals = useLiveVitals();
  const [activity, setActivity] = useState([]);

  // ----------------------------------------------------------
  // ⭐ PROFILE EDIT STATE
  // ----------------------------------------------------------
  const [profile, setProfile] = useState({
    name: "Vishal Borana",
    email: "vishal@example.com",
    blood: "O+",
    phone: "+91 98765 43210",
    age: "21 Years",
  });

  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState(profile);

  const handleEdit = () => {
    setEditData(profile);
    setIsEditing(true);
  };

  const saveProfile = () => {
    setProfile(editData);
    setIsEditing(false);
  };

  // ----------------------------------------------------------
  // 🔥 Fetch activity.json from backend
  // ----------------------------------------------------------
  const fetchActivity = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/get_activity");
      const data = await res.json();
      setActivity(data);
    } catch (err) {
      console.error("Failed to load activity:", err);
    }
  };

  useEffect(() => {
    fetchActivity();
    const interval = setInterval(fetchActivity, 3000);
    return () => clearInterval(interval);
  }, []);

  // 🌍 Open Google Maps
  const openMap = () => {
    const hospital = "CityCare Hospital";
    // Fixed URL structure for Google Maps Search
    window.open(
      `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(hospital)}`,
      "_blank"
    );
  };

  return (
    <div className="min-h-screen w-full bg-white text-black flex flex-col relative selection:bg-black selection:text-white font-sans overflow-x-hidden">

      {/* 1. Subtle Grain Texture */}
      <div
        className="fixed inset-0 pointer-events-none opacity-[0.03] z-0"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
        }}
      ></div>

      {/* 2. HEADER */}
      <header className="z-20 shrink-0 flex items-center justify-between px-4 py-4 md:px-8 md:py-5 border-b border-gray-100 bg-white/80 backdrop-blur-md sticky top-0">
        
        {/* Left Side: Back Button + Navbar */}
        <div className="flex items-center gap-4 md:gap-6">
            <button 
                onClick={() => navigate("/dashboard")}
                className="
                    group flex items-center justify-center 
                    w-10 h-10 rounded-xl 
                    bg-gray-50 border border-gray-200 
                    text-gray-500 hover:text-black hover:border-black 
                    hover:bg-white hover:shadow-md 
                    transition-all duration-300
                "
                title="Back to Dashboard"
            >
                <ArrowLeft size={20} className="group-hover:-translate-x-0.5 transition-transform" />
            </button>
            
            <Navbar />
        </div>

        <div className="hidden md:flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-green-500"></span>
            <span className="text-xs font-bold uppercase tracking-widest text-gray-400">Profile Settings</span>
        </div>
      </header>

      {/* 3. MAIN CONTENT */}
      {/* Responsive padding: p-4 on mobile, p-10 on desktop */}
      <main className="relative z-10 flex-1 overflow-y-auto p-4 md:p-10">
        <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6 md:gap-8">

          {/* --------------------------------------------------
              LEFT — PROFILE CARD
          -------------------------------------------------- */}
          {/* h-fit ensures it doesn't stretch weirdly on desktop */}
          <div className="bg-white rounded-3xl border border-gray-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] p-6 md:p-8 flex flex-col items-center h-fit w-full">
            
            {/* Avatar - Responsive size */}
            <div className="relative group mb-6">
                <div className="w-24 h-24 md:w-32 md:h-32 rounded-full p-1 border-2 border-gray-100 overflow-hidden">
                    <img
                        src="https://i.pinimg.com/736x/be/09/81/be0981c4652679ab4db74f764d405132.jpg"
                        alt="User"
                        className="w-full h-full rounded-full object-cover transition-all duration-500"
                    />
                </div>
                {!isEditing && (
                    <button onClick={handleEdit} className="absolute bottom-0 right-0 p-2 bg-black text-white rounded-full hover:scale-110 transition shadow-lg">
                        <Edit2 size={14} />
                    </button>
                )}
            </div>

            {!isEditing ? (
              <>
                <h1 className="text-xl md:text-2xl font-bold tracking-tight text-black text-center">{profile.name}</h1>
                <p className="text-gray-400 text-xs font-medium uppercase tracking-wider mt-1 text-center">
                  BSc Computer Science • Developer
                </p>

                <div className="mt-8 w-full space-y-3 md:space-y-4">
                  {[
                    { icon: Mail, label: "Email", value: profile.email },
                    { icon: Droplet, label: "Blood Type", value: profile.blood },
                    { icon: Phone, label: "Phone", value: profile.phone },
                    { icon: Clock, label: "Age", value: profile.age },
                  ].map((item, i) => (
                    <div key={i} className="flex items-center justify-between p-3 rounded-2xl bg-gray-50 border border-gray-100 group hover:border-black/10 transition-colors w-full">
                      <div className="flex items-center gap-3 overflow-hidden">
                          <div className="shrink-0 p-2 bg-white rounded-full border border-gray-200 text-gray-400 group-hover:text-black transition-colors">
                             <item.icon size={14} />
                          </div>
                          <span className="text-xs font-medium text-gray-500 uppercase tracking-wide truncate">{item.label}</span>
                      </div>
                      <span className="text-sm font-semibold text-black truncate ml-2">{item.value}</span>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              /* ✏ EDIT MODE */
              <div className="w-full space-y-4 animate-fade-in">
                <div className="flex justify-between items-center mb-4">
                    <h2 className="text-lg font-bold">Edit Details</h2>
                    <span className="text-xs text-gray-400">Update your info</span>
                </div>

                {[
                  { key: "name", label: "Name", icon: User },
                  { key: "email", label: "Email", icon: Mail },
                  { key: "blood", label: "Blood Type", icon: Droplet },
                  { key: "phone", label: "Phone", icon: Phone },
                  { key: "age", label: "Age", icon: Clock },
                ].map((field, i) => (
                  <div key={i} className="group">
                    <label className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-1 block">{field.label}</label>
                    <div className="relative">
                        <input
                            type="text"
                            className="w-full pl-10 pr-4 py-3 rounded-xl bg-gray-50 border border-transparent focus:bg-white focus:border-black/10 focus:outline-none transition-all text-sm font-medium"
                            value={editData[field.key]}
                            onChange={(e) =>
                                setEditData({ ...editData, [field.key]: e.target.value })
                            }
                        />
                        <field.icon size={14} className="absolute left-3.5 top-3.5 text-gray-400" />
                    </div>
                  </div>
                ))}

                <div className="grid grid-cols-2 gap-3 mt-6">
                  <button
                    className="flex items-center justify-center gap-2 py-3 bg-black text-white rounded-xl font-bold text-sm hover:scale-[1.02] transition shadow-lg shadow-black/10"
                    onClick={saveProfile}
                  >
                    <Save size={16} /> Save
                  </button>
                  <button
                    className="flex items-center justify-center gap-2 py-3 bg-gray-100 text-gray-600 rounded-xl font-bold text-sm hover:bg-gray-200 transition"
                    onClick={() => setIsEditing(false)}
                  >
                    <X size={16} /> Cancel
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* --------------------------------------------------
              RIGHT — OVERVIEW + ACTIVITY
          -------------------------------------------------- */}
          <div className="lg:col-span-2 space-y-6 md:space-y-8">

            {/* HEALTH OVERVIEW */}
            <div className="bg-white rounded-3xl border border-gray-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] p-6 md:p-8">
              <div className="flex items-center justify-between mb-6">
                 <h2 className="text-lg font-bold tracking-tight flex items-center gap-2">
                    <Activity size={20} className="text-black" /> Health Overview
                 </h2>
                 <span className="text-[10px] bg-black text-white px-3 py-1 rounded-full font-bold uppercase tracking-wide">Live</span>
              </div>

              {/* Grid responsive: 2 cols on mobile, 3 on desktop */}
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3 md:gap-4">
                {[
                  { label: "Heart Rate", value: vitals.heart_rate, unit: "BPM" },
                  { label: "SpO₂", value: vitals.spo2, unit: "%" },
                  { label: "BMI", value: vitals.bmi, unit: "" },
                  { label: "Systolic BP", value: vitals.systolic, unit: "mmHg" },
                  { label: "Diastolic BP", value: vitals.diastolic, unit: "mmHg" },
                  { label: "Cholesterol", value: vitals.cholesterol, unit: "mg/dL" },
                ].map((v, i) => (
                  <div
                    key={i}
                    className="flex flex-col p-4 md:p-5 bg-gray-50 rounded-2xl border border-transparent hover:bg-white hover:border-gray-100 hover:shadow-md transition-all duration-300"
                  >
                    <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider truncate">{v.label}</span>
                    <div className="text-xl md:text-2xl mt-1 font-bold text-black tracking-tight flex items-baseline flex-wrap">
                      {v.value} <span className="text-xs md:text-sm text-gray-400 font-medium ml-1">{v.unit}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* ACTIVITY */}
            <div className="bg-white rounded-3xl border border-gray-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] p-6 md:p-8">
              <h2 className="text-lg font-bold tracking-tight mb-6 flex items-center gap-2">
                  <Clock size={20} /> Recent Activity
              </h2>

              <div className="space-y-6 pl-2">
                {activity.length === 0 && (
                  <p className="text-gray-400 text-sm italic">No recent activity detected...</p>
                )}

                {activity.map((item, i) => {
                  const isAppointment = item.label.includes("Appointment booked");

                  return (
                    <div key={i} className="relative pl-6 border-l-2 border-gray-100 last:border-0 pb-6">
                      {/* Timeline Dot */}
                      <div className={`absolute -left-[9px] top-0 w-4 h-4 rounded-full border-2 border-white ${isAppointment ? 'bg-black' : 'bg-gray-300'}`}></div>
                      
                      <div className="flex flex-col gap-1">
                        <p
                          className="text-sm font-medium text-black"
                          dangerouslySetInnerHTML={{ __html: item.label }}
                        />
                        <span className="text-xs text-gray-400">{item.time}</span>

                        {isAppointment && (
                          <button
                            onClick={openMap}
                            className="mt-3 w-fit flex items-center gap-2 px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-xs font-bold uppercase tracking-wide hover:bg-black hover:text-white transition-all duration-300"
                          >
                            <MapPin size={12} /> Open Map
                          </button>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* SETTINGS */}
            <div className="bg-white rounded-3xl border border-gray-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] p-6 md:p-8">
              <h2 className="text-lg font-bold tracking-tight mb-6 flex items-center gap-2">
                  <Settings size={20} /> Preferences
              </h2>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {[
                  { label: "Two-Factor Auth", icon: Shield },
                  { label: "Emergency Contacts", icon: Phone },
                  { label: "Insurance Auto-Sync", icon: Activity },
                  { label: "Crash Detection", icon: Activity }, 
                  { label: "Cloud Backups", icon: Droplet },
                ].map((item, i) => (
                  <div
                    key={i}
                    className="flex items-center justify-between p-4 rounded-2xl border border-gray-100 bg-gray-50/50 hover:bg-white hover:shadow-sm transition-all"
                  >
                    <div className="flex items-center gap-3 overflow-hidden">
                        <div className="shrink-0 p-2 bg-white rounded-lg border border-gray-200 text-gray-400">
                            <item.icon size={16} />
                        </div>
                        <span className="text-sm font-medium text-gray-700 truncate">{item.label}</span>
                    </div>
                    {/* Custom Toggle */}
                    <label className="relative inline-flex items-center cursor-pointer shrink-0 ml-2">
                        <input type="checkbox" className="sr-only peer" defaultChecked={i > 2} />
                        <div className="w-9 h-5 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-black"></div>
                    </label>
                  </div>
                ))}
              </div>
            </div>

          </div>
        </div>
      </main>
    </div>
  );
}