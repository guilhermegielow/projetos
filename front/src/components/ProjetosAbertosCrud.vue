<template>
    <div class="container">
      <h1 class="text-center">Projetos em Aberto</h1>
  
      <!-- Lista de Projetos -->
      <div v-for="projeto in projetos" :key="projeto.id" class="panel panel-default">
        <div class="panel-body">
          <!-- Informações do Projeto em linha -->
          <div class="row">
            <!-- Nome -->
            <div class="col-md-3">
              <strong>Nome:</strong> {{ projeto.nome }}
            </div>
            <!-- Descrição -->
            <div class="col-md-3">
              <strong>Descrição:</strong> {{ projeto.descricao }}
            </div>
            <!-- Cliente -->
            <div class="col-md-3">
              <strong>Cliente:</strong> {{ projeto.cliente }}
            </div>
            <!-- Status -->
            <div class="col-md-3">
              <strong>Status:</strong> {{ projeto.status }}
            </div>
          </div>
  
          <!-- Botão para mostrar/ocultar atividades -->
          <button @click="toggleAtividades(projeto)" class="btn btn-info">
            <span v-if="projeto.showAtividades">Ocultar Atividades</span>
            <span v-else>Ver Atividades</span>
          </button>
  
          <!-- Lista de atividades do projeto -->
          <div v-if="projeto.showAtividades" class="mt-3">
            <h4>Atividades:</h4>
            <ul class="list-group">
              <li v-for="atividade in projeto.atividades" :key="atividade.id" class="list-group-item">
                {{ atividade.descricao }} - {{ formatDate(atividade.data) }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import moment from 'moment';
  export default {
    data() {
      return {
        projetos: []
      };
    },
    mounted() {
      this.fetchProjetos();
    },
    methods: {
      // Função para buscar os projetos da API
      async fetchProjetos() {
        try {
          const response = await fetch('http://localhost:5000/projetos/abertos');
          const data = await response.json();
          this.projetos = data.map(projeto => ({
            ...projeto,
            showAtividades: false  // Inicialmente, as atividades estão ocultas
          }));
        } catch (error) {
          console.error('Erro ao carregar projetos:', error);
        }
      },
      
      // Função para alternar a visibilidade das atividades
      toggleAtividades(projeto) {
        projeto.showAtividades = !projeto.showAtividades;
      },
      formatDate(timestamp) {
      return moment(timestamp).format('DD/MM/YYYY HH:mm');
    },
    }
  };
  </script>
  
  <style scoped>
  .container {
    margin-top: 50px;
  }
  
  .panel {
    margin-bottom: 20px;
  }
  
  .panel-title {
    font-size: 1.5em;
  }
  
  .btn {
    margin-top: 10px;
  }
  
  .list-group-item {
    font-size: 1em;
    padding: 10px 15px;
    margin-bottom: 5px;
  }
  
  /* Estilo para a listagem dos projetos */
  .panel-body {
    padding: 20px;
  }
  
  /* Ajuste para a grid de 4 colunas */
  .row {
    margin-top: 10px;
  }
  
  .col-md-3 {
    margin-bottom: 10px;
  }
  </style>
  