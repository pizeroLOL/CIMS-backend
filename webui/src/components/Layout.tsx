import React from 'react';
import { styled, useTheme, Theme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import MuiDrawer from '@mui/material/Drawer';
import CssBaseline from '@mui/material/CssBaseline';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import DashboardIcon from '@mui/icons-material/Dashboard';
import DevicesIcon from '@mui/icons-material/Devices';
import SettingsIcon from '@mui/icons-material/Settings';
import ImageIcon from '@mui/icons-material/Image';
import { Link, useLocation } from 'react-router-dom';
import { Description as DescriptionIcon } from '@mui/icons-material';
import useMediaQuery from '@mui/material/useMediaQuery';
import { CSSProperties } from 'react';
import MuiAppBar from '@mui/material/AppBar';

const drawerWidth = 240;

const openedMixin = (theme: Theme): CSSProperties => ({
    width: drawerWidth,
    transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
    }),
    overflowX: 'hidden',
});

const closedMixin = (theme: Theme): CSSProperties => ({
    transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }),
    overflowX: 'hidden',
    width: `calc(${theme.spacing(7)} + 1px)`,
    [theme.breakpoints.up('sm')]: {
        width: `calc(${theme.spacing(9)} + 1px)`,
    },
});

const DrawerHeader = styled('div')(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: theme.spacing(0, 1),
    // necessary for content to be below app bar
    ...theme.mixins.toolbar,
}));


const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open'
})<{ open?: boolean }>(({ theme, open }) => ({ // Define props directly in styled call
    zIndex: theme.zIndex.drawer + 1,
    width: `calc(100% - ${open ? drawerWidth : `calc(${theme.spacing(9)} + 1px)`})`,
    marginLeft: `${open ? drawerWidth : `calc(${theme.spacing(9)} + 1px)`}`,
}));


const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })<{ open?: boolean }>( // Define props directly in styled call
    ({ theme, open }) => ({
        width: drawerWidth,
        flexShrink: 0,
        whiteSpace: 'nowrap',
        boxSizing: 'border-box',
        ...(open && openedMixin(theme)),
        ...(!open && closedMixin(theme)),
        '& .MuiDrawer-paper': {
            ...(open && openedMixin(theme)),
            ...(!open && closedMixin(theme)),
        },
    }),
);


const Main = styled('main', { shouldForwardProp: (prop) => prop !== 'open' })<{ open?: boolean }>( // Define props directly in styled call
    ({ theme, open }) => ({
        flexGrow: 1,
        padding: theme.spacing(3),
        transition: theme.transitions.create('margin', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
        }),
        marginLeft: `- ${drawerWidth}px`,
        ...(open && {
            transition: theme.transitions.create('margin', {
                easing: theme.transitions.easing.easeOut,
                duration: theme.transitions.duration.enteringScreen,
            }),
            marginLeft: 0,
        }),
        marginTop: '0px',
    }),
);


interface LayoutProps {
    children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
    const location = useLocation();
    const theme = useTheme();
    const isSmUp = useMediaQuery(theme.breakpoints.up('sm'));
    const [open, setOpen] = React.useState(isSmUp);

    React.useEffect(() => {
        setOpen(isSmUp);
    }, [isSmUp]);


    const version = {
        server: '0.1.1.34(build 19)',
        webui: '0.3.1.5(build 77)',
    };

    const menuItems = [
        { text: '概览', icon: <DashboardIcon />, path: '/' },
        { text: '设备管理', icon: <DevicesIcon />, path: '/devices' },
        { text: '配置管理', icon: <DescriptionIcon />, path: '/configs' },
        { text: '设置', icon: <SettingsIcon />, path: '/settings' },
    ];


    const logoUrl = new URL('../assets/logo.png', import.meta.url).href;


    return (
        <Box sx={{ display: 'flex' }}>
            <CssBaseline />
            <AppBar position="fixed" open={open} > {/* Pass 'open' prop here */}
                <Toolbar>
                    {/* Removed the Typography component with the title from here */}
                </Toolbar>
            </AppBar>
            <Drawer variant="permanent" open={open} PaperProps={{ sx: { position: 'relative' } }}> {/* Pass 'open' prop here */}
                <Toolbar />
                <DrawerHeader sx={{ flexDirection: 'column', alignItems: 'flex-start', padding: 2, display: 'flex', justifyContent: 'center' }}>
                    <Box component="img" src={logoUrl} alt="Logo" sx={{ height: 50, mb: 1 }} />
                    <Typography variant="h6" noWrap component="div" sx={{ fontWeight: 'bold', textAlign: 'center' }}>
                        ClassIsland
                    </Typography>
                    <Typography variant="body2" noWrap component="div" sx={{ textAlign: 'center' }}>
                        集控控制台
                    </Typography>
                </DrawerHeader>
                <Divider />
                <List>
                    {menuItems.map((item, index) => (
                        <ListItem key={item.text} disablePadding sx={{ display: 'block' }}>
                            <ListItemButton
                                component={Link}
                                to={item.path}
                                selected={location.pathname === item.path}
                                sx={{
                                    minHeight: 48,
                                    justifyContent: open ? 'initial' : 'center',
                                    px: 2.5,
                                }}
                            >
                                <ListItemIcon
                                    sx={{
                                        minWidth: 0,
                                        mr: open ? 3 : 'auto',
                                        justifyContent: 'center',
                                    }}
                                >
                                    {item.icon}
                                </ListItemIcon>
                                <ListItemText primary={item.text} sx={{ opacity: open ? 1 : 0 }} />
                            </ListItemButton>
                        </ListItem>
                    ))}
                </List>
                <Divider />
                <Box sx={{ mt: 'auto', p: 2, textAlign: 'center', fontSize: '0.8rem', color: 'text.secondary', opacity: open ? 1 : 0 }}>
                    <Box sx={{ display: 'block' }}> {/* 使用 Box 包裹服务器版本，并设置 display: 'block' */}
                        <Typography variant="caption">服务器版本: {version.server}</Typography>
                    </Box>
                    <Box sx={{ display: 'block' }}> {/* 使用 Box 包裹 WebUI 版本，并设置 display: 'block' */}
                        <Typography variant="caption">WebUI 版本: {version.webui}</Typography>
                    </Box>
                </Box>
            </Drawer>
            <Main open={open}> {/* Pass 'open' prop here */}
                <DrawerHeader />
                {children}
            </Main>
        </Box>
    );
};