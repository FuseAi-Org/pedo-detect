import React, { useState } from 'react';
import './App.css';
import MetricCard from './components/MetricCard';
import SearchBar from './components/SearchBar';
import UserCard from './components/UserCard';

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('All');

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleFilterChange = (newFilter) => {
    setFilter(newFilter);
  };

  const users = [
    { name: 'Andre', initial: 'A', percentage: '12.35' },
    { name: 'Daniel', initial: 'D', percentage: '62.35' },
    { name: 'Christina', initial: 'C', percentage: '92.35'},
    // Add more users as needed
  ];

  const filteredUsers = users
    .filter(user => user.name.toLowerCase().includes(searchTerm.toLowerCase()))
    .filter(user => {
      if (filter === 'High-Sus') return user.percentage > 66;
      if (filter === 'Med-Sus') return user.percentage > 33 && user.percentage <= 66;
      if (filter === 'Low-Sus') return user.percentage <= 33;
      return true; // For 'All' filter
    });

  return (
    <div className="app">
      <div className="metrics">
        <MetricCard title="Pedo Client Engagement" percentage={12.35} />
        <MetricCard title="Susceptibility to Pedos" percentage={52.35} />
        <MetricCard title="Metric 3" percentage={71} />
      </div>
      <SearchBar onSearch={handleSearch} onFilterChange={handleFilterChange} />
      <div className="activity-feed">
        {filteredUsers.map((user, index) => (
          <UserCard key={index} {...user} />
        ))}
      </div>
    </div>
  );
}

export default App;
