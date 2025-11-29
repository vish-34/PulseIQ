import React, { useRef, useEffect, useState } from "react";
import axios from "axios";
import { useActivity } from "../context/ActivityContext";
import { useChat } from "../context/ChatContext";
import { Send, Paperclip, Bot, CheckCircle, FileText, Image as ImageIcon } from "lucide-react";

export default function ChatBot() {
  const { addActivity } = useActivity();

  // ⭐ Global Chat State (persistent)
  const { messages, setMessages, stopPolling, setStopPolling } = useChat();

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);

  const chatEndRef = useRef(null);

  // Auto-scroll on new messages
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);


  // -----------------------------------------------------
  // ⭐ ALERT POLLING (stops after user interacts)
  // -----------------------------------------------------
  useEffect(() => {
    if (stopPolling) return;

    const checkAlerts = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:5000/check_alert");
        if (res.data.alert) {
          setMessages(prev => [...prev, { from: "bot", text: res.data.alert }]);
        }
      } catch (err) {
        console.error("Polling error:", err);
      }
    };

    const id = setInterval(checkAlerts, 3000);
    return () => clearInterval(id);
  }, [stopPolling]);


  // -----------------------------------------------------
  // ⭐ FILE UPLOAD (PDF + IMAGES)
  // -----------------------------------------------------
  const handleFileUpload = async (e) => {
    const uploaded = e.target.files[0];
    if (!uploaded) return;

    setFile(uploaded);

    const isImage = uploaded.type.startsWith("image/");
    const showLabel = isImage
      ? `🖼 Uploaded image: ${uploaded.name}`
      : `📄 Uploaded document: ${uploaded.name}`;

    setMessages(prev => [...prev, { from: "user", text: showLabel }]);
    addActivity(`Uploaded ${isImage ? "an image" : "a PDF"} report`);

    const vitals = window.currentVitals || {};
    const formData = new FormData();
    formData.append("file", uploaded);
    formData.append("vitals", JSON.stringify(vitals));

    setLoading(true);
    setStopPolling(true);

    try {
      const res = await axios.post("http://127.0.0.1:5000/upload_pdf", formData);
      setMessages(prev => [...prev, { from: "bot", text: res.data.response }]);
    } catch {
      setMessages(prev => [...prev, { from: "bot", text: "⚠ File upload failed." }]);
    }

    setLoading(false);
  };


  // -----------------------------------------------------
  // ⭐ SEND MESSAGE 
  // -----------------------------------------------------
  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    setStopPolling(true);

    const userMsg = { from: "user", text: input };
    setMessages(prev => [...prev, userMsg]);

    const vitals = window.currentVitals || {};
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:5000/chat", {
        message: input,
        vitals
      });

      const botText = res.data.response;
      const action = res.data.action;
      const hospital = res.data.hospital;

      if (action === "appointment") {
        addActivity(`Started appointment booking at ${hospital}`);

        setMessages(prev => [
          ...prev,
          { from: "bot", text: botText },
          {
            from: "appointment",
            hospital: hospital || "CityCare Hospital",
            doctorName: res.data.doctor?.name,
            specialty: res.data.doctor?.specialty
          }
        ]);
      } else {
        setMessages(prev => [...prev, { from: "bot", text: botText }]);
      }

    } catch {
      setMessages(prev => [...prev, { from: "bot", text: "⚠ Server unreachable." }]);
    }

    setLoading(false);
  };


  // -----------------------------------------------------
  // ⭐ CONFIRM APPOINTMENT
  // -----------------------------------------------------
  const confirmAppointment = (hospital, doctorName = "Dr. Meera Desai", specialty = "General Physician") => {
    const time = "5pm";

    addActivity(
      `✔ Appointment booked with ${doctorName} (${specialty}) at ${hospital}, time ${time}`
    );

    setMessages(prev => [
      ...prev,
      { from: "user", text: `Confirmed appointment at ${hospital}` },
      { from: "bot", text: `✔ Appointment booked!\n${doctorName} at ${time}` }
    ]);
  };


  // -----------------------------------------------------
  // ⭐ UI (Fully Preserved)
  // -----------------------------------------------------
  return (
    <div className="w-full h-full flex flex-col bg-white relative">

      {/* HEADER */}
      <div className="px-6 py-3 border-b border-gray-100 bg-white flex justify-between items-center shrink-0">
        <div className="flex items-center gap-2 text-xs font-bold uppercase text-gray-400">
          <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
          Live Session
        </div>

        <label className="flex items-center gap-2 px-4 py-2 rounded-full bg-gray-50 border border-gray-200 
          text-xs font-bold uppercase text-black cursor-pointer 
          hover:bg-black hover:text-white transition-all">

          <Paperclip size={14} />
          <span>Upload File</span>

          <input
            type="file"
            accept="application/pdf, image/*"   // ⭐ PDF + IMAGE support
            className="hidden"
            onChange={handleFileUpload}
          />
        </label>
      </div>


      {/* CHAT MESSAGES */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-gray-50/30">
        {messages.map((msg, i) => {
          // Appointment Card
          if (msg.from === "appointment") {
            return (
              <div key={i} className="flex justify-start animate-fade-in-up">
                <div className="bg-white border border-gray-200 shadow-xl rounded-2xl p-5 w-full max-w-sm">
                  <h3 className="text-sm font-bold uppercase tracking-wide mb-2">Confirm Booking</h3>
                  <p className="text-sm text-gray-600 mb-4">
                    Would you like to book at <b>{msg.hospital}</b>?
                  </p>
                  <button
                    onClick={() => confirmAppointment(msg.hospital, msg.doctorName, msg.specialty)}
                    className="w-full py-3 bg-black text-white text-xs rounded-xl hover:bg-gray-800 flex justify-center gap-2"
                  >
                    Confirm Appointment <CheckCircle size={14} />
                  </button>
                </div>
              </div>
            );
          }

          const isBot = msg.from === "bot";

          return (
            <div key={i} className={`flex gap-3 ${isBot ? "justify-start" : "justify-end"} animate-fade-in`}>
              {isBot && (
                <div className="w-8 h-8 rounded-full bg-gray-100 border flex items-center justify-center">
                  <Bot size={16} />
                </div>
              )}

              <div
                className={`max-w-[75%] px-5 py-3 text-sm rounded-2xl shadow-sm ${
                  isBot
                    ? "bg-white text-gray-700 border rounded-tl-none"
                    : "bg-black text-white rounded-tr-none"
                }`}
              >
                {/* File Icon Detection */}
                {msg.text.includes("📄") && <FileText size={16} className="inline mr-2 mb-1" />}
                {msg.text.includes("🖼") && <ImageIcon size={16} className="inline mr-2 mb-1" />}
                {msg.text}
              </div>
            </div>
          );
        })}

        {/* LOADING */}
        {loading && (
          <div className="flex justify-start gap-3">
            <div className="w-8 h-8 rounded-full bg-gray-100 border flex items-center justify-center">
              <Bot size={16} />
            </div>
            <div className="bg-white px-5 py-4 rounded-2xl border flex gap-1">
              <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"></span>
              <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce delay-75"></span>
              <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce delay-150"></span>
            </div>
          </div>
        )}

        <div ref={chatEndRef}></div>
      </div>


      {/* INPUT BAR */}
      <div className="p-4 bg-white border-t">
        <div className="relative flex items-center">
          <input
            type="text"
            placeholder="Type your health query..."
            className="w-full pl-5 pr-14 py-4 bg-gray-50 border rounded-2xl"
            value={input}
            onChange={(e) => { setInput(e.target.value); setStopPolling(true); }}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            disabled={loading}
          />

          <button
            onClick={sendMessage}
            disabled={loading}
            className={`absolute right-2 p-2.5 rounded-xl ${
              loading
                ? "bg-gray-200 text-gray-400 cursor-not-allowed"
                : "bg-black text-white hover:bg-gray-800 hover:scale-105"
            }`}
          >
            <Send size={18} />
          </button>
        </div>
      </div>

    </div>
  );
}
