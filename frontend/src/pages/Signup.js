import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api";

function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const getPasswordStrength = (pwd) => {
    if (!pwd) return { level: 0, text: "" };
    let score = 0;
    if (pwd.length >= 6) score++;
    if (pwd.length >= 10) score++;
    if (/[A-Z]/.test(pwd)) score++;
    if (/[0-9]/.test(pwd)) score++;
    if (/[^A-Za-z0-9]/.test(pwd)) score++;

    if (score <= 1) return { level: 1, text: "Weak" };
    if (score <= 3) return { level: 2, text: "Medium" };
    return { level: 3, text: "Strong" };
  };

  const strength = getPasswordStrength(password);

  const handleSignup = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await API.post("/signup", { email, password });
      setSuccess(true);
      setTimeout(() => navigate("/"), 1500);
    } catch (err) {
      setError(
        err.response?.data?.detail || "Signup failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      {/* Floating orbs */}
      <div className="auth-orb auth-orb-1" />
      <div className="auth-orb auth-orb-2" />
      <div className="auth-orb auth-orb-3" />

      <div className="auth-card">
        {/* Brand */}
        <div className="auth-brand">
          <div className="auth-brand-icon">✦</div>
          <h1>QuoteSaaS</h1>
          <p>Create your account to get started</p>
        </div>

        {/* Success message */}
        {success && (
          <div
            style={{
              background: "rgba(16, 185, 129, 0.1)",
              border: "1px solid rgba(16, 185, 129, 0.3)",
              borderRadius: "var(--radius-sm)",
              padding: "10px 14px",
              color: "#10b981",
              fontSize: "0.85rem",
              marginBottom: "16px",
              animation: "fadeInUp 0.3s var(--ease-out) both",
            }}
          >
            ✓ Account created! Redirecting to login...
          </div>
        )}

        {/* Error */}
        {error && <div className="auth-error">{error}</div>}

        {/* Form */}
        <form className="auth-form" onSubmit={handleSignup}>
          <div className="input-group">
            <input
              id="signup-email"
              className="auth-input"
              type="email"
              placeholder="Email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoFocus
            />
            <span className="input-icon">✉</span>
          </div>

          <div className="input-group">
            <input
              id="signup-password"
              className="auth-input"
              type="password"
              placeholder="Create a password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <span className="input-icon">🔒</span>
          </div>

          {/* Password strength indicator */}
          {password && (
            <>
              <div className="password-strength">
                {[1, 2, 3].map((i) => (
                  <div
                    key={i}
                    className={`password-strength-bar ${
                      i <= strength.level
                        ? strength.level === 1
                          ? "weak"
                          : strength.level === 2
                          ? "medium"
                          : "strong"
                        : ""
                    }`}
                  />
                ))}
              </div>
              <span
                className="password-strength-text"
                style={{
                  color:
                    strength.level === 1
                      ? "var(--danger)"
                      : strength.level === 2
                      ? "var(--warning)"
                      : "var(--success)",
                }}
              >
                {strength.text}
              </span>
            </>
          )}

          <button
            id="signup-submit"
            className="btn btn-primary btn-full"
            type="submit"
            disabled={loading || success}
          >
            {loading ? (
              <>
                <span className="spinner" />
                Creating account...
              </>
            ) : success ? (
              "✓ Created!"
            ) : (
              "Create Account"
            )}
          </button>
        </form>

        {/* Footer */}
        <div className="auth-footer">
          <p>
            Already have an account?{" "}
            <span className="auth-link" onClick={() => navigate("/")}>
              Sign in
            </span>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Signup;