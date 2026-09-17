import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SignIn from "./pages/SignIn";
import SignUp from "./pages/SignUp";
import Documents from "./pages/Documents";
import Chats from "./pages/Chats";
import ChatConversation from "./pages/ChatConversation";
import Account from "./pages/Account";
import Help from "./pages/Help";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<SignIn />} />
          <Route path="/signup" element={<SignUp />} />

          {/* //Protected routes */}
          <Route element={<ProtectedRoute />}>
            <Route path="/documents" element={<Documents />} />
            <Route path="/chats" element={<Chats />} />
            <Route path="/chat/:chatId" element={<ChatConversation />} />
            <Route path="/account" element={<Account />} />
            <Route path="/help" element={<Help />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}
