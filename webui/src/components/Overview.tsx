import React, { useState, useEffect } from 'react';
import { getClientList, getClientStatus } from '../services/command';
import { Card, Text, Spinner, Divider, Badge } from '@fluentui/react-components';
import { formatTimestamp } from '../utils';
import { ClientList, ClientStatusList } from '../types';
function Overview() {
    const [clientCount, setClientCount] = useState<number>(0);
    const [onlineClientCount, setOnlineClientCount] = useState<number>(0);
    const [loading, setLoading] = useState<boolean>(true);
    const [clientList, setClientList] = useState<ClientList>({});
    const [clientStatusList, setClientStatusList] = useState<ClientStatusList>({})

    useEffect(() => {
        const fetchData = async () => {
            try {
                const clients = await getClientList();
                const status = await getClientStatus();
                setClientList(clients)
                setClientStatusList(status)
                setClientCount(Object.keys(clients).length);
                setOnlineClientCount(Object.values(status).filter(s => s.isOnline).length);
                setLoading(false);
            } catch (error) {
                console.error("获取数据失败:", error);
                setLoading(false);
            }
        };

        fetchData();
        const intervalId = setInterval(fetchData, 10000); // 每 10 秒刷新一次
        return () => clearInterval(intervalId)
    }, []);

    return (
        <div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 16 }}>
                <Card style={{ maxWidth: 350 }}>
                    <div> {/* 直接使用 div, 不再使用 Card.Section */}
                        <Text size={600}>已注册客户端数量</Text>
                        {loading ? <Spinner /> : <Text size={800}>{clientCount}</Text>}
                    </div>
                </Card>
                <Card style={{ maxWidth: 350 }}>
                    <div>
                        <Text size={600}>在线客户端数量</Text>
                        {loading ? <Spinner /> : <Text size={800}>{onlineClientCount}</Text>}
                    </div>
                </Card>

            </div>
            <Divider />
            <Text size={600}>客户端状态列表</Text>
            {loading ? (<Spinner />) : (
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 16 }}>
                    {
                        Object.keys(clientList).map((uid) => (
                            <Card key={uid} style={{ maxWidth: 350 }} className='card'>
                                <div>
                                    <div style={{ display: 'flex', alignItems: 'center' }}>
                                        <div style={{ flexGrow: 1 }}>
                                            <Text block size={600}>{clientList[uid]}({uid})</Text>
                                        </div>
                                        {clientStatusList[uid].isOnline ? (
                                            <Badge>在线</Badge>
                                        ) : (
                                            <Badge>离线</Badge>
                                        )}
                                    </div>

                                    <Text>最后心跳时间：{formatTimestamp(clientStatusList[uid].lastHeartbeat)}</Text>
                                </div>
                            </Card>
                        ))
                    }
                </div>
            )}
        </div>
    );
}

export default Overview;