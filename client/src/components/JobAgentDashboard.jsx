import { useState } from "react";
import {
  uploadResume,
  getResumeAnalysis,
  searchJobs,
  getRecommendedJobs,
} from "../services/jobAgent";
import { useAuth } from "../context/AuthContext";

export default function JobAgentDashboard() {
  const { user, logout } = useAuth();
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [statusText, setStatusText] = useState("");

  // Application Data States
  const [resumeId, setResumeId] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [jobs, setJobs] = useState([]);

  // Step 1 & 2: Handle Upload -> Fetch Analysis & Search Initial Jobs
  const handleFileUpload = async (selectedFile) => {
    if (!selectedFile) return;
    setFile(selectedFile);
    setLoading(true);

    try {
      setStatusText("Uploading resume to AI Engine...");
      const uploadRes = await uploadResume(selectedFile);
      const id = uploadRes.resume_id || uploadRes.id;
      setResumeId(id);

      setStatusText("Analyzing skills and parsing experience...");
      const analysisRes = await getResumeAnalysis(id);
      setAnalysis(analysisRes);

      setStatusText("Searching best matched jobs based on analyzed skills...");
      const searchRes = await searchJobs(id);

      const initialJobs = Array.isArray(searchRes)
        ? searchRes
        : searchRes.jobs || searchRes.data || [];
      setJobs(initialJobs);
    } catch (err) {
      console.error("Agent workflow error:", err);
      alert(
        "Failed to process resume. Please check backend logs or endpoint methods.",
      );
    } finally {
      setLoading(false);
      setStatusText("");
    }
  };

  // Step 3: Explicitly Call Recommendation API on Button Click
  const handleGetRecommendations = async () => {
    if (!resumeId) return;
    setLoading(true);
    setStatusText(
      "AI Agent processing vector embeddings for recommended matches...",
    );

    try {
      const recommendRes = await getRecommendedJobs(resumeId);
      const recommendedJobs = Array.isArray(recommendRes)
        ? recommendRes
        : recommendRes.jobs || recommendRes.data || [];

      setJobs(() => [...recommendedJobs]);
    } catch (err) {
      console.error("Failed to fetch recommendations:", err);
      alert("Failed to load recommendations.");
    } finally {
      setLoading(false);
      setStatusText("");
    }
  };

  return (
    <div className="max-w-[1000px] mx-auto px-5 py-10 min-h-screen bg-white text-slate-900 font-sans shadow-2xl shadow-black">
      {/* Account bar */}
      <div className="flex justify-end items-center gap-3 mb-3">
        <span className="text-slate-500 text-sm">
          <span>Hello , </span>
          {user?.full_name || user?.email}
        </span>
        <button
          onClick={logout}
          className="bg-transparent border border-slate-300 text-slate-700 rounded-lg px-3 py-1.5 text-[13px] cursor-pointer hover:bg-slate-100 transition-colors"
        >
          Log out
        </button>
      </div>

      {/* Header Banner */}
      <header className="text-center mb-10">
        <div className="inline-block px-3.5 py-1.5 rounded-full bg-orange-50 text-orange-600 text-xs font-bold tracking-wider border border-orange-200 mb-3">
          ⚡ AI AGENT ACTIVE
        </div>
        <h1 className="text-4xl font-extrabold mb-2 text-slate-900">
          Autonomous <span className="text-orange-500">AI</span> Job Matcher
        </h1>
        <p className="text-slate-500 text-base max-w-[600px] mx-auto">
          Upload your resume, search instant matches, and trigger AI
          recommendation pipelines.
        </p>
      </header>

      {/* Upload Zone */}
      {!resumeId ? (
        <div className="bg-slate-50 border-2 border-dashed border-slate-200 rounded-2xl p-10 text-center">
          <div className="flex flex-col items-center">
            <div className="text-5xl mb-3">📄</div>
            <h3 className="text-lg font-semibold text-slate-900">
              Upload Your Resume
            </h3>
            <p className="text-slate-500 text-sm my-2 mb-5">
              Supports PDF, DOCX — Max 5MB
            </p>
            <label className="bg-blue-600 hover:bg-blue-700 text-white px-7 py-3 rounded-lg font-semibold cursor-pointer transition-colors inline-block">
              Select Resume
              <input
                type="file"
                accept=".pdf,.doc,.docx"
                className="hidden"
                onChange={(e) => handleFileUpload(e.target.files[0])}
              />
            </label>
          </div>
        </div>
      ) : (
        /* Resume Summary & Action Bar */
        <div className="bg-slate-50 border border-slate-200 rounded-xl p-6">
          <div className="flex justify-between items-center flex-wrap gap-3 border-b border-slate-200 pb-4">
            <div>
              <span className="text-blue-600 font-semibold">
                Active Resume ID #{resumeId}:
              </span>{" "}
              <strong className="text-slate-900">
                {file?.name || "Uploaded File"}
              </strong>
            </div>
            <button
              onClick={() => {
                setResumeId(null);
                setJobs([]);
                setAnalysis(null);
              }}
              className="bg-transparent border border-slate-300 text-slate-500 px-3 py-1.5 rounded-md cursor-pointer hover:bg-slate-100 transition-colors"
            >
              Reset / Re-upload
            </button>
          </div>

          {analysis && (
            <div className="grid grid-cols-[repeat(auto-fit,minmax(200px,1fr))] gap-4 mt-4">
              <div className="flex flex-col">
                <span className="text-xs text-slate-500 mb-1">
                  Detected Skills
                </span>
                <span className="text-[15px] font-semibold text-slate-800">
                  {analysis.skills?.slice(0, 4).join(", ") ||
                    "React, Node.js, Python"}
                </span>
              </div>
              <div className="flex flex-col">
                <span className="text-xs text-slate-500 mb-1">
                  Experience Level
                </span>
                <span className="text-[15px] font-semibold text-slate-800">
                  {analysis.experience_level || "Full Stack (3+ Yrs)"}
                </span>
              </div>
              <div className="flex flex-col">
                <span className="text-xs text-slate-500 mb-1">
                  Embedding Score
                </span>
                <span className="text-[15px] font-semibold text-emerald-500">
                  {analysis.score || "94"}% Match
                </span>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Loading Bar */}
      {loading && (
        <div className="flex items-center justify-center gap-3 my-6 text-blue-600 font-medium">
          <div className="w-5 h-5 border-[3px] border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
          <span>{statusText}</span>
        </div>
      )}

      {/* Jobs Results Display */}
      {jobs.length > 0 && (
        <section className="mt-8">
          <div className="flex justify-between items-center flex-wrap gap-4 mb-5">
            <div>
              <h2 className="text-[22px] font-semibold m-0 text-slate-900">
                Matched Job Opportunities
              </h2>
              <p className="text-slate-500 text-sm mt-1 mb-0">
                Showing search results & AI recommended roles
              </p>
            </div>

            <div className="flex gap-3">
              <button
                onClick={handleGetRecommendations}
                disabled={loading}
                className="bg-orange-50 text-orange-600 border border-orange-300 px-4.5 py-2.5 rounded-lg font-semibold cursor-pointer hover:bg-orange-100 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
              >
                ✨ Get AI Recommendations
              </button>
            </div>
          </div>

          {/* Job List Cards */}
          <div className="flex flex-col gap-4">
            {jobs.map((job, index) => (
              <div
                key={job.id || index}
                className="bg-white border border-slate-200 rounded-xl p-5 relative shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="absolute top-4 right-4 bg-slate-100 border border-slate-200 text-slate-500 text-xs px-2 py-0.5 rounded">
                  Rank #{index + 1}
                </div>

                <div className="flex justify-between items-center flex-wrap gap-4">
                  <div>
                    <h3 className="mb-1.5 text-lg font-semibold text-slate-900">
                      {job.title || "Software Engineer"}
                    </h3>
                    <p className="text-slate-500 text-sm mb-3">
                      🏢 {job.company || "Global Tech"} • 📍{" "}
                      {job.location || "Remote"}
                    </p>
                    <div className="flex gap-2 flex-wrap">
                      {(
                        job.matched_skills || ["React", "API", "JavaScript"]
                      ).map((skill, i) => (
                        <span
                          key={i}
                          className="bg-orange-50 text-orange-600 text-xs px-2.5 py-1 rounded-md"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Score */}
                  <div className="flex items-center gap-6">
                    <div className="flex flex-col items-center">
                      <span className="text-2xl font-extrabold text-emerald-500">
                        {job.match_score || 90 - index * 2}%
                      </span>
                      <span className="text-[11px] text-slate-500">
                        Match Score
                      </span>
                    </div>
                  </div>

                  <div>
                    <p className="text-slate-500 text-sm">{job.reason || ""}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Bottom Call-To-Action */}
          <div className="text-center mt-8">
            <button
              onClick={handleGetRecommendations}
              disabled={loading}
              className="border border-blue-500 text-blue-600 bg-transparent px-7 py-3 rounded-lg font-semibold cursor-pointer hover:bg-blue-50 transition-colors disabled:opacity-60"
            >
              🔄 Load Next AI Recommendations
            </button>
          </div>
        </section>
      )}
    </div>
  );
}