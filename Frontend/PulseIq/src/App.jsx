import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  Outlet,
} from "react-router-dom";

import LandingPage from "./Pages/LandingPage";
import Login from "./Pages/Login";
import Dashboard from "./Pages/Dashboard";
import Profile from "./Pages/Profile";

// ⭐ NEW — Import global providers (to stop refresh issues)
import { ChatProvider } from "./context/ChatContext";
import { ActivityProvider } from "./context/ActivityContext";

// Protected Route
function ProtectedRoute() {
  const user = localStorage.getItem("pulse_user");

  if (!user) return <Navigate to="/login" replace />;

  return <Outlet />;
}

// Prevent logged-in users from visiting / and /login
function PublicRoute() {
  const user = localStorage.getItem("pulse_user");

  if (user) return <Navigate to="/dashboard" replace />;

  return <Outlet />;
}

// Layout that keeps Dashboard & Profile mounted
function AppLayout() {
  return (
    <div className="w-full h-full">
      <Outlet />
    </div>
  );
}

export default function App() {
  return (
    // ⭐ Wrapping the ENTIRE app with providers prevents remounting
    <ActivityProvider>
      <ChatProvider>
        <Router>
          <Routes>
            {/* Public Routes */}
            <Route element={<PublicRoute />}>
              <Route path="/" element={<LandingPage />} />
              <Route path="/login" element={<Login />} />
            </Route>

            {/* Protected Routes */}
            <Route element={<ProtectedRoute />}>
              <Route element={<AppLayout />}>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/profile" element={<Profile />} />
              </Route>
            </Route>

            {/* Redirect unknown routes */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Router>
      </ChatProvider>
    </ActivityProvider>
  );
}
