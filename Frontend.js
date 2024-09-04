import React, { useState, useEffect } from 'react';

function Recommendations({ userId }) {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    fetch(`/recommendations/${userId}`)
      .then(response => response.json())
      .then(data => setJobs(data));
  }, [userId]);

  return (
    <div>
      <h3>Recommended Jobs</h3>
      <ul>
        {jobs.map(job => (
          <li key={job}>{job}</li>
        ))}
      </ul>
    </div>
  );
}

export default Recommendations;
