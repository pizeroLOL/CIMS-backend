// 类型定义文件
export interface ClientManifest {
    ClassPlanSource: { Value: string; Version: number };
    TimeLayoutSource: { Value: string; Version: number };
    SubjectsSource: { Value: string; Version: number };
    DefaultSettingsSource: { Value: string; Version: number };
    PolicySource: { Value: string; Version: number };
    ServerKind: number;
    OrganizationName: string;
  }

  export interface ClientStatus {
    isOnline: boolean;
    lastHeartbeat: number;
  }

  export interface ClientList {
    [uid: string]: string; // uid: clientName
  }

  export interface ClientStatusList {
    [uid: string]: ClientStatus;
  }


  // 可以根据需要添加更多类型定义