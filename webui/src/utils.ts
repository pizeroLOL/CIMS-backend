// 工具函数

// 格式化时间戳
export function formatTimestamp(timestamp: number): string {
    const date = new Date(timestamp * 1000);
    return date.toLocaleString();
  }

  // 其他工具函数...