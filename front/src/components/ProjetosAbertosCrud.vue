<template>
  <div>
    <Header /> <!-- Cabeçalho global da página -->
    <div class="container mt-6">
      <div class="text-left mb-6">
        <h1>Projetos em Aberto</h1>
      </div>

      <!-- Lista de Projetos -->
      <div v-for="projeto in projetos" :key="projeto.id" class="panel panel-default mb-4">
        <div class="panel-body">
          <div class="row">
            <!-- Nome do Projeto -->
            <div class="col-md-3">
              <strong>Nome:</strong> {{ projeto.nome }}
            </div>
            <!-- Descrição do Projeto -->
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
          <button @click="toggleAtividades(projeto)" class="btn btn-info mt-3">
            <span v-if="projeto.showAtividades">Ocultar Atividades</span>
            <span v-else>Ver Atividades</span>
          </button>

          <!-- Lista de atividades do projeto -->
          <div v-if="projeto.showAtividades" class="mt-3">
            <h4>Atividades:</h4>
            <ul class="list-group">
              <li v-for="atividade in projeto.atividades" :key="atividade.id" class="list-group-item">
                {{ atividade.descricao }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
 import Header from "./HeaderPage.vue";
  
  export default {
    components: {
    Header,
  },
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
  }
};
</script>

<style scoped>
.container {
  margin-top: 60px;
  max-width: 900px;
  padding: 10px;
}

.page-title {
  font-size: 1.8em;
  font-weight: 600;
  color: #343a40;
  margin-bottom: 20px;
}

.project-panel {
  border: 1px solid #e3e3e3;
  border-radius: 8px;
  padding: 15px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.panel-body {
  padding: 10px;
}

.row {
  margin-bottom: 10px;
}

.col-sm-3 {
  font-size: 0.95em;
}

.btn {
  font-size: 0.9em;
  padding: 6px 12px;
}

.activity-title {
  font-size: 1.2em;
  font-weight: bold;
  margin-bottom: 8px;
}

.list-group-item {
  font-size: 0.9em;
  padding: 8px;
  border-radius: 5px;
  background-color: #ffffff;
}

h1 {
  margin-bottom: 15px;
  font-size: 1.5rem;
}
</style>
