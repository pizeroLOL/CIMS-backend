import React from 'react';
import { Dialog, DialogTrigger, DialogSurface, DialogTitle, DialogBody, Text, Button,  Divider, Input } from '@fluentui/react-components'; // 导入 Input
import { restartClient, sendNotification, updateClient } from '../services/command';

export interface DeviceCardProps {
    clientUid: string;
    clientName:string;
    onClose: () => void;
  }

export const DeviceCard: React.FC<DeviceCardProps> = ({ clientUid, clientName, onClose }) => {
    const [notifyOpen, setNotifyOpen] = React.useState(false);
    const [messageTitle, setMessageTitle] = React.useState("");
    const [messageContent, setMessageContent] = React.useState("");

    const handleRestart = async () => {
      try {
        await restartClient(clientUid);
        alert('已发送重启指令');
      } catch (error) {
        console.error('重启失败:', error);
        alert('重启失败');
      }
    };

    const handleUpdate = async () => {
      try {
        await updateClient(clientUid);
        alert('已发送更新指令');
      } catch (error) {
        console.error('更新失败:', error);
        alert('更新失败');
      }
    };

    const handleNotify = async ()=>{
        try{
            await sendNotification(clientUid, messageTitle, messageContent)
            setNotifyOpen(false)
            alert("发送成功")
        }catch(err){
            console.error("发送失败", err)
            alert("发送失败")
        }
    }
    return (
        <>
            <Dialog modalType={undefined}>
                <DialogSurface style={{width:'80%',maxWidth:800}} >
                    <DialogTitle>{clientName} - 操作</DialogTitle>
                    <DialogBody>
                        <div style={{display:'flex', flexDirection:"column", gap:10}}>
                            <Text><b>UID:</b> {clientUid}</Text>
                            <Button appearance='primary' onClick={handleRestart}>重启客户端</Button>
                            <Button onClick={handleUpdate}>更新客户端配置</Button>
                            <DialogTrigger disableButtonEnhancement>
                                <Button onClick={()=>setNotifyOpen(true)}>发送通知</Button>
                            </DialogTrigger>
                            <Divider />
                            <Button appearance='secondary' onClick={onClose}>关闭</Button>
                        </div>
                    </DialogBody>
                </DialogSurface>
                <Dialog open={notifyOpen} onOpenChange={(_,data)=>{setNotifyOpen(data.open)}}>
                    <DialogSurface style={{width:'80%',maxWidth:500}}>
                        <DialogTitle>发送通知到 {clientName}</DialogTitle>
                        <DialogBody>
                            <div style={{display:'flex', flexDirection:"column", gap:8}}>
                                <Input placeholder='通知标题' value={messageTitle} onChange={(_,{value})=>{setMessageTitle(value)}}/>
                                <Input placeholder='通知正文' value={messageContent} onChange={(_,{value})=>{setMessageContent(value)}}/>
                                <div style={{display:'flex', gap:8}}>
                                    <Button appearance='primary' onClick={handleNotify}>发送</Button>
                                    <Button appearance='secondary' onClick={()=>setNotifyOpen(false)}>取消</Button>
                                </div>
                            </div>
                        </DialogBody>
                    </DialogSurface>
                </Dialog>
            </Dialog>
        </>
    );
};