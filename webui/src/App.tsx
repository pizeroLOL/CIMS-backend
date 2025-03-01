// 确保已安装: npm install react-router-dom @types/react-router-dom
import React from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom'; // 正确导入
import Sidebar from './components/Sidebar';
import Overview from './components/Overview';
import DeviceManagement from './components/DeviceManagement';
import ConfigManagement from './components/ConfigManagement';
import Settings from './components/Settings';

function App() {
    return (
        <Router>
            <AppContent />
        </Router>
    );
}

function AppContent() {
    const location = useLocation();

    return (
        <div className="app-container">
            <Sidebar />
            <main className="main-content">
                <Routes>
                    <Route path="/" element={<Overview />} />
                    <Route path="/device" element={<DeviceManagement />} />
                    <Route path="/config" element={<ConfigManagement />} />
                    <Route path="/settings" element={<Settings />} />
                    <Route path="*" element={<Overview />} />
                </Routes>
            </main>
        </div>
    );
}

export default App;