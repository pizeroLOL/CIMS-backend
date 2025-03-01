import React, { useState } from 'react';
import { Dialog,  DialogSurface, DialogTitle, DialogBody, Button,  Text, Input } from '@fluentui/react-components'; // 导入 Input
import { restartClient, sendNotification, updateClient } from '../services/command';

interface BulkActionPanelProps {
  open: boolean;
  onClose: () => void;
  selectedClients: string[];
}

export const BulkActionPanel: React.FC<BulkActionPanelProps> = ({ open, onClose, selectedClients }) => {
    const [notifyOpen, setNotifyOpen] = useState(false)
    const [messageTitle, setMessageTitle] = React.useState("");
    const [messageContent, setMessageContent] = React.useState("");

  const handleRestartSelected = async () => {
    try {
      await Promise.all(selectedClients.map(uid => restartClient(uid)));
      alert('已发送重启指令');
      onClose();
    } catch (error) {
      console.error('重启失败:', error);
      alert('重启失败');
    }
  };

  const handleUpdateSelected = async () => {
    try {
      await Promise.all(selectedClients.map(uid => updateClient(uid)));
      alert('已发送更新指令');
      onClose();
    } catch (error) {
      console.error('更新失败:', error);
      alert('更新失败');
    }
  };
  const handleNotify = async ()=>{
    try{
        await Promise.all(selectedClients.map(uid=> sendNotification(uid, messageTitle, messageContent)))
        setNotifyOpen(false)
        onClose()
        alert("发送成功")
    }catch(err){
        console.error("发送失败", err)
        alert("发送失败")
    }
}

  return (
    <>
        <Dialog modalType={undefined} open={open}>
            <DialogSurface style={{width:'80%',maxWidth:800}}>
                <DialogTitle>批量操作 ({selectedClients.length} 个客户端已选择)</DialogTitle>
                <DialogBody>
                    <div style={{display:'flex', flexDirection:'column', gap:8}}>
                        <Button appearance='primary' onClick={handleRestartSelected}>重启所选客户端</Button>
                        <Button onClick={handleUpdateSelected}>更新所选客户端配置</Button>
                        <div>
                            <Button onClick={()=>setNotifyOpen(true)}>发送通知</Button>
                        </div>
                        <Button appearance='secondary' onClick={onClose}>取消</Button>
                    </div>
                </DialogBody>
            </DialogSurface>
            <Dialog open={notifyOpen} onOpenChange={(_,data)=>{setNotifyOpen(data.open)}}>
                <DialogSurface style={{width:'80%',maxWidth:500}}>
                    <DialogTitle>发送通知到 {selectedClients.length} 个客户端</DialogTitle>
                    <DialogBody>
                        <div style={{display:'flex', flexDirection:"column", gap:8}}>
                            <Input placeholder='通知标题' value={messageTitle} onChange={(_, {value})=>setMessageTitle(value)}/>
                            <Input placeholder='通知正文' value={messageContent} onChange={(_, {value})=>setMessageContent(value)}/>
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