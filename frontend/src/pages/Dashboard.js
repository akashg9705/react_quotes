import { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api";

/* ── Toast System ── */
let toastId = 0;

function ToastContainer({ toasts, onRemove }) {
  return (
    <div className="toast-container">
      {toasts.map((t) => (
        <div key={t.id} className={`toast toast-${t.type} ${t.exit ? "toast-exit" : ""}`}>
          <span className="toast-icon">
            {t.type === "success" ? "✓" : t.type === "error" ? "✕" : "ℹ"}
          </span>
          <span className="toast-message">{t.message}</span>
        </div>
      ))}
    </div>
  );
}

function Dashboard() {
  const [email, setEmail] = useState("");
  const [data, setData] = useState([]);
  const [stats, setStats] = useState({ total: 0, active: 0, inactive: 0 });
  const [quote, setQuote] = useState(null);
  const [quoteLoading, setQuoteLoading] = useState(true);
  const [toasts, setToasts] = useState([]);
  const [actionLoading, setActionLoading] = useState("");
  const navigate = useNavigate();

  const addToast = useCallback((message, type = "success") => {
    const id = ++toastId;
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts((prev) =>
        prev.map((t) => (t.id === id ? { ...t, exit: true } : t))
      );
      setTimeout(() => {
        setToasts((prev) => prev.filter((t) => t.id !== id));
      }, 300);
    }, 3000);
  }, []);

  const fetchSubscribers = useCallback(async () => {
    try {
      const res = await API.get("/subscribers");
      setData(res.data.data);
    } catch {
      addToast("Session expired. Please login again.", "error");
      localStorage.removeItem("token");
      navigate("/");
    }
  }, [addToast, navigate]);

  const fetchStats = useCallback(async () => {
    try {
      const res = await API.get("/stats");
      setStats(res.data);
    } catch {
      // silently fail
    }
  }, []);

  const fetchQuote = useCallback(async () => {
    setQuoteLoading(true);
    try {
      const res = await API.get("/quote");
      setQuote(res.data);
    } catch {
      setQuote({
        quote: "The only way to do great work is to love what you do.",
        author: "Steve Jobs",
      });
    } finally {
      setQuoteLoading(false);
    }
  }, []);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/");
      return;
    }
    fetchSubscribers();
    fetchStats();
    fetchQuote();
  }, [fetchSubscribers, fetchStats, fetchQuote, navigate]);

  const subscribe = async () => {
    if (!email.trim()) {
      addToast("Please enter an email address.", "error");
      return;
    }
    setActionLoading("subscribe");
    try {
      const res = await API.post("/subscribe", { email });
      addToast(res.data.status === "Subscribed"
        ? `${email} subscribed successfully!`
        : `${email} already exists.`, res.data.status === "Subscribed" ? "success" : "info");
      setEmail("");
      fetchSubscribers();
      fetchStats();
    } catch {
      addToast("Failed to subscribe.", "error");
    } finally {
      setActionLoading("");
    }
  };

  const unsubscribe = async () => {
    if (!email.trim()) {
      addToast("Please enter an email address.", "error");
      return;
    }
    setActionLoading("unsubscribe");
    try {
      await API.post("/unsubscribe", { email });
      addToast(`${email} unsubscribed.`, "info");
      setEmail("");
      fetchSubscribers();
      fetchStats();
    } catch {
      addToast("Failed to unsubscribe.", "error");
    } finally {
      setActionLoading("");
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div className="dashboard-layout">
      {/* Toast Notifications */}
      <ToastContainer toasts={toasts} />

      {/* ── Top Navbar ── */}
      <nav className="top-nav">
        <div className="nav-brand">
          <div className="nav-brand-icon">✦</div>
          <h1>QuoteSaaS</h1>
        </div>
        <div className="nav-right">
          <span className="nav-user">Dashboard</span>
          <button className="btn btn-ghost" onClick={logout}>
            ↗ Logout
          </button>
        </div>
      </nav>

      {/* ── Main Content ── */}
      <main className="dashboard-content">
        {/* Stats Cards */}
        <div className="stats-grid stagger-children">
          <div className="stat-card total animate-fade-in-up">
            <div className="stat-icon">📊</div>
            <div className="stat-label">Total Subscribers</div>
            <div className="stat-value">{stats.total}</div>
          </div>
          <div className="stat-card active animate-fade-in-up">
            <div className="stat-icon">✅</div>
            <div className="stat-label">Active</div>
            <div className="stat-value">{stats.active}</div>
          </div>
          <div className="stat-card inactive animate-fade-in-up">
            <div className="stat-icon">⛔</div>
            <div className="stat-label">Unsubscribed</div>
            <div className="stat-value">{stats.inactive}</div>
          </div>
        </div>

        {/* Quote of the Day */}
        <div className="quote-card">
          <div className="quote-header">
            <span className="quote-header-icon">💡</span>
            <h3>Quote of the Day</h3>
          </div>
          {quoteLoading ? (
            <div className="quote-loading">
              <span className="spinner" style={{ borderTopColor: "var(--warning)" }} />
              Loading quote...
            </div>
          ) : quote ? (
            <>
              <p className="quote-text">{quote.quote}</p>
              <p className="quote-author">— {quote.author}</p>
            </>
          ) : null}
        </div>

        {/* Manage Subscribers */}
        <div className="section-card">
          <div className="section-header">
            <div className="section-title">
              <span>📬</span>
              Manage Subscribers
            </div>
          </div>
          <div className="section-body">
            <div className="subscriber-form">
              <input
                id="subscriber-email"
                type="email"
                placeholder="Enter subscriber email..."
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && subscribe()}
              />
              <button
                id="subscribe-btn"
                className="btn btn-success"
                onClick={subscribe}
                disabled={!!actionLoading}
              >
                {actionLoading === "subscribe" ? (
                  <span className="spinner" />
                ) : (
                  "+ Subscribe"
                )}
              </button>
              <button
                id="unsubscribe-btn"
                className="btn btn-danger"
                onClick={unsubscribe}
                disabled={!!actionLoading}
              >
                {actionLoading === "unsubscribe" ? (
                  <span className="spinner" />
                ) : (
                  "Unsubscribe"
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Subscriber Table */}
        <div className="section-card">
          <div className="section-header">
            <div className="section-title">
              <span>👥</span>
              Subscriber List
            </div>
            <span style={{ color: "var(--text-muted)", fontSize: "0.8rem" }}>
              {data.length} {data.length === 1 ? "subscriber" : "subscribers"}
            </span>
          </div>
          <div className="section-body" style={{ padding: data.length ? 0 : undefined }}>
            {data.length === 0 ? (
              <div className="empty-state">
                <div className="empty-state-icon">📭</div>
                <p>No subscribers yet. Add your first one above!</p>
              </div>
            ) : (
              <table className="subscriber-table">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Email Address</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {data.map((item, i) => (
                    <tr key={i} style={{ animationDelay: `${i * 50}ms` }}>
                      <td style={{ color: "var(--text-muted)", fontFamily: "var(--font-mono)", fontSize: "0.8rem" }}>
                        {String(i + 1).padStart(2, "0")}
                      </td>
                      <td>{item[0]}</td>
                      <td>
                        <span className={`badge ${item[1] === "active" ? "badge-active" : "badge-inactive"}`}>
                          <span className="badge-dot" />
                          {item[1]}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default Dashboard;