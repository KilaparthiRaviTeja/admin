import React, { useEffect, useState } from "react";
import "./App.css";

const AdminDashboard = () => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    try {
      setLoading(true);
      const response = await fetch("http://localhost:8000/admin/applications/");
      const data = await response.json();
      setApplications(data);
    } catch (error) {
      setError("Failed to load applications");
    } finally {
      setLoading(false);
    }
  };

  const updateStatus = async (appId, newStatus) => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:8000/admin/applications/${appId}?status=${newStatus}`, {
        method: "PUT",
      });

      if (!response.ok) {
        throw new Error("Failed to update application");
      }

      fetchApplications(); // Refresh after update
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="admin-container">
      <h2>Admin Dashboard</h2>
      {error && <p className="error-message">{error}</p>}
      {loading && <p>Loading...</p>}

      <table className="admin-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Status</th>
            <th>ETA</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {applications.map((app) => (
            <tr key={app._id}>
              <td>{app.first_name} {app.last_name}</td>
              <td>{app.status}</td>
              <td>{app.approval_eta !== null ? `${app.approval_eta} days` : "N/A"}</td>
              <td>
                {app.status === "Pending" && (
                  <>
                    <button onClick={() => updateStatus(app._id, "Approved")} className="approve-btn">Approve</button>
                    <button onClick={() => updateStatus(app._id, "Rejected")} className="reject-btn">Reject</button>
                  </>
                )}
                {app.status === "Approved" && <span className="approved">✔ Approved</span>}
                {app.status === "Rejected" && <span className="rejected">✖ Rejected</span>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminDashboard;
