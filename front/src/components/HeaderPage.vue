<template>
  <div class="header">
    <div class="container">
      <div class="title">Sistema de Gestão</div>
      <div class="menu">
        <a 
          v-for="(menu, index) in menus" 
          :key="menu.name" 
          :href="menu.link" 
          class="menu-item"
          :class="{'active': activeMenuIndex === index}" 
          @click="setActiveMenu(index)"
        >
          {{ menu.name }}
        </a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeMenuIndex: null,  // Índice do menu ativo
      menus: [
        { name: "Início", link: "/" },
        { name: "Clientes", link: "/clientes" },
        { name: "Projetos", link: "/projetos" },
        { name: "Atividades", link: "/atividades" },
        { name: "Projetos em Aberto e Atividades", link: "/projetosabertos" },
      ],
    };
  },
  methods: {
    // Definir o menu ativo
    setActiveMenu(index) {
      this.activeMenuIndex = index;
    },
  },
};
</script>

<style scoped>
.header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  padding: 10px 20px;
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
}

.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 1.2em;
  font-weight: bold;
  color: #343a40;
}

.menu-item {
  color: #007bff;
  font-size: 0.9em;
  text-decoration: none;
  padding: 5px 10px;
  margin-left: 10px;
  border: 1px solid #007bff;
  border-radius: 3px;
  transition: all 0.3s ease;
}

.menu-item:hover {
  background-color: #007bff;
  color: white;
}

/* Classe para o item ativo */
.menu-item.active {
  color: black !important;  /* Altera a cor do texto para preto */
  font-weight: bold;  /* Opcional: Deixa o texto em negrito */
  border-color: black;  /* Altera a borda para preta */
  background-color: #f0f0f0;  /* Altera a cor de fundo quando ativo */
}
</style>
