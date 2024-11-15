import { createRouter, createWebHistory } from 'vue-router';
import Clientes from '../components/ClientesCrud.vue';
import Projetos from '../components/ProjetosCrud.vue';
import Atividades from '../components/AtividadesCrud.vue';
import ProjetosAbertos from '../components/ProjetosAbertosCrud.vue';

const routes = [
  {
    path: '/clientes',
    name: 'Clientes',
    component: Clientes
  },
  {
    path: '/projetos',
    name: 'Projetos',
    component: Projetos
  },
  {
    path: '/atividades',
    name: 'Atividades',
    component: Atividades
  },
  {
    path: '/projetosabertos',
    name: 'ProjetosAbertos',
    component: ProjetosAbertos
  },
  {
    path: '/',
    redirect: '/atividades'  // Redireciona para a página inicial de Clientes
  }
];

// Criando o router com a configuração
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL), // Usando o createWebHistory para navegação sem hash
  routes
});

export default router;