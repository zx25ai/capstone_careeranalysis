import React, { useState } from "react";
import axios from "axios";

const API = "http://localhost:8000";

export default function App() {
  const [profile, setProfile] = useState({ name: "", email: "", skills: [] });
  const [userId, setUserId] = useState(null);
  const [recs, setRecs] = useState([]);

  async function createProfile() {
    const res = await axios.post(API + "/profiles", profile);
    setUserId(res.data.user_id);
  }

  async function getRecs() {
    const res = await axios.get(API + `/recommend/${userId}`);
    setRecs(res.data.recommendations);
  }

  return (
    <div style={{ maxWidth: 900, margin: "20px auto" }}>
      <h1>Job Role Recommender</h1>

      <input
        placeholder="Name"
        onChange={(e) => setProfile({ ...profile, name: e.target.value })}
      />
      <br />
      <input
        placeholder="Email"
        onChange={(e) => setProfile({ ...profile, email: e.target.value })}
      />
      <br />
      <input
        placeholder="Comma-separated skills"
        onChange={(e) =>
          setProfile({
            ...profile,
            skills: e.target.value.split(",").map((s) => s.trim()),
          })
        }
      />
      <br />

      <button onClick={createProfile}>Create Profile</button>
      <button onClick={getRecs}>Get Recommendations</button>

      <h2>Recommendations</h2>
      {recs.map((r) => (
        <div key={r.job_role_id} style={{ marginBottom: 10 }}>
          <strong>{r.title}</strong> — Score: {(r.score * 100).toFixed(1)}%
          <br />
          Missing: {r.missing_skills.join(", ") || "None"}
        </div>
      ))}
    </div>
  );
}
