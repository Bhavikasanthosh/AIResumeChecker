import { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("linkedin_text", ""); // Module 3 placeholder

    try {
      // Using 127.0.0.1 to avoid local DNS/resolution timeouts on Mac
      const response = await fetch("http://127.0.0.1:8000/api/analyze", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Backend server error");

      const result = await response.json();
      setData(result);
    } catch (err) {
      console.error("Pipeline Error:", err);
      alert("Connection failed. Ensure the backend is running with: ./venv/bin/python -m uvicorn api:app --reload");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ backgroundColor: '#f1f5f9', minHeight: '100vh', fontFamily: '"Inter", sans-serif', color: '#0f172a' }}>
      {/* Top Navigation */}
      <nav style={{ backgroundColor: '#1e293b', color: 'white', padding: '1rem 3rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}>
        <h1 style={{ fontSize: '1.2rem', fontWeight: '800' }}>🛡️ RESUME AUTHENTICITY SYSTEM</h1>
        <span style={{ fontSize: '0.8rem', opacity: 0.7 }}>MODULES 1-3 | AI VERIFICATION ACTIVE</span>
      </nav>

      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '40px' }}>
        
        {!data ? (
          /* UPLOAD VIEW - Module 1 Entry Point */
          <div style={{ textAlign: 'center', marginTop: '10vh' }}>
            <div style={{ backgroundColor: 'white', padding: '60px', borderRadius: '24px', boxShadow: '0 20px 25px -5px rgba(0,0,0,0.1)', maxWidth: '600px', margin: '0 auto' }}>
              <h2 style={{ marginBottom: '10px' }}>Analyze Candidate</h2>
              <p style={{ color: '#64748b', marginBottom: '30px' }}>Upload PDF to trigger spaCy NER and BERT Skill Extraction.</p>
              
              <label htmlFor="upload" style={{ display: 'block', padding: '20px', border: '2px dashed #cbd5e1', borderRadius: '12px', cursor: 'pointer', marginBottom: '20px' }}>
                <input type="file" id="upload" onChange={(e) => setFile(e.target.files[0])} style={{ display: 'none' }} />
                <span style={{ color: '#2563eb', fontWeight: '600' }}>{file ? file.name : "Select Resume PDF"}</span>
              </label>

              <button onClick={handleUpload} disabled={!file || loading} style={{ width: '100%', padding: '15px', backgroundColor: '#2563eb', color: 'white', border: 'none', borderRadius: '12px', fontWeight: '700', cursor: 'pointer' }}>
                {loading ? "Processing AI Pipeline..." : "Scan & Authenticate"}
              </button>
            </div>
          </div>
        ) : (
          /* DASHBOARD VIEW - Professional Recruiter Interface */
          <div style={{ display: 'grid', gridTemplateColumns: '350px 1fr', gap: '30px' }}>
            
            {/* LEFT SIDEBAR: Profile, Skills, and Scores */}
            <aside style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <div style={{ backgroundColor: 'white', padding: '25px', borderRadius: '20px', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
                <h3 style={{ margin: '0 0 15px' }}>{data.profile.name}</h3>
                <p style={{ fontSize: '0.9rem', color: '#64748b' }}>{data.profile.email}</p>
                <div style={{ marginTop: '20px', borderTop: '1px solid #eee', paddingTop: '15px' }}>
                  <div style={{ marginBottom: '10px' }}>
                    <small style={{ fontWeight: 'bold', color: '#94a3b8' }}>RESUME STRENGTH</small>
                    <div style={{ fontSize: '1.8rem', fontWeight: '800', color: '#2563eb' }}>{data.strength_score}%</div>
                  </div>
                  <div>
                    <small style={{ fontWeight: 'bold', color: '#94a3b8' }}>GITHUB MATCH (MOD 2)</small>
                    <div style={{ fontSize: '1.8rem', fontWeight: '800', color: '#10b981' }}>{Math.round(data.github_match_score * 100)}%</div>
                  </div>
                </div>
              </div>

              {/* SKILL INTELLIGENCE */}
              <div style={{ backgroundColor: 'white', padding: '25px', borderRadius: '20px', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
                <h4 style={{ margin: '0 0 15px', fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase' }}>Skill Intelligence</h4>
                {Object.entries(data.skills.categorized).map(([cat, list]) => (
                  list.length > 0 && (
                    <div key={cat} style={{ marginBottom: '15px' }}>
                      <div style={{ fontSize: '0.7rem', fontWeight: 'bold', color: '#64748b' }}>{cat}</div>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '5px', marginTop: '5px' }}>
                        {list.map(s => <span key={s} style={{ background: '#f1f5f9', padding: '3px 8px', borderRadius: '6px', fontSize: '0.75rem' }}>{s}</span>)}
                      </div>
                    </div>
                  )
                ))}
              </div>
            </aside>

            {/* MAIN CONTENT: Summary, Experience, and Repos */}
            <main style={{ display: 'flex', flexDirection: 'column', gap: '25px' }}>
              
              {/* AI SUMMARY */}
              <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '20px', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
                <h3 style={{ marginTop: 0 }}>✨ AI Insight Summary</h3>
                <p style={{ lineHeight: '1.6', color: '#475569' }}>{data.ai_summary}</p>
              </div>

              {/* CAREER TIMELINE */}
              <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '20px', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
                <h3 style={{ marginTop: 0, marginBottom: '20px' }}>💼 Career Timeline</h3>
                {data.experience && data.experience.length > 0 ? (
                    data.experience.map((job, i) => (
                    <div key={i} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '20px', background: '#f8fafc', borderRadius: '15px', marginBottom: '10px', border: '1px solid #e2e8f0' }}>
                        <div>
                        <div style={{ fontWeight: '800', fontSize: '1.05rem' }}>{job.role}</div>
                        <div style={{ color: '#64748b', fontSize: '0.9rem' }}>{job.company}</div>
                        </div>
                        <div style={{ fontWeight: '700', color: '#2563eb', background: 'white', padding: '5px 12px', borderRadius: '10px', border: '1px solid #cbd5e1' }}>{job.years}</div>
                    </div>
                    ))
                ) : (
                    <p style={{ color: '#94a3b8', fontStyle: 'italic' }}>No structured experience detected.</p>
                )}
              </div>

              {/* GITHUB REPOS - Module 2 Proof */}
              <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '20px', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
                <h3 style={{ marginTop: 0, marginBottom: '20px' }}>📦 Verified GitHub Projects</h3>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
                  {data.github_repos && data.github_repos.length > 0 ? data.github_repos.map((repo, i) => (
                    <div key={i} style={{ padding: '15px', border: '1px solid #e5e7eb', borderRadius: '12px' }}>
                      <a href={repo.html_url} target="_blank" rel="noreferrer" style={{ fontWeight: 'bold', color: '#2563eb', textDecoration: 'none' }}>{repo.name}</a>
                      <p style={{ fontSize: '0.8rem', color: '#64748b', margin: '5px 0' }}>{repo.description || "Project verified via GitHub API."}</p>
                      <span style={{ fontSize: '0.7rem', background: '#f1f5f9', padding: '2px 6px', borderRadius: '4px' }}>{repo.language}</span>
                    </div>
                  )) : <p style={{ color: '#94a3b8' }}>No public repositories found.</p>}
                </div>
              </div>

              <button onClick={() => setData(null)} style={{ alignSelf: 'center', background: 'none', border: 'none', cursor: 'pointer', textDecoration: 'underline', color: '#64748b', marginTop: '20px' }}>
                Scan New Candidate
              </button>
            </main>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;