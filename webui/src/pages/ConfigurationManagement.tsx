import React, { useState, useEffect } from 'react';
import {
    Typography,
    Paper,
    Tabs,
    Tab,
    Box,
    CircularProgress,
    Button,
    Snackbar,
    Alert,
    Grid,
    useMediaQuery,
    useTheme,
    FormControlLabel,
    Switch,
    FormGroup,
    FormControl
} from '@mui/material';
import { apiClient } from '../services/api';
import ConfigEditor from '../components/ConfigEditor';
import DescriptionIcon from '@mui/icons-material/Description';

interface ConfigManifest {
    [key: string]: {
        Value: string;
        Version: number;
    };
}

interface PolicyConfig {
    DisableProfileClassPlanEditing: boolean;
    DisableProfileTimeLayoutEditing: boolean;
    DisableProfileSubjectsEditing: boolean;
    DisableProfileEditing: boolean;
    DisableSettingsEditing: boolean;
    DisableSplashCustomize: boolean;
    DisableDebugMenu: boolean;
    AllowExitManagement: boolean;
}

const resourceTypes = [
    { key: 'ClassPlans', label: '课表' },
    { key: 'TimeLayouts', label: '时间布局' },
    { key: 'SubjectsSource', label: '科目' },
    { key: 'DefaultSettings', label: '默认设置' },
    { key: 'Policies', label: '策略' },
];

const ConfigurationManagement: React.FC = () => {
    const [tabValue, setTabValue] = useState(0);
    const [configNames, setConfigNames] = useState<string[]>([]);
    const [selectedConfigName, setSelectedConfigName] = useState<string | null>(null);
    const [configContent, setConfigContent] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [snackbarSeverity, setSnackbarSeverity] = useState<'success' | 'error'>('success');
    const [isEditing, setIsEditing] = useState(false);
    const theme = useTheme();
    const isSmDown = useMediaQuery(theme.breakpoints.down('sm'));

    const [policyConfig, setPolicyConfig] = useState<PolicyConfig | null>(null);

    const currentResourceType = resourceTypes[tabValue].key;

    useEffect(() => {
        fetchConfigNames(currentResourceType);
    }, [tabValue, currentResourceType]);

    const fetchConfigNames = async (resourceType: string) => {
        setLoading(true);
        try {
            const response = await apiClient.get(`/api/v1/panel/${resourceType}`);
            setConfigNames(response.data);
            if (response.data.length > 0) {
                setSelectedConfigName(response.data[0]);
            } else {
                setSelectedConfigName(null);
            }
        } catch (error) {
            console.error("Failed to fetch config names:", error);
            setConfigNames([]);
            setSelectedConfigName(null);
            handleSnackbarOpen('获取配置文件列表失败', 'error');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (selectedConfigName) {
            fetchConfigContent(currentResourceType, selectedConfigName);
        } else {
            setConfigContent('');
            setPolicyConfig(null);
        }
    }, [selectedConfigName, currentResourceType]);

    const fetchConfigContent = async (resourceType: string, name: string) => {
        setLoading(true);
        try {
            const response = await apiClient.get(`/api/v1/client/${resourceType}?name=${name}`);
            if (resourceType === 'Policies') {
                setPolicyConfig(response.data);
                setConfigContent('');
            } else {
                setConfigContent(JSON.stringify(response.data, null, 2));
                setPolicyConfig(null);
            }
        } catch (error) {
            console.error("Failed to fetch config content:", error);
            setConfigContent('');
            setPolicyConfig(null);
            handleSnackbarOpen('获取配置文件内容失败', 'error');
        } finally {
            setLoading(false);
        }
    };

    const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
        setTabValue(newValue);
        setSelectedConfigName(null);
        setIsEditing(false);
    };

    const handleConfigNameClick = (name: string) => {
        setSelectedConfigName(name);
        setIsEditing(false);
    };

    const handleSaveConfig = async (content: string) => {
        if (!selectedConfigName) return;
        setLoading(true);
        try {
            await apiClient.post(`/api/resources/${currentResourceType}/${selectedConfigName}`, JSON.parse(content));
            handleSnackbarOpen('配置文件保存成功', 'success');
            setIsEditing(false);
        } catch (error) {
            console.error("Failed to save config:", error);
            handleSnackbarOpen('配置文件保存失败', 'error');
        } finally {
            setLoading(false);
        }
    };

    const handleSavePolicyConfig = async () => {
        if (!selectedConfigName || !policyConfig) return;
        setLoading(true);
        try {
            await apiClient.post(`/api/resources/Policies/${selectedConfigName}`, policyConfig);
            handleSnackbarOpen('策略配置文件保存成功', 'success');
            setIsEditing(false);
        } catch (error) {
            console.error("Failed to save config:", error);
            handleSnackbarOpen('策略配置文件保存失败', 'error');
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

    const handleAddConfig = () => {
        alert('新增配置功能待实现');
    };

    const handleDeleteConfig = () => {
        if (selectedConfigName) {
            alert(`删除配置 ${selectedConfigName} 功能待实现`);
        } else {
            alert('请先选择要删除的配置文件');
        }
    };

    const handlePolicyConfigChange = (key: keyof PolicyConfig, value: boolean) => {
        if (policyConfig) {
            setPolicyConfig({ ...policyConfig, [key]: value });
        }
    };

    const isPolicyTab = currentResourceType === "Policies" && policyConfig !== null;

    return (
        <div>
            <Typography variant="h4" gutterBottom>
                配置管理
            </Typography>

            <Tabs value={tabValue} onChange={handleTabChange} aria-label="resource types tabs">
                {resourceTypes.map((type, index) => (
                    <Tab key={type.key} label={type.label} />
                ))}
            </Tabs>

            <Paper elevation={2} style={{ marginTop: 20, padding: 20 }}>
                <Grid container spacing={isSmDown ? 0 : 2} direction={isSmDown ? "column" : "row"}>
                    <Grid item xs={12} sm={isSmDown ? 12 : 4} md={3}>
                        <Typography variant="h6" gutterBottom>配置文件列表</Typography>
                        {loading && tabValue === tabValue ? (
                            <div style={{ display: 'flex', justifyContent: 'center', margin: '20px 0' }}>
                                <CircularProgress size={24} />
                            </div>
                        ) : (
                            <ListGroup>
                                {configNames.map((name) => (
                                    <ListItem
                                        key={name}
                                        selected={selectedConfigName === name}
                                        onClick={() => handleConfigNameClick(name)}
                                    >
                                        {name}
                                    </ListItem>
                                ))}
                            </ListGroup>
                        )}
                        <Box mt={2}>
                            <Button variant="contained" color="primary" onClick={handleAddConfig} sx={{ mr: 1 }}>
                                新增
                            </Button>
                            <Button variant="outlined" color="error" onClick={handleDeleteConfig} disabled={!selectedConfigName}>
                                删除
                            </Button>
                        </Box>
                    </Grid>

                    <Grid item xs={12} sm={isSmDown ? 12 : 8} md={9}>
                        <Typography variant="h6" gutterBottom>配置文件内容</Typography>
                        {loading && selectedConfigName ? (
                            <div style={{ display: 'flex', justifyContent: 'center', margin: '20px 0' }}>
                                <CircularProgress size={24} />
                            </div>
                        ) : (
                            <>
                            {isPolicyTab? (
                                <FormControl component="fieldset">
                                    <FormGroup>
                                        <FormControlLabel
                                            control={<Switch checked={policyConfig.DisableProfileClassPlanEditing} onChange={(e) => handlePolicyConfigChange('DisableProfileClassPlanEditing', e.target.checked)} />}
                                            label="禁用课表编辑"
                                        />
                                        <FormControlLabel
                                            control={<Switch checked={policyConfig.DisableProfileTimeLayoutEditing} onChange={(e) => handlePolicyConfigChange('DisableProfileTimeLayoutEditing', e.target.checked)} />}
                                            label="禁用时间布局编辑"
                                        />
                                        <FormControlLabel
                                            control={<Switch checked={policyConfig.DisableProfileSubjectsEditing} onChange={(e) => handlePolicyConfigChange('DisableProfileSubjectsEditing', e.target.checked)} />}
                                            label="禁用科目编辑"
                                        />
                                        <FormControlLabel
                                            control={<Switch checked={policyConfig.DisableProfileEditing} onChange={(e) => handlePolicyConfigChange('DisableProfileEditing', e.target.checked)} />}
                                            label="禁用客户端配置编辑"
                                        />
                                        <FormControlLabel
                                            control={<Switch checked={policyConfig.DisableSettingsEditing} onChange={(e) => handlePolicyConfigChange('DisableSettingsEditing', e.target.checked)} />}
                                            label="禁用客户端设置编辑"
                                        />
                                        <FormControlLabel
                                            control={<Switch checked={policyConfig.DisableSplashCustomize} onChange={(e) => handlePolicyConfigChange('DisableSplashCustomize', e.target.checked)} />}
                                            label="禁用客户端启动画面自定义"
                                        />
                                        <FormControlLabel
                                            control={<Switch checked={policyConfig.DisableDebugMenu} onChange={(e) => handlePolicyConfigChange('DisableDebugMenu', e.target.checked)} />}
                                            label="禁用客户端调试菜单"
                                        />
                                        <FormControlLabel
                                            control={<Switch checked={policyConfig.AllowExitManagement} onChange={(e) => handlePolicyConfigChange('AllowExitManagement', e.target.checked)} />}
                                            label="允许客户端退出管理"
                                        />
                                    </FormGroup>
                                    <Button variant="contained" color="primary" onClick={handleSavePolicyConfig} disabled={loading}>
                                            保存
                                    </Button>
                                </FormControl>
                            ) : (
                                <ConfigEditor
                                    value={configContent}
                                    onChange={setConfigContent}
                                    onSave={handleSaveConfig}
                                    isEditing={isEditing}
                                    setIsEditing={setIsEditing}
                                />
                            )}
                            </>
                        )}
                    </Grid>
                </Grid>
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


interface ListGroupProps {
    children: React.ReactNode;
}

const ListGroup: React.FC<ListGroupProps> = ({ children }) => (
    <Paper style={{ maxHeight: 400, overflow: 'auto' }}>
        <Box component="ul" sx={{ listStyle: 'none', p: 1, m: 0 }}>
            {children}
        </Box>
    </Paper>
);


interface ListItemProps {
    children: React.ReactNode;
    selected?: boolean;
    onClick?: () => void;
}

const ListItem: React.FC<ListItemProps> = ({ children, selected, onClick }) => (
    <Box component="li" sx={{
        padding: '8px 16px',
        cursor: 'pointer',
        backgroundColor: selected ? 'action.selected' : 'inherit',
        '&:hover': {
            backgroundColor: 'action.hover',
        },
    }}
        onClick={onClick}
    >
        {children}
    </Box>
);


export default ConfigurationManagement;