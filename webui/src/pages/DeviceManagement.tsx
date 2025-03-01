import React, { useState, useEffect } from 'react';
import { Typography, Paper, Box, TextField, IconButton, InputAdornment, Button, CircularProgress } from '@mui/material';
import { DataGrid, GridColDef, GridRowSelectionModel, GridRenderCellParams } from '@mui/x-data-grid';
import SearchIcon from '@mui/icons-material/Search';
import RestartIcon from '@mui/icons-material/Replay';
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive';
import UpdateIcon from '@mui/icons-material/Update';
import { apiClient } from '../services/api';

interface ClientInfo {
  uid: string;
  id: string;
  isOnline: boolean;
}

interface ClientStatus {
  [uid: string]: {
    isOnline: boolean;
    lastHeartbeat: number;
  };
}

const DeviceManagement: React.FC = () => {
  const [clients, setClients] = useState<ClientInfo[]>([]);
  const [clientStatus, setClientStatus] = useState<ClientStatus>({});
  const [searchQuery, setSearchQuery] = useState('');
  const [rowSelectionModel, setRowSelectionModel] = React.useState<GridRowSelectionModel>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchClients = async () => {
      setLoading(true);
      try {
        const clientsResponse = await apiClient.get('/command/clients');
        const statusResponse = await apiClient.get('/command/clients/status');
        const clientsData = clientsResponse.data;
        const statusData: ClientStatus = statusResponse.data;

        setClientStatus(statusData);

        const clientList: ClientInfo[] = Object.entries(clientsData).map(([uid, id]) => ({
          uid,
          id: id as string,
          isOnline: statusData[uid]?.isOnline || false,
        }));
        setClients(clientList);
      } catch (error) {
        console.error("Failed to fetch clients:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchClients();
  }, []);

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(event.target.value);
  };

  const filteredClients = clients.filter(client =>
    client.id.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleRestartClient = async (uid: string) => {
    try {
      await apiClient.post(`/command/clients/${uid}/restart`);
      alert(`客户端 ${uid} 重启指令已发送`);
    } catch (error) {
      console.error("Failed to restart client:", error);
      alert(`重启客户端 ${uid} 失败`);
    }
  };

  const handleBulkRestart = async () => {
    if (rowSelectionModel.length === 0) {
      alert("请选择要批量操作的客户端");
      return;
    }
    for (const uid of rowSelectionModel) {
      await handleRestartClient(uid.toString()); // 假设 uid 是 string 类型
    }
    setRowSelectionModel([]); // 清空选择
  };


  const columns: GridColDef[] = [
    { field: 'id', headerName: '客户端名称', flex: 1 },
    {
      field: 'isOnline',
      headerName: '状态',
      width: 100,
      renderCell: (params: GridRenderCellParams) => (
        params.value ? '在线' : '离线'
      ),
    },
    {
      field: 'actions',
      headerName: '操作',
      width: 200,
      renderCell: (params: GridRenderCellParams<any, ClientInfo>) => (
        <div>
          <IconButton aria-label="restart" onClick={() => handleRestartClient(params.row.uid)}>
            <RestartIcon />
          </IconButton>
          <IconButton aria-label="notify">
            <NotificationsActiveIcon />
          </IconButton>
          <IconButton aria-label="update">
            <UpdateIcon />
          </IconButton>
        </div>
      ),
    },
  ];

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        设备管理
      </Typography>

      <Paper elevation={2} sx={{ padding: 2, mb: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <TextField
            label="搜索客户端名称"
            variant="outlined"
            size="small"
            value={searchQuery}
            onChange={handleSearchChange}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={handleBulkRestart}
            disabled={rowSelectionModel.length === 0}
          >
            批量重启
          </Button>
        </Box>
      </Paper>

      <Paper elevation={2} style={{ height: 600, width: '100%' }}>
        {loading ? (
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
            <CircularProgress />
          </div>
        ) : (
          <DataGrid
            rows={filteredClients}
            columns={columns}
            getRowId={(row) => row.uid}
            pageSizeOptions={[5, 10, 25, 50]}
            checkboxSelection
            disableRowSelectionOnClick
            onRowSelectionModelChange={(newRowSelectionModel) => {
              setRowSelectionModel(newRowSelectionModel);
            }}
            rowSelectionModel={rowSelectionModel}
          />
        )}
      </Paper>
    </div>
  );
};

export default DeviceManagement;