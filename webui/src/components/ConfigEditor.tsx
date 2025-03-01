import React, { useState, useEffect } from 'react';
import { Dialog,  DialogSurface, DialogTitle, DialogBody, Textarea, Button,  } from '@fluentui/react-components';
import { saveConfigFile, getConfigFile } from '../services/api';

interface ConfigEditorProps {
    resourceType: string;
    name: string;
    content?:string;
    onClose: () => void;
}

export const ConfigEditor: React.FC<ConfigEditorProps> = ({ resourceType, name, onClose, content }) => {
  const [configContent, setConfigContent] = useState(content || '');
    const [loading, setLoading] = useState(false)

    useEffect(()=>{
        const fetchData = async ()=>{
            if(content === ""){
                try{
                    const realUrl = `/api/v1/client/${resourceType.toLowerCase()}?name=${name}`
                    const res = await getConfigFile(realUrl)
                    setConfigContent(res)
                    setLoading(false)
                }catch(err){
                    console.error("获取配置失败",err)
                    alert("获取配置失败")
                    onClose()
                }
            }
        }
        if (name !== "new"){
            setLoading(true)
            fetchData()
        }
    },[])

  const handleSave = async () => {
    try {
      await saveConfigFile(resourceType, name, configContent);
      alert('保存成功');
      onClose();
    } catch (error) {
      console.error('保存失败:', error);
      alert('保存失败');
    }
  };
    if(loading){
        return <div>加载中...</div>
    }

  return (
        <Dialog modalType={undefined}>
            <DialogSurface style={{width:'80%',maxWidth:800}}>
                <DialogTitle>{resourceType} - {name}</DialogTitle>
                <DialogBody>
                    <div style={{display:'flex', flexDirection:'column', gap:8}}>
                        <Textarea
                            value={configContent}
                            onChange={(e) => setConfigContent(e.target.value)}
                            style={{height:300}}
                        />
                         <div style={{display:'flex', gap:8}}>
                            <Button appearance='primary' onClick={handleSave}>保存</Button>
                            <Button appearance='secondary' onClick={onClose}>取消</Button>
                        </div>
                    </div>
                </DialogBody>
            </DialogSurface>
        </Dialog>
  );
};