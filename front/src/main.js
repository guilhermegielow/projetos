import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { BootstrapVue3 } from 'bootstrap-vue-3'; // Importando o BootstrapVue
import 'bootstrap/dist/css/bootstrap.min.css'; // Estilos do Bootstrap
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'; // Estilos do BootstrapVue

createApp(App)
  .use(router)
  .use(BootstrapVue3)  // Usando Bootstrap Vue
  .mount('#app');

