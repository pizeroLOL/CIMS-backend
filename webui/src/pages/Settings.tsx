import React, { useState, useEffect } from 'react';
import { Typography, Paper, Box, CircularProgress, Snackbar, Alert, Button } from '@mui/material';
import { apiClient } from '../services/api';
import ConfigEditor from '../components/ConfigEditor';

interface ServerSettings {
    ports: {
        gRPC: number;
        command: number;
        api: number;
        webui: number;
    };
    organization_name: string;
    host: string;
}

const Settings: React.FC = () => {
    const [settingsContent, setSettingsContent] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [snackbarSeverity, setSnackbarSeverity] = useState<'success' | 'error'>('success');
    const [isEditing, setIsEditing] = useState(false);

    useEffect(() => {
        fetchSettings();
    }, []);

    const fetchSettings = async () => {
        setLoading(true);
        try {
            const response = await apiClient.get('/command/server/settings');
            setSettingsContent(JSON.stringify(response.data, null, 2));
        } catch (error) {
            console.error("Failed to fetch server settings:", error);
            handleSnackbarOpen('获取服务器设置失败', 'error');
        } finally {
            setLoading(false);
        }
    };

    const handleSaveSettings = async (content: string) => {
        setLoading(true);
        try {
            const parsedContent = JSON.parse(content); // 确保内容是有效的 JSON
            await apiClient.post('/command/server/settings', parsedContent);
            setSettingsContent(content); // 更新本地显示的内容
            handleSnackbarOpen('服务器设置保存成功', 'success');
            setIsEditing(false); // 保存后退出编辑状态
        } catch (error) {
            console.error("Failed to save server settings:", error);
            handleSnackbarOpen('服务器设置保存失败', 'error');
        } finally {
            setLoading(false);
        }
    };

    const handleSnackbarOpen = (message: string, severity: 'success' | 'error') => {
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

    return (
        <div>
            <Typography variant="h4" gutterBottom>
                设置
            </Typography>

            <Paper elevation={2} style={{ padding: 20 }}>
                <Typography variant="h6" gutterBottom>服务器设置</Typography>
                {loading ? (
                    <div style={{ display: 'flex', justifyContent: 'center', margin: '20px 0' }}>
                        <CircularProgress size={24} />
                    </div>
                ) : (
                    <ConfigEditor
                        value={settingsContent}
                        onChange={setSettingsContent}
                        onSave={handleSaveSettings}
                        isEditing={isEditing}
                        setIsEditing={setIsEditing}
                    />
                )}
            </Paper>

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

export default Settings;