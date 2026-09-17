import { useNavigate } from "react-router-dom";
import "../styles/Sidebar.css";
import Logo from "../assets/logo-icon.svg.svg";
import DocumentsIcon from "../assets/documents-icon.svg";
import ChatIcon from "../assets/chat-icon.svg";
import HelpIcon from "../assets/help-icon.svg";
import credit from "../assets/credits-icon.svg";
import UpArrow from "../assets/upArrow.svg";
import { useAuth } from "../context/AuthContext";

function Sidebar({ activePage }) {
  const { user, profile } = useAuth()
  const navigate = useNavigate();

   const displayName    = profile?.name || user?.email?.split('@')[0] || 'User'
  const creditsLeft    = profile?.credits_remaining ?? 0
  const avatarInitial  = displayName[0].toUpperCase()

  const menuItems = [
    {
      id: "documents",
      label: "Documents",
      icon: DocumentsIcon,
      path: "/documents",
    },
    { id: "chats", label: "Chats", icon: ChatIcon, path: "/chats" },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <img src={Logo} alt="DocQ Logo" className="logo-img" />
          <span className="logo-text">docAnalyzer.ai</span>
        </div>
      </div>

      <nav className="sidebar-menu">
        {menuItems.map((item) => (
          <button
            key={item.id}
            className={`sidebar-menu-item ${activePage === item.id ? "active" : ""}`}
            onClick={() => navigate(item.path)}
          >
            <img src={item.icon} alt={item.label} className="menu-icon" />
            <span>{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
         {/* Help button — navigates to /help */}
        <button
          className={`sidebar-menu-item help-btn ${activePage === "help" ? "active" : ""}`}
          onClick={() => navigate("/help")}
        >
          <img src={HelpIcon} alt="Help" className="menu-icon" />
          <span>Help</span>
        </button>
        {/* ── Clicking the profile section opens Account settings ── */}
        <button
          className="user-profile"
          onClick={() => navigate("/account")}
          title="Account settings"
        >
          <div className="user-avatar">{avatarInitial}</div>
          <div className="user-info">
            <p className="user-name">{displayName}</p>
            <div className="user-credits">
              <img className="credit-icon" src={credit} alt="Credit" />
              <span>{creditsLeft}</span>
            </div>
          </div>
          <img src={UpArrow} alt="open" className="profile-arrow" />
        </button>
      </div>
    </aside>
  );
}

export default Sidebar;
