import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await register({ email, password, fullName });
      navigate("/");
    } catch (err) {
      const detail = err.response?.data?.detail;
      let message = "Registration failed.";
      if (typeof detail === "string") {
        message = detail;
      } else if (Array.isArray(detail)) {
        // FastAPI/Pydantic-style validation errors: array of { msg, loc, ... }
        message = detail.map((d) => d.msg || JSON.stringify(d)).join(" ");
      } else if (detail && typeof detail === "object") {
        message = detail.msg || JSON.stringify(detail);
      }
      setError(message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 px-4 font-sans">
      <div className="w-full max-w-sm bg-white rounded-2xl p-8 shadow-sm border border-slate-200">
        <div className="inline-block px-3 py-1 rounded-full bg-orange-50 text-orange-600 text-xs font-bold tracking-wider border border-orange-200 mb-4">
          ⚡ AI JOB MATCHER
        </div>

        <h1 className="text-2xl font-semibold text-slate-900 mb-1">Create your account</h1>
        <p className="text-slate-500 text-sm mb-6">Start matching with AI-recommended jobs.</p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-slate-600 mb-1">Full name</label>
            <input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              className="w-full rounded-lg bg-white border border-slate-300 px-3 py-2 text-slate-900 outline-none focus:border-blue-500 transition-colors"
              placeholder="Jane Doe"
            />
          </div>
          <div>
            <label className="block text-sm text-slate-600 mb-1">Email</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-lg bg-white border border-slate-300 px-3 py-2 text-slate-900 outline-none focus:border-blue-500 transition-colors"
              placeholder="you@example.com"
            />
          </div>
          <div>
            <label className="block text-sm text-slate-600 mb-1">Password</label>
            <input
              type="password"
              required
              minLength={8}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-lg bg-white border border-slate-300 px-3 py-2 text-slate-900 outline-none focus:border-blue-500 transition-colors"
              placeholder="At least 8 characters"
            />
          </div>

          {error && <p className="text-red-500 text-sm">{error}</p>}

          <button
            type="submit"
            disabled={submitting}
            className="w-full rounded-lg bg-blue-600 hover:bg-blue-700 disabled:opacity-60 text-white font-medium py-2 transition-colors"
          >
            {submitting ? "Creating account..." : "Sign up"}
          </button>
        </form>

        <p className="text-slate-500 text-sm mt-6 text-center">
          Already have an account?{" "}
          <Link to="/login" className="text-orange-500 hover:text-orange-600 font-medium">
            Log in
          </Link>
        </p>
      </div>
    </div>
  );
}