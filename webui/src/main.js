import { createApp } from 'vue'
// import { setTheme } from '@fluentui/web-components';
// import { webLightTheme } from '@fluentui/tokens';
import App from './App.vue'
import router from './router'
// import '@fluentui/web-components/button.js'

// setTheme(webLightTheme);

createApp(App).use(router).mount('#app')