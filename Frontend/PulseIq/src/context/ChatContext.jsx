import { createContext, useContext, useState } from "react";

const ChatContext = createContext();

export function ChatProvider({ children }) {
  const [messages, setMessages] = useState([
    { from: "bot", text: "Hello, I am PulseIQ Guardian. Upload your medical PDF or ask anything." },
  ]);

  const [stopPolling, setStopPolling] = useState(false);

  return (
    <ChatContext.Provider value={{ messages, setMessages, stopPolling, setStopPolling }}>
      {children}
    </ChatContext.Provider>
  );
}

export const useChat = () => useContext(ChatContext);
