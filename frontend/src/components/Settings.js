import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import appLogo from '../assets/logo.jpg';
import './Settings.scss';

// Register the necessary components
ChartJS.register(ArcElement, Tooltip, Legend);

function Settings() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [platform, setPlatform] = useState('');
    const [accounts, setAccounts] = useState({
        Instagram: { id: 1, name: '', metricScore: 0, isActive: true },
        Facebook: { id: 2, name: '', metricScore: 0, isActive: true },
        Twitter: { id: 3, name: '', metricScore: 0, isActive: true }
    });
    const [loggedInPlatforms, setLoggedInPlatforms] = useState([]);

    useEffect(() => {
        // Load data from sessionStorage on mount
        const storedAccounts = JSON.parse(sessionStorage.getItem('accounts'));
        const storedPlatforms = JSON.parse(sessionStorage.getItem('loggedInPlatforms'));
        console.log('Loaded accounts from sessionStorage:', storedAccounts);
        console.log('Loaded loggedInPlatforms from sessionStorage:', storedPlatforms);
        if (storedAccounts) setAccounts(storedAccounts);
        if (storedPlatforms) setLoggedInPlatforms(storedPlatforms);
    }, []);

    useEffect(() => {
        // Save data to sessionStorage whenever accounts or loggedInPlatforms changes
        console.log('Saving accounts to sessionStorage:', accounts);
        console.log('Saving loggedInPlatforms to sessionStorage:', loggedInPlatforms);
        sessionStorage.setItem('accounts', JSON.stringify(accounts));
        sessionStorage.setItem('loggedInPlatforms', JSON.stringify(loggedInPlatforms));
    }, [accounts, loggedInPlatforms]);

    const handleLogin = (e) => {
        e.preventDefault();
        const randomScore = (Math.random() * 100).toFixed(2);
        setAccounts(prevAccounts => {
            const updatedAccounts = {
                ...prevAccounts,
                [platform]: {
                    ...prevAccounts[platform],
                    name: username,
                    metricScore: randomScore
                }
            };
            console.log('Updating accounts:', updatedAccounts);
            sessionStorage.setItem('accounts', JSON.stringify(updatedAccounts));
            return updatedAccounts;
        });
        if (!loggedInPlatforms.includes(platform)) {
            const updatedPlatforms = [...loggedInPlatforms, platform];
            setLoggedInPlatforms(updatedPlatforms);
            console.log('Updating loggedInPlatforms:', updatedPlatforms);
            sessionStorage.setItem('loggedInPlatforms', JSON.stringify(updatedPlatforms));
        }
        setUsername('');
        setPassword('');
        setPlatform('');
    };

    const handleToggle = (platform) => {
        setAccounts(prevAccounts => {
            const updatedAccounts = {
                ...prevAccounts,
                [platform]: {
                    ...prevAccounts[platform],
                    isActive: !prevAccounts[platform].isActive
                }
            };
            console.log('Toggling isActive for platform:', platform, updatedAccounts);
            sessionStorage.setItem('accounts', JSON.stringify(updatedAccounts));
            return updatedAccounts;
        });
    };

    return (
        <div className="settings">
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

            <form onSubmit={handleLogin} className='settings_login'>
                <div>
                    <label htmlFor="platform">Social Media Platform</label>
                    <select
                        id="platform"
                        value={platform}
                        onChange={(e) => setPlatform(e.target.value)}
                        required
                    >
                        <option value="">Select a platform</option>
                        <option value="Instagram">Instagram</option>
                        <option value="Facebook">Facebook</option>
                        <option value="Twitter">Twitter</option>
                    </select>
                </div>
                <div>
                    <label htmlFor="username">Username</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Enter your username"
                        required
                    />
                </div>
                <div>
                    <label htmlFor="password">Password</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Enter your password"
                        required
                    />
                </div>
                <button type="submit">Login</button>
            </form>

            <div className="accounts">
                {loggedInPlatforms.map((platformKey) => (
                    <div key={platformKey} className="account">

                        <div className='account_left'>
                            <h3><span>Platform: </span>{platformKey}</h3>
                            <p><span>Username: </span>{accounts[platformKey].name}</p>
                            <p><span>Enable Tracking?: </span><button onClick={() => handleToggle(platformKey)}>
                                {accounts[platformKey].isActive ? 'Disable' : 'Enable'}
                            </button></p>
                        </div>
                        <div className='account_right'>
                            <Doughnut data={{
                                datasets: [{
                                    data: [accounts[platformKey].metricScore, 100 - accounts[platformKey].metricScore],
                                    backgroundColor: ['#36A2EB', '#EEE'],
                                    borderColor: ['#36A2EB', '#EEE'],
                                    borderWidth: 2, // Border width for the segments
                                    cutout: '80%' // Adjust the thickness of the ring
                                }],
                                labels: ['Score', 'Remaining']
                            }} options={{ maintainAspectRatio: false, plugins: { legend: { display: false } } }} />
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Settings;
