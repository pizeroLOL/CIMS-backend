import { ClientList, ClientStatusList } from '../types';
// Command 请求封装

const COMMAND_BASE = '/command';

// 获取已注册的设备清单
export async function getClientList(): Promise<ClientList> {
  const response = await fetch(`${COMMAND_BASE}/clients`);
  if (!response.ok) {
    throw new Error(`获取客户端列表失败: ${response.status}`);
  }
  return await response.json();
}

// 获取设备状态
export async function getClientStatus(): Promise<ClientStatusList> {
  const response = await fetch(`${COMMAND_BASE}/clients/status`);
  if (!response.ok) {
    throw new Error(`获取客户端状态失败: ${response.status}`);
  }
  return await response.json();
}

// 重启客户端
export async function restartClient(clientUid: string): Promise<void> {
    const response = await fetch(`${COMMAND_BASE}/clients/${clientUid}/restart`);
    if (!response.ok) {
        throw new Error(`重启客户端失败: ${response.status}`);
    }
}

// 发送通知
export async function sendNotification(
    clientUid: string,
    messageMask: string,
    messageContent: string,
    overlayIconLeft: number = 0,
    overlayIconRight: number = 0,
    isEmergency: boolean = false,
    isSpeechEnabled: boolean = true,
    isEffectEnabled: boolean = true,
    isSoundEnabled: boolean = true,
    isTopmost: boolean = true,
    durationSeconds: number = 5.0,
    repeatCounts: number = 1
): Promise<void> {
    const response = await fetch(`${COMMAND_BASE}/clients/${clientUid}/notify`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message_mask: messageMask,
          message_content: messageContent,
          overlay_icon_left: overlayIconLeft,
          overlay_icon_right: overlayIconRight,
          is_emergency: isEmergency,
          is_speech_enabled: isSpeechEnabled,
          is_effect_enabled: isEffectEnabled,
          is_sound_enabled: isSoundEnabled,
          is_topmost: isTopmost,
          duration_seconds: durationSeconds,
          repeat_counts: repeatCounts,
        }),
      });
      if (!response.ok) {
        throw new Error(`发送通知失败: ${response.status}`);
      }
}

// 要求客户端更新
export async function updateClient(clientUid: string): Promise<void> {
  const response = await fetch(`${COMMAND_BASE}/clients/${clientUid}/update`);
    if (!response.ok) {
        throw new Error(`更新客户端失败: ${response.status}`);
    }
}