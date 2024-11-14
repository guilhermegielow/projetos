<template>
    <b-navbar toggleable="lg" variant="blue" bg="primary">
      <b-navbar-brand href="#">Projeto</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <!-- Menu de navegação -->
          <b-nav-item to="/clientes">Clientes</b-nav-item>
          <b-nav-item to="/projetos">Projetos</b-nav-item>
          <b-nav-item to="/atividades">Atividades</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </template>
  
  <script>
  // Importando os componentes do bootstrap-vue-3
  import { BNavbar, BNavbarBrand, BNavbarToggle, BCollapse, BNavbarNav, BNavItem } from 'bootstrap-vue-3';
  
  export default {
    components: {
      BNavbar,
      BNavbarBrand,
      BNavbarToggle,
      BCollapse,
      BNavbarNav,
      BNavItem
    }
  };
  </script>
  