import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './styles/global.css';
import { FluentProvider, teamsLightTheme } from '@fluentui/react-components'

const root = createRoot(document.getElementById('root')!);
root.render(
    <React.StrictMode>
        <FluentProvider theme={teamsLightTheme}>
            <App />
        </FluentProvider>
    </React.StrictMode>
);