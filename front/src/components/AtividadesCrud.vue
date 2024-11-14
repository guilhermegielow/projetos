<template>
    <div>
      <h1>Cadastrar Atividade</h1>
      <form @submit.prevent="cadastrarAtividade">
        <div>
          <label for="cliente">Cliente:</label>
          <select v-model="atividade.clienteId" id="cliente">
            <option v-for="cliente in clientes" :key="cliente.id" :value="cliente.id">
              {{ cliente.nome }}
            </option>
          </select>
        </div>
        
        <div>
          <label for="projeto">Projeto:</label>
          <select v-model="atividade.projetoId" id="projeto">
            <option v-for="projeto in projetos" :key="projeto.id" :value="projeto.id">
              {{ projeto.nome }}
            </option>
          </select>
        </div>
        
        <div>
          <label for="descricao">Descrição:</label>
          <input type="text" v-model="atividade.descricao" id="descricao" />
        </div>
  
        <button type="submit">Cadastrar</button>
      </form>
    </div>
  </template>
  
  <script>
  import api from '../services/api';
  
  export default {
    data() {
      return {
        atividade: {
          clienteId: null,
          projetoId: null,
          descricao: ''
        },
        clientes: [],
        projetos: []
      };
    },
    async created() {
      // Carregar clientes e projetos
      try {
        const responseClientes = await api.get('/clientes');
        this.clientes = responseClientes.data;
  
        const responseProjetos = await api.get('/projetos');
        this.projetos = responseProjetos.data;
      } catch (error) {
        console.error('Erro ao carregar dados:', error);
      }
    },
    methods: {
      async cadastrarAtividade() {
        try {
          await api.post('/atividades', this.atividade);
          alert('Atividade cadastrada com sucesso!');
        } catch (error) {
          console.error('Erro ao cadastrar atividade:', error);
        }
      }
    }
  };
  </script>