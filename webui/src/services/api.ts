  // API 请求封装
import { ClientManifest } from '../types';

const API_BASE = '/api/v1';

// 获取客户端配置清单
export async function getClientManifest(uid: string): Promise<ClientManifest> {
    const response = await fetch(`${API_BASE}/client/${uid}/manifest`);
    if (!response.ok) {
        throw new Error(`获取客户端清单失败: ${response.status}`);
    }
    return await response.json();
}

// 获取具体的配置文件
export async function getConfigFile(url:string){
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`获取配置文件失败: ${response.status}`);
    }
    return await response.text();
}
// 获取资源列表 ClassPlans, DefaultSettings, Policies, SubjectsSource, TimeLayouts
export async function getPanelResource(resourceType: string): Promise<string[]> {
  const response = await fetch(`${API_BASE}/panel/${resourceType}`);
  if (!response.ok) {
    throw new Error(`获取${resourceType}失败: ${response.status}`);
  }
  return await response.json();
}

// 保存配置文件
export async function saveConfigFile(resourceType: string, name: string, content: string): Promise<void> {
    const response = await fetch(`/api/resources/${resourceType}/${name}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content }),
    });
    if (!response.ok) {
        throw new Error(`保存配置文件失败: ${response.status}`);
    }
}
  // 其他 API 请求...