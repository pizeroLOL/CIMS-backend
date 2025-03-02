import React, { useState, useEffect } from 'react';
import { Typography, Grid, Paper, CircularProgress } from '@mui/material';
import { apiClient } from '../services/api';

interface ClientStatus {
  [uid: string]: {
    isOnline: boolean;
    lastHeartbeat: number;
  };
}

const Overview: React.FC = () => {
  const [totalClients, setTotalClients] = useState<number>(0);
  const [onlineClients, setOnlineClients] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchClientData = async () => {
      setLoading(true);
      try {
        const clientsResponse = await apiClient.get('/command/clients');
        const statusResponse = await apiClient.get('/command/clients/status');

        const clients = clientsResponse.data;
        const status: ClientStatus = statusResponse.data;

        setTotalClients(Object.keys(clients).length);
        let onlineCount = 0;
        for (const uid in status) {
          if (status[uid].isOnline) {
            onlineCount++;
          }
        }
        setOnlineClients(onlineCount);
      } catch (error) {
        console.error("Failed to fetch client data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchClientData();
  }, []);

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        概览
      </Typography>
      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '200px' }}>
          <CircularProgress />
        </div>
      ) : (
        <Grid container spacing={3}> {/* 使用 Grid 容器 */}
          <Grid item xs={12} sm={6} md={4} lg={3}> {/* 响应式 Grid Item */}
            <Paper elevation={3} style={{ padding: '20px', textAlign: 'center' }}>
              <Typography variant="h6">总客户端数量</Typography>
              <Typography variant="h3">{totalClients}</Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={4} lg={3}> {/* 响应式 Grid Item */}
            <Paper elevation={3} style={{ padding: '20px', textAlign: 'center' }}>
              <Typography variant="h6">在线客户端数量</Typography>
              <Typography variant="h3">{onlineClients}</Typography>
            </Paper>
          </Grid>
          {/* 可以添加更多概览信息卡片 */}
        </Grid>
      )}
    </div>
  );
};

export default Overview;