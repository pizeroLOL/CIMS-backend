import React, { useState, useEffect } from 'react';
import { getPanelResource } from '../services/api';
import { Text, Button, TabList, Tab } from '@fluentui/react-components'; // 正确导入 TabList, Tab
import { ConfigEditor } from './ConfigEditor';

function ConfigManagement() {
    const [classPlans, setClassPlans] = useState<string[]>([]);
    const [defaultSettings, setDefaultSettings] = useState<string[]>([]);
    const [policies, setPolicies] = useState<string[]>([]);
    const [subjects, setSubjects] = useState<string[]>([]);
    const [timeLayouts, setTimeLayouts] = useState<string[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [activeTabValue, setActiveTabValue] = useState<
        'ClassPlans' | 'DefaultSettings' | 'Policies' | 'SubjectsSource' | 'TimeLayouts'
    >('ClassPlans'); // 使用 activeTabValue 跟踪当前激活的 Tab 的 value
    const [editConfig, setEditConfig] = useState<{
        resourceType: string;
        name: string;
        content: string;
    } | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const classPlansData = await getPanelResource('ClassPlans');
                const defaultSettingsData = await getPanelResource('DefaultSettings');
                const policiesData = await getPanelResource('Policies');
                const subjectsData = await getPanelResource('SubjectsSource');
                const timeLayoutsData = await getPanelResource('TimeLayouts');

                setClassPlans(classPlansData);
                setDefaultSettings(defaultSettingsData);
                setPolicies(policiesData);
                setSubjects(subjectsData);
                setTimeLayouts(timeLayoutsData);
                setLoading(false);
            } catch (err: any) {
                setError(err.message);
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return <div>加载中...</div>;
    }

    if (error) {
        return <div>错误: {error}</div>;
    }

    const handleEdit = (resourceType: string, name: string, content: string) => {
        setEditConfig({ resourceType, name, content });
    };

    // 根据 activeTabValue 渲染不同的内容
    const renderTabContent = () => {
        switch (activeTabValue) {
            case 'ClassPlans':
                return (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                        <Button onClick={() => handleEdit('ClassPlans', 'new', '')}>添加</Button>
                        {classPlans.map((name) => (
                            <div style={{ display: 'flex', gap: 8, alignItems: 'center' }} key={name}>
                                <Text block style={{ flexGrow: 1 }}>
                                    {name}
                                </Text>
                                <Button onClick={() => handleEdit('ClassPlans', name, '')}>编辑</Button>
                            </div>
                        ))}
                    </div>
                );
            case 'DefaultSettings':
                return (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                        <Button onClick={() => handleEdit('DefaultSettings', 'new', '')}>添加</Button>
                        {defaultSettings.map((name) => (
                            <div style={{ display: 'flex', gap: 8, alignItems: 'center' }} key={name}>
                                <Text block style={{ flexGrow: 1 }}>
                                    {name}
                                </Text>
                                <Button onClick={() => handleEdit('DefaultSettings', name, '')}>编辑</Button>
                            </div>
                        ))}
                    </div>
                );
            case 'Policies':
                return (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                        <Button onClick={() => handleEdit('Policies', 'new', '')}>添加</Button>
                        {policies.map((name) => (
                            <div style={{ display: 'flex', gap: 8, alignItems: 'center' }} key={name}>
                                <Text block style={{ flexGrow: 1 }}>
                                    {name}
                                </Text>
                                <Button onClick={() => handleEdit('Policies', name, '')}>编辑</Button>
                            </div>
                        ))}
                    </div>
                );
            case 'SubjectsSource':
                return (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                        <Button onClick={() => handleEdit('SubjectsSource', 'new', '')}>添加</Button>
                        {subjects.map((name) => (
                            <div style={{ display: 'flex', gap: 8, alignItems: 'center' }} key={name}>
                                <Text block style={{ flexGrow: 1 }}>
                                    {name}
                                </Text>
                                <Button onClick={() => handleEdit('SubjectsSource', name, '')}>编辑</Button>
                            </div>
                        ))}
                    </div>
                );
            case 'TimeLayouts':
                return (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                        <Button onClick={() => handleEdit('TimeLayouts', 'new', '')}>添加</Button>
                        {timeLayouts.map((name) => (
                            <div style={{ display: 'flex', gap: 8, alignItems: 'center' }} key={name}>
                                <Text block style={{ flexGrow: 1 }}>
                                    {name}
                                </Text>
                                <Button onClick={() => handleEdit('TimeLayouts', name, '')}>编辑</Button>
                            </div>
                        ))}
                    </div>
                );
            default:
                return null;
        }
    };

    return (
        <div>
            <Text size={600}>配置管理</Text>
            <TabList> {/* 注意这里的 onTabChange */}
                <Tab value="ClassPlans">课程表</Tab>
                <Tab value="DefaultSettings">默认设置</Tab>
                <Tab value="Policies">策略</Tab>
                <Tab value="SubjectsSource">科目</Tab>
                <Tab value="TimeLayouts">时间安排</Tab>
            </TabList>
            {renderTabContent()}
            {editConfig && (
                <ConfigEditor
                    resourceType={editConfig.resourceType}
                    name={editConfig.name}
                    content={editConfig.content}
                    onClose={() => setEditConfig(null)}
                />
            )}
        </div>
    );
}

export default ConfigManagement;