import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import Overview from './pages/Overview';
import DeviceManagement from './pages/DeviceManagement';
import ConfigurationManagement from './pages/ConfigurationManagement';
import Settings from './pages/Settings';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Overview />} />
          <Route path="/devices" element={<DeviceManagement />} />
          <Route path="/configs" element={<ConfigurationManagement />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;