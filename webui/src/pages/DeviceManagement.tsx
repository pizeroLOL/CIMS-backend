import React, { useState, useEffect } from 'react';
import { Typography, Paper, Box, TextField, IconButton, InputAdornment, Button, CircularProgress, Dialog, DialogTitle, DialogContent, DialogActions, FormControlLabel, Checkbox, Grid, Snackbar, Alert, Tooltip, useMediaQuery, useTheme } from '@mui/material';
import { DataGrid, GridColDef, GridRowSelectionModel, GridRenderCellParams } from '@mui/x-data-grid';
import SearchIcon from '@mui/icons-material/Search';
import RestartIcon from '@mui/icons-material/Replay';
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive';
import UpdateIcon from '@mui/icons-material/Update';
import RefreshIcon from '@mui/icons-material/Refresh';
import { apiClient } from '../services/api';

interface ClientInfo {
    uid: string;
    id: string;
    displayName: string;
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
    const [notifyDialogOpen, setNotifyDialogOpen] = useState(false);
    const [notifyClientUid, setNotifyClientUid] = useState<string | null>(null);
    const [notificationTitle, setNotificationTitle] = useState('来自控制台的消息');
    const [notificationMessage, setNotificationMessage] = useState('');
    const [isEmergency, setIsEmergency] = useState(false);
    const [durationSeconds, setDurationSeconds] = useState<number>(5);
    const [repeatCounts, setRepeatCounts] = useState<number>(1);
    const [isSpeechEnabled, setIsSpeechEnabled] = useState(true);
    const [isEffectEnabled, setIsEffectEnabled] = useState(true);
    const [isSoundEnabled, setIsSoundEnabled] = useState(true);
    const [isTopmost, setIsTopmost] = useState(true);
    const [overlayIconLeft, setOverlayIconLeft] = useState<number>(0);
    const [overlayIconRight, setOverlayIconRight] = useState<number>(0);
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [snackbarSeverity, setSnackbarSeverity] = useState<'success' | 'error' | 'warning'>('success'); // 添加 'warning' 类型
    const theme = useTheme();
    const isSmDown = useMediaQuery(theme.breakpoints.down('sm'));

    const fetchClientsData = async () => {
        setLoading(true);
        try {
            const clientsResponse = await apiClient.get('/command/clients');
            const statusResponse = await apiClient.get('/command/clients/status');
            const clientsData = clientsResponse.data;
            const statusData: ClientStatus = statusResponse.data;

            setClientStatus(statusData);

            const clientList: ClientInfo[] = Object.entries(clientsData).map(([uid, id]) => {
                // Explicitly cast displayName to string using 'as string'
                const displayName = (id ? id : `${uid.substring(0, 4)}...${uid.substring(uid.length - 2)}`) as string;
                return {
                    uid,
                    id: id as string,
                    displayName,
                    isOnline: statusData[uid]?.isOnline || false,
                };
            });
            setClients(clientList);
        } catch (error) {
            console.error("Failed to fetch clients:", error);
            handleSnackbarOpen('获取客户端数据失败', 'error');
        } finally {
            setLoading(false);
        }
    };


    useEffect(() => {
        fetchClientsData();
        const intervalId = setInterval(fetchClientsData, 5000);
        return () => clearInterval(intervalId);
    }, []);

    const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSearchQuery(event.target.value);
    };

    const filteredClients = clients.filter(client =>
        client.displayName.toLowerCase().includes(searchQuery.toLowerCase())
    );

    const handleRestartClient = async (uid: string, clientId: string) => {
        try {
            await apiClient.get(`/command/clients/${uid}/restart`);
            handleSnackbarOpen(`客户端 ${clientId || uid} 重启指令已发送`, 'success');
        } catch (error: any) {
            if (error.response?.status === 404) {
                handleSnackbarOpen(`客户端 ${clientId || uid} 离线`, 'error');
            } else {
                handleSnackbarOpen(`重启客户端 ${clientId || uid} 失败`, 'error');
                console.error("Failed to restart client:", error);
            }
        }
    };

    const handleBulkRestart = async () => {
        if (rowSelectionModel.length === 0) {
            handleSnackbarOpen("请选择要批量操作的客户端", 'warning');
            return;
        }
        setLoading(true); // 批量操作开始时设置 loading 状态
        for (const uid of rowSelectionModel) {
            const client = clients.find(c => c.uid === uid);
            await handleRestartClient(uid.toString(), client?.id || '');
        }
        setRowSelectionModel([]);
        setLoading(false); // 批量操作完成后取消 loading 状态
        handleSnackbarOpen('批量重启指令已发送', 'success');
    };

    const handleUpdateClient = async (uid: string, clientId: string) => {
        try {
            await apiClient.get(`/command/clients/${uid}/update`);
            handleSnackbarOpen(`客户端 ${clientId || uid} 更新配置指令已发送`, 'success');
        } catch (error: any) {
            if (error.response?.status === 404) {
                handleSnackbarOpen(`客户端 ${clientId || uid} 离线`, 'error');
            } else {
                handleSnackbarOpen(`客户端 ${clientId || uid} 更新配置失败`, 'error');
                console.error("Failed to update client:", error);
            }
        }
    };

    const handleBulkUpdate = async () => {
        if (rowSelectionModel.length === 0) {
            handleSnackbarOpen("请选择要批量操作的客户端", 'warning');
            return;
        }
        setLoading(true); // 批量操作开始时设置 loading 状态
        for (const uid of rowSelectionModel) {
            const client = clients.find(c => c.uid === uid);
            await handleUpdateClient(uid.toString(), client?.id || '');
        }
        setRowSelectionModel([]);
        setLoading(false); // 批量操作完成后取消 loading 状态
        handleSnackbarOpen('批量更新配置指令已发送', 'success');
    };

    const handleNotifyClient = (uid: string) => {
        setNotifyClientUid(uid);
        setNotifyDialogOpen(true);
    };

    const handleBulkNotify = () => {
        if (rowSelectionModel.length === 0) {
            handleSnackbarOpen("请选择要批量操作的客户端", 'warning');
            return;
        }
        setNotifyDialogOpen(true); // 打开通知对话框，准备批量发送
    };

    const handleSendNotification = async () => {
        if (!notifyClientUid && rowSelectionModel.length === 0) return; // 检查是否有选定客户端
        setLoading(true); // 批量操作开始时设置 loading 状态
        const uidsToNotify = notifyClientUid ? [notifyClientUid] : rowSelectionModel.map(uid => uid.toString()); // 单个或批量 UID
        let successCount = 0;
        let failCount = 0;

        for (const uid of uidsToNotify) {
            const client = clients.find(c => c.uid === uid);
            const clientId = client?.id || '';
            try {
                const params = new URLSearchParams({
                    message_mask: notificationTitle,
                    message_content: notificationMessage,
                    overlay_icon_left: overlayIconLeft.toString(),
                    overlay_icon_right: overlayIconRight.toString(),
                    is_emergency: String(isEmergency),
                    is_speech_enabled: String(isSpeechEnabled),
                    is_effect_enabled: String(isEffectEnabled),
                    is_sound_enabled: String(isSoundEnabled),
                    is_topmost: String(isTopmost),
                    duration_seconds: durationSeconds.toString(),
                    repeat_counts: repeatCounts.toString(),
                });

                await apiClient.get(`/command/clients/${uid}/notify?${params.toString()}`);
                successCount++;
            } catch (error: any) {
                console.error(`Failed to send notification to client ${clientId || uid}:`, error);
                failCount++;
            }
        }

        setLoading(false); // 批量操作完成后取消 loading 状态
        handleCloseNotifyDialog();
        if (failCount === 0) {
            handleSnackbarOpen(`成功向 ${successCount} 个客户端发送通知`, 'success');
        } else {
            handleSnackbarOpen(`成功${successCount}个, 失败${failCount}个客户端发送通知`, 'warning');
        }

    };

    const handleCloseNotifyDialog = () => {
        setNotifyDialogOpen(false);
        setNotifyClientUid(null);
        setNotificationTitle('来自控制台的消息');
        setNotificationMessage('');
        setIsEmergency(false);
        setDurationSeconds(5);
        setRepeatCounts(1);
        setIsSpeechEnabled(true);
        setIsEffectEnabled(true);
        setIsSoundEnabled(true);
        setIsTopmost(true);
        setOverlayIconLeft(0);
        setOverlayIconRight(0);
        setRowSelectionModel([]); // 关闭对话框时清空批量选择，避免下次批量通知时仍然选中上次的客户端
    };

    const handleSnackbarOpen = (message: string, severity: 'success' | 'error' | 'warning') => {
        setSnackbarMessage(message);
        setSnackbarSeverity(severity);
        setSnackbarOpen(true);
    };

    const handleSnackbarClose = (event: React.SyntheticEvent | Event, reason?: string) => {
        if (reason === 'clickaway') {
            return;
        }
        setSnackbarOpen(false);
    };

    const handleRefresh = () => {
        fetchClientsData();
        handleSnackbarOpen('客户端列表已刷新', 'success');
    };


    const columns: GridColDef[] = [
        {
            field: 'displayName',
            headerName: '客户端名称',
            flex: 1,
            renderCell: (params: GridRenderCellParams<any, ClientInfo>) => (
                <div title={params.row.id}>{params.row.displayName}</div>
            )
        },
        {
            field: 'isOnline',
            headerName: '状态',
            width: isSmDown ? 80 : 100,
            renderCell: (params: GridRenderCellParams) => (
                params.value ? '在线' : '离线'
            ),
        },
        {
            field: 'actions',
            headerName: '操作',
            width: isSmDown ? 180 : 200, // 操作列宽度稍作调整
            renderCell: (params: GridRenderCellParams<any, ClientInfo>) => (
                <div>
                    <Tooltip title="重启客户端">
                        <IconButton aria-label="restart" onClick={() => handleRestartClient(params.row.uid, params.row.id)}>
                            <RestartIcon />
                        </IconButton>
                    </Tooltip>
                    <Tooltip title="发送通知">
                        <IconButton aria-label="notify" onClick={() => handleNotifyClient(params.row.uid)}>
                            <NotificationsActiveIcon />
                        </IconButton>
                    </Tooltip>
                    <Tooltip title="更新配置">
                        <IconButton aria-label="update" onClick={() => handleUpdateClient(params.row.uid, params.row.id)}>
                            <UpdateIcon />
                        </IconButton>
                    </Tooltip>
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
                <Grid container spacing={2} alignItems="center">
                    <Grid item xs={12} sm={6}>
                        <TextField
                            fullWidth
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
                    </Grid>
                    <Grid item xs={12} sm={6} md="auto" sx={{ textAlign: { xs: 'left', sm: 'right' } }}>
                        <Tooltip title="刷新客户端列表">
                            <IconButton aria-label="refresh" onClick={handleRefresh} disabled={loading}>
                                <RefreshIcon />
                            </IconButton>
                        </Tooltip>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={handleBulkRestart}
                            disabled={rowSelectionModel.length === 0 || loading}
                            sx={{ ml: 1 }}
                        >
                            批量重启
                        </Button>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={handleBulkNotify}
                            disabled={rowSelectionModel.length === 0 || loading}
                            sx={{ ml: 1 }}
                        >
                            批量通知
                        </Button>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={handleBulkUpdate}
                            disabled={rowSelectionModel.length === 0 || loading}
                            sx={{ ml: 1 }}
                        >
                            批量更新
                        </Button>
                    </Grid>
                </Grid>
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
                        sx={{
                            '& .MuiDataGrid-columnHeader--menuIcon': { display: 'none' },
                        }}
                    />
                )}
            </Paper>

            {/* 通知对话框 */}
            <Dialog open={notifyDialogOpen} onClose={handleCloseNotifyDialog} fullWidth maxWidth="sm">
                <DialogTitle>发送通知</DialogTitle>
                <DialogContent>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <TextField
                                autoFocus
                                margin="dense"
                                id="notification-title"
                                label="通知标题"
                                fullWidth
                                variant="outlined"
                                value={notificationTitle}
                                onChange={(e) => setNotificationTitle(e.target.value)}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                margin="dense"
                                id="notification-message"
                                label="消息内容"
                                fullWidth
                                variant="outlined"
                                multiline
                                rows={3}
                                value={notificationMessage}
                                onChange={(e) => setNotificationMessage(e.target.value)}
                            />
                        </Grid>
                        <Grid item xs={6}>
                            <TextField
                                margin="dense"
                                id="duration-seconds"
                                label="持续时间 (秒)"
                                type="number"
                                fullWidth
                                variant="outlined"
                                value={durationSeconds}
                                onChange={(e) => setDurationSeconds(Number(e.target.value))}
                                inputProps={{ min: 1 }}
                            />
                        </Grid>
                        <Grid item xs={6}>
                            <TextField
                                margin="dense"
                                id="repeat-counts"
                                label="重复次数"
                                type="number"
                                fullWidth
                                variant="outlined"
                                value={repeatCounts}
                                onChange={(e) => setRepeatCounts(Number(e.target.value))}
                                inputProps={{ min: 1 }}
                            />
                        </Grid>
                        <Grid item xs={6}>
                            <TextField
                                margin="dense"
                                id="overlay-icon-left"
                                label="左侧图标偏移"
                                type="number"
                                fullWidth
                                variant="outlined"
                                value={overlayIconLeft}
                                onChange={(e) => setOverlayIconLeft(Number(e.target.value))}
                            />
                        </Grid>
                        <Grid item xs={6}>
                            <TextField
                                margin="dense"
                                id="overlay-icon-right"
                                label="右侧图标偏移"
                                type="number"
                                fullWidth
                                variant="outlined"
                                value={overlayIconRight}
                                onChange={(e) => setOverlayIconRight(Number(e.target.value))}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <FormControlLabel
                                control={<Checkbox checked={isEmergency} onChange={(e) => setIsEmergency(e.target.checked)} />}
                                label="紧急通知"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <FormControlLabel
                                control={<Checkbox checked={isSpeechEnabled} onChange={(e) => setIsSpeechEnabled(e.target.checked)} />}
                                label="语音播报"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <FormControlLabel
                                control={<Checkbox checked={isEffectEnabled} onChange={(e) => setIsEffectEnabled(e.target.checked)} />}
                                label="动画效果"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <FormControlLabel
                                control={<Checkbox checked={isSoundEnabled} onChange={(e) => setIsSoundEnabled(e.target.checked)} />}
                                label="声音提示"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <FormControlLabel
                                control={<Checkbox checked={isTopmost} onChange={(e) => setIsTopmost(e.target.checked)} />}
                                label="置顶显示"
                            />
                        </Grid>
                    </Grid>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseNotifyDialog}>取消</Button>
                    <Button onClick={handleSendNotification} color="primary">发送</Button>
                </DialogActions>
            </Dialog>

            {/* 页面内通知 Snackbar */}
            <Snackbar
                open={snackbarOpen}
                autoHideDuration={3000}
                onClose={handleSnackbarClose}
                anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
            >
                <Alert onClose={handleSnackbarClose} severity={snackbarSeverity} sx={{ width: '100%' }}>
                    {snackbarMessage}
                </Alert>
            </Snackbar>
        </div>
    );
};

export default DeviceManagement;