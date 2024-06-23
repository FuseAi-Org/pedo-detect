import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { mockMetrics, mockEntries } from '../mockData';
import appLogo from '../assets/logo.jpg'
import './Home.scss';

// Register the necessary components
ChartJS.register(ArcElement, Tooltip, Legend);

function Home() {
    const [metrics, setMetrics] = useState([]);
    const [entries, setEntries] = useState([]);
    const [search, setSearch] = useState('');
    const [filter, setFilter] = useState('');
    const [clientId] = useState('client_123');

    useEffect(() => {
        // Using mock data instead of API call
        setMetrics(mockMetrics);
        fetchEntries();
    }, []);

    const fetchEntries = () => {
        // Filter mock entries based on search and filter
        let filteredEntries = mockEntries;
        if (search) {
            filteredEntries = filteredEntries.filter(entry =>
                entry.content.toLowerCase().includes(search.toLowerCase())
            );
        }
        if (filter) {
            filteredEntries = filteredEntries.filter(entry => entry.score >= filter);
        }
        setEntries(filteredEntries);
    };

    const handleSearch = (e) => {
        e.preventDefault();
        fetchEntries();
    };

    const handleFilter = (filterValue) => {
        setFilter(filterValue);
        fetchEntries();
    };

    return (
        <div className="home">
            <div className="home_header">
                <Link to="/">
                    <div className='home_header_left'>
                        <img src={appLogo} alt="Logo" />
                        PedoDetect
                    </div>
                </Link>
                <Link to="/settings">
                    <div className="user-icon home_header_right">U</div>
                </Link>
            </div>
            <div className="metrics">
                {metrics.map((metric, index) => (
                    <div key={index} className="metric">
                        <Doughnut
                            data={{
                                datasets: [{
                                    data: [metric.score, 100 - metric.score],
                                    backgroundColor: ['#36A2EB', '#EEE'],
                                    borderColor: ['#36A2EB', '#EEE'],
                                    borderWidth: 2, // Border width for the segments
                                    cutout: '80%' // Adjust the thickness of the ring
                                }],
                                labels: ['Score', 'Remaining']
                            }}
                            options={{ maintainAspectRatio: false, plugins: { legend: { display: false } } }}
                        />
                        <p className="metric_score">{metric.score}</p>
                        <p>{metric.name}</p>
                    </div>
                ))}
            </div>
            <div className="home_title">Activity Feed</div>
            <div className="home_search">
                <form onSubmit={handleSearch}>
                    <input
                        type="text"
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        placeholder="Search"
                    />
                    <button type="submit">→</button>
                </form>
                <div className="home_search_filters">
                    <button onClick={() => handleFilter(80)}>High-Sus</button>
                    <button onClick={() => handleFilter(60)}>Med-Sus</button>
                    <button onClick={() => handleFilter(40)}>Low-Sus</button>
                    <button onClick={() => handleFilter('')}>All</button>
                </div>
            </div>
            <div className="home_entries_container">
                <div className="home_entries">
                    {entries.map((entry, index) => (
                        <div key={index} className="home_entry">
                            <div className="home_entry_left">
                                <div className="home_entry-icon">{entry.content.charAt(0).toUpperCase()}</div>
                                <p>{entry.content}</p>
                            </div>
                            <div className="home_entry-content">
                                <Doughnut
                                    className="home_entry-content_chart"
                                    data={{
                                        datasets: [{
                                            data: [entry.score, 100 - entry.score],
                                            backgroundColor: ['#36A2EB', '#EEE'],
                                            borderColor: ['#36A2EB', '#EEE'],
                                            borderWidth: 2, // Border width for the segments
                                            cutout: '80%' // Adjust the thickness of the ring
                                        }],
                                        labels: ['Score', 'Remaining']
                                    }}
                                    options={{ maintainAspectRatio: false, plugins: { legend: { display: false } } }}
                                    width={40}
                                    height={40}
                                />
                                <p>{entry.score}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default Home;
