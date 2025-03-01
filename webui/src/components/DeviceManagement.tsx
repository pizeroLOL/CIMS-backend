import React, { useState, useEffect, useMemo } from 'react';
import { getClientList, getClientStatus } from '../services/command';
import { ClientList, ClientStatusList } from '../types';
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableCell,
  Input,
  Button,
  Select,
  Option,
  Toolbar,
  Checkbox,
  Text
} from '@fluentui/react-components';
import { DeviceCard } from './DeviceCard';
import { BulkActionPanel } from './BulkActionPanel';

function DeviceManagement() {
  const [clients, setClients] = useState<ClientList>({});
  const [status, setStatus] = useState<ClientStatusList>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'online' | 'offline'>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedClients, setSelectedClients] = useState<string[]>([]);
  const [bulkActionOpen, setBulkActionOpen] = useState(false);
  const [cardViewOpen, setCardViewOpen] = useState("")

  useEffect(() => {
    const fetchData = async () => {
      try {
        const clientList = await getClientList();
        const clientStatus = await getClientStatus();
        setClients(clientList);
        setStatus(clientStatus);
        setLoading(false);
      } catch (err: any) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchData();
    const intervalId = setInterval(fetchData, 10000)
    return () => clearInterval(intervalId)
  }, []);

  const filteredClients = useMemo(() => {
    return Object.entries(clients)
      .filter(([uid, name]) => {
        // 搜索过滤
        const searchLower = searchQuery.toLowerCase();
        if (!name.toLowerCase().includes(searchLower) && !uid.toLowerCase().includes(searchLower)) {
          return false;
        }
        // 状态过滤
        if (filter === 'online' && !status[uid]?.isOnline) {
          return false;
        }
        if (filter === 'offline' && status[uid]?.isOnline) {
          return false;
        }

        return true;
      });
  }, [clients, status, filter, searchQuery]);

    const handleSelectClient = (uid: string) => {
    setSelectedClients((prevSelected) =>
      prevSelected.includes(uid) ? prevSelected.filter((id) => id !== uid) : [...prevSelected, uid]
    );
  };

  const handleSelectAll = (isChecked: false | true | "mixed") => { // 明确 isChecked 的类型
    if (isChecked) {
      setSelectedClients(filteredClients.map(([uid]) => uid));
    } else {
      setSelectedClients([]);
    }
  };
  const handleBulkActionClose = () => {
    setBulkActionOpen(false)
    setSelectedClients([])
  }

  const handleOpenCard = (uid: string) => {
    setCardViewOpen(uid)
  }

  if (loading) {
    return <div>加载中...</div>;
  }

  if (error) {
    return <div>错误: {error}</div>;
  }

  return (
    <div>
      <Text size={600}>设备管理</Text>

      {/* 搜索和筛选工具栏 */}
      <Toolbar>
        <div style={{ width: '100%', display: 'flex', gap: 8 }}>
          <div style={{ flexGrow: 1 }}>
            <Input
              placeholder="搜索客户端名称或 UID"
              value={searchQuery}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSearchQuery(e.target.value)} // 添加类型
              style={{ width: '100%' }}
            />
          </div>
          <Select
            value={filter}
            onChange={(e, data) => setFilter(data.value as 'all' | 'online' | 'offline')}
          >
            <Option value="all">所有</Option>
            <Option value="online">在线</Option>
            <Option value="offline">离线</Option>
          </Select>
          <Button onClick={() => setBulkActionOpen(true)} disabled={selectedClients.length === 0}>批量操作</Button>
        </div>
      </Toolbar>
      <BulkActionPanel
        open={bulkActionOpen}
        onClose={handleBulkActionClose}
        selectedClients={selectedClients}
      />
      {/* 表格 */}
      <Table>
        <TableHeader>
          <TableRow>
            <TableCell>
              <Checkbox
                checked={selectedClients.length === filteredClients.length && filteredClients.length > 0}
                onChange={(_, data) => handleSelectAll(data.checked)}
              />选择
            </TableCell>
            <TableCell>客户端名称</TableCell>
            <TableCell>UID</TableCell>
            <TableCell>状态</TableCell>
            <TableCell>操作</TableCell>
          </TableRow>
        </TableHeader>
        <TableBody>
          {filteredClients.map(([uid, name]) => (
            <>
              <TableRow key={uid}>
                <TableCell>
                  <Checkbox checked={selectedClients.includes(uid)} onChange={() => handleSelectClient(uid)} />
                </TableCell>
                <TableCell>{name}</TableCell>
                <TableCell>{uid}</TableCell>
                <TableCell>{status[uid]?.isOnline ? '在线' : '离线'}</TableCell>
                <TableCell>
                  <Button onClick={() => handleOpenCard(uid)}>查看详情</Button>
                </TableCell>
              </TableRow>
            </>
          ))}
        </TableBody>
      </Table>
      {cardViewOpen !== "" && (<DeviceCard clientUid={cardViewOpen} clientName={clients[cardViewOpen]} onClose={() => setCardViewOpen("")} />)}
    </div>
  );
}

export default DeviceManagement;