# CIMS.py API 文档

[TOC]

## 客户端 API

### 配置文件分发

#### `/api/v1/client/{client_uid}/manifest`

用于获取其它配置文件的配置清单

- 请求方式：`GET`
- 参数：
  - `client_uid`
    - 名称：客户端 UID
    - 类别：字符串
    - 必填：是
  - `version`
    - 名称：版本
    - 类别：整数
    - 必填：否
      - 缺省值：当前时间戳
- 返回：
  - 类别：JSON 数据
    ```json
    {
      "ClassPlanSource": {
        "Value": "http://localhost:50050/api/v1/client/ClassPlan?name=default",
        "Version": 1741685849
      },
      "TimeLayoutSource": {
        "Value": "http://localhost:50050/api/v1/client/TimeLayout?name=default",
        "Version": 1741685849
      },
      "SubjectsSource": {
        "Value": "http://localhost:50050/api/v1/client/Subjects?name=default",
        "Version": 1741685849
      },
      "DefaultSettingsSource": {
        "Value": "http://localhost:50050/api/v1/client/DefaultSettings?name=default",
        "Version": 1741685849
      },
      "PolicySource": {
        "Value": "http://localhost:50050/api/v1/client/Policy?name=default",
        "Version": 1741685849
      },
      "ServerKind": 1,
      "OrganizationName": "CIMS default organization"
    }
    ```
- 错误状态：
  - 无

#### `/api/v1/client/{resource_type}`

用于获取具体的配置文件

- 请求方式：`GET`
- 参数：
  - `resource_type`
    - 名称：资源类型
    - 类别：字符串
    - 必填：是
    - 可选值：`ClassPlan`、`TimeLayout`、`Subjects`、`DefaultSettings`、`Policy`
  - `name`
    - 名称：资源名称
    - 类别：字符串
    - 必填：是
- 返回：
  - 类别：JSON 数据
    ```json
    {
      "key": "value"
    }
    ```
- 错误状态：
  - `404`：资源不存在

## 服务器指令 API

### 配置文件处理

#### `/command/datas/{resource_type}/create`

用于创建配置文件

- 请求方式：`GET`
- 参数：
  - `resource_type`
    - 名称：资源类型
    - 类别：字符串
    - 必填：是
    - 可选值：`ClassPlan`、`DefaultSettings`、`Policy`、`Subjects`、`TimeLayout`
  - `name`
    - 名称：资源名称
    - 类别：字符串
    - 必填：是
- 返回：
  - 类别：无
- 错误状态：
  - `404`：资源类型错误

#### `/command/datas/{resource_type}/delete`

用于删除配置文件

- 请求方式：`GET`、`DELETE`
- 参数：
  - `resource_type`
    - 名称：资源类型
    - 类别：字符串
    - 必填：是
    - 可选值：`ClassPlan`、`DefaultSettings`、`Policy`、`Subjects`、`TimeLayout`
  - `name`
    - 名称：资源名称
    - 类别：字符串
    - 必填：是
- 返回：
  - 类别：无
- 错误状态：
  - `404`：资源类型错误

#### `/command/datas/{resource_type}/list`

用于列出配置文件

- 请求方式：`GET`
- 参数：
  - `resource_type`
    - 名称：资源类型
    - 类别：字符串
    - 必填：是
    - 可选值：`ClassPlan`、`DefaultSettings`、`Policy`、`Subjects`、`TimeLayout`
- 返回：
  - 类别：JSON 数组
    ```json
    [
      "default"
    ]
- 错误状态：
  - `404`：资源类型错误

#### `/command/datas/{resource_type}/rename`

用于重命名配置文件

- 请求方式：`GET`
- 参数：
  - `resource_type`
    - 名称：资源类型
    - 类别：字符串
    - 必填：是
    - 可选值：`ClassPlan`、`DefaultSettings`、`Policy`、`Subjects`、`TimeLayout`
  - `name`
    - 名称：资源名称
    - 类别：字符串
    - 必填：是
  - `target`
    - 名称：目标名称
    - 类别：字符串
    - 必填：是
- 返回：
  - 类别：无
- 错误状态：
  - `404`：资源类型错误

#### `/command/datas/{resource_type}/write`

用于写入配置文件

- 请求方式：`GET`、`POST`、`PUT`
- 参数：
  - `resource_type`
    - 名称：资源类型
    - 类别：字符串
    - 必填：是
    - 可选值：`ClassPlan`、`DefaultSettings`、`Policy`、`Subjects`、`TimeLayout`
  - `name`
    - 名称：资源名称
    - 类别：字符串
    - 必填：是
  - `request`
    - 名称：请求体（即将被写入的配置文件内容）
    - 类别：字符串
    - 必填：是
- 返回：
  - 类别：无
- 错误状态：
  - `404`：资源类型错误

### 服务器配置处理

#### `/command/server/settings`

用于获取服务器配置

- 请求方式：`GET`
- 参数：
  - 无
- 返回：
  - 类别：JSON 数据
    ```json
    {
        "ports": {
            "gRPC": 50051,
            "command": 50052,
            "api": 50050,
            "webui": 50053
        },
        "organization_name": "CMS2.py \u672c\u5730\u6d4b\u8bd5",
        "host": "localhost"
    }
- 错误状态：
  - 无

#### `/command/server/settings`

用于更新服务器配置

- 请求方式：`POST`、`PUT`
- 参数：
  - `request`
    - 名称：请求体（即将被写入的服务器配置文件内容）
    - 类别：字符串
    - 必填：是
- 返回：
  - 类别：无
- 错误状态：
  - 无

### 客户端信息处理

#### `/command/clients/list`

用于列出客户端

- 请求方式：`GET`
- 参数：
  - 无
- 返回：
  - 类别：JSON 数组
    ```json
    [
        "38e1255e-6d15-4972-84be-efd5dfb6ba86"
    ]
    ```
- 错误状态：
  - 无

#### `/command/clients/status`

用于列出客户端状态

- 请求方式：`GET`
- 参数：
  - 无
- 返回：
  - 类别：JSON 数组
    ```json
    [
        {
            "uid": "38e1255e-6d15-4972-84be-efd5dfb6ba86",
            "status": "online"
        }
    ]
    ```
- 错误状态：
  - 无

#### `/command/clients/pre_register`

用于预注册客户端

- 请求方式：`GET`、`POST`

- 参数：
  - `request`
    - 名称：请求体（即将被写入的客户端预注册信息）
    - 类别：字符串
    - 必填：是
- 返回：
  - 类别：无
- 错误状态：
  - 无

### 指令

#### `/command/client/{client_uid}/restart`

用于重启客户端

- 请求方式：`GET`
- 参数：
  - `client_uid`
    - 名称：客户端 UID
    - 类别：字符串
    - 必填：是
- 返回：
  - 类别：无
- 错误状态：
  - 无

#### `/command/client/{client_uid}/send_notification`

用于向客户端发送通知

- 请求方式：`GET`
- 参数：
  - `client_uid`
    - 名称：客户端 UID
    - 类别：字符串
    - 必填：是
  - `message_mask`
    - 名称：消息掩码
    - 类别：字符串
    - 必填：是
  - `message_content`
    - 名称：消息内容
    - 类别：字符串
    - 必填：是
  - `overlay_icon_left`
    - 名称：左侧覆盖图标
    - 类别：整数
    - 必填：否
    - 缺省值：0
  - `overlay_icon_right`
    - 名称：右侧覆盖图标
    - 类别：整数
    - 必填：否
    - 缺省值：0
  - `is_emergency`
    - 名称：是否紧急
    - 类别：布尔值
    - 必填：否
    - 缺省值：`false`
  - `is_speech_enabled`
    - 名称：是否启用语音
    - 类别：布尔值
    - 必填：否
    - 缺省值：`true`
  - `is_effect_enabled`
    - 名称：是否启用特效
    - 类别：布尔值
    - 必填：否
    - 缺省值：`true`
  - `is_sound_enabled`
    - 名称：是否启用声音
    - 类别：布尔值
    - 必填：否
    - 缺省值：`true`
  - `is_topmost`
    - 名称：是否置顶
    - 类别：布尔值
    - 必填：否
    - 缺

