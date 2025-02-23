# Class Island Management WebUI

基于 Vue.js 的集控管理 Web UI。

## 开发运行

1.  确保已安装 Node.js 和 npm 或 yarn。
2.  进入 `webui` 目录: `cd webui`
3.  安装依赖: `npm install` 或 `yarn install`
4.  启动开发服务器: `npm run serve` 或 `yarn serve`
5.  在浏览器中访问 `http://localhost:50053`

## 构建生产版本

1.  在 `webui` 目录中运行: `npm run build` 或 `yarn build`
2.  构建产物在项目根目录的 `dist_webui` 文件夹中。

## 配置说明

-   `package.json`: 项目依赖和脚本。
-   `vue.config.js`: Vue CLI 配置文件，包含了端口、代理等配置。
-   `public/index.html`: HTML 入口文件。
-   `src/main.js`: Vue 应用入口 JS 文件，导入和配置 Vue Router、Element Plus 等。
-   `src/App.vue`: 根组件。
-   `src/components`: 组件目录。
-   `src/router`: Vue Router 配置文件目录 (如果使用路由)。

更多详细配置请参考 Vue CLI 文档。