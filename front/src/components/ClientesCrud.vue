<template>
    <div class="container mt-4">
      <b-button @click="showAddModal" variant="primary">Adicionar Cliente</b-button>
      
      <b-table :items="clientes" :fields="fields" hover responsive striped>
        <template #cell(actions)="data">
          <b-button size="sm" @click="editCliente(data.item)" variant="warning">Editar</b-button>
          <b-button size="sm" @click="deleteCliente(data.item.id)" variant="danger">Excluir</b-button>
        </template>
      </b-table>
  
      <!-- Modal para Adicionar ou Editar Cliente -->
      <b-modal v-model="modalVisible" :hide-footer="true" :title="isEditing ? 'Editar Cliente' : 'Adicionar Cliente'">
        <b-form @submit.prevent="isEditing ? updateCliente() : createCliente()">
          <b-form-group label="Nome" label-for="nome">
            <b-form-input
              id="nome"
              v-model="cliente.nome"
              required
              placeholder="Nome do cliente"
            ></b-form-input>
          </b-form-group>
          <b-form-group label="Email" label-for="email">
            <b-form-input
              id="email"
              v-model="cliente.email"
              required
              placeholder="Email do cliente"
            ></b-form-input>
          </b-form-group>
          <b-form-group label="Telefone" label-for="telefone">
            <b-form-input
              id="telefone"
              v-model="cliente.telefone"
              required
              placeholder="Telefone do cliente"
            ></b-form-input>
          </b-form-group>
          <b-form-group label="CNPJ" label-for="cnpj">
            <b-form-input
              id="cnpj"
              v-model="cliente.cnpj"
              required
              placeholder="CNPJ do cliente"
            ></b-form-input>
          </b-form-group>
          <b-button type="submit" variant="success" class="mr-2">{{ isEditing ? 'Salvar' : 'Adicionar' }}</b-button>
          <b-button variant="secondary" @click="closeModal">Cancelar</b-button>
        </b-form>
      </b-modal>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        clientes: [], // Lista de clientes
        fields: [
          { key: 'nome', label: 'Nome' },
          { key: 'email', label: 'Email' },
          { key: 'telefone', label: 'Telefone' },
          { key: 'cnpj', label: 'CNPJ' },
          { key: 'actions', label: 'Ações' },
        ],
        modalVisible: false, // Controla a exibição do modal
        cliente: { nome: '', email: '', telefone: '' }, // Dados do cliente
        isEditing: false, // Define se é edição ou criação
        editId: null, // ID do cliente para editar
      };
    },
    mounted() {
      this.fetchClientes();
    },
    methods: {
      // Função para buscar todos os clientes
      fetchClientes() {
        // Fazendo uma requisição GET para o endpoint da API que retorna a lista de clientes
        axios.get('http://localhost:5000/clientes')
            .then(response => {
            // Armazenando os clientes recebidos na variável 'clientes'
            this.clientes = response.data;
        })
          .catch(error => console.error('Erro ao consultar cliente:', error));
      },
      // Exibir o modal de adição de um cliente
      showAddModal() {
        this.resetForm();
        this.modalVisible = true;
        this.isEditing = false;
      },
      // Exibir o modal para editar um cliente
      editCliente(cliente) {
        this.cliente = { ...cliente };
        this.editId = cliente.id;
        this.modalVisible = true;
        this.isEditing = true;
      },
      // Fechar o modal
      closeModal() {
        this.modalVisible = false;
      },
      // Criar um novo cliente
      createCliente() {
        axios.post('http://localhost:5000/clientes', this.cliente) // Envia os dados para o backend
          .then(() => {
            this.fetchClientes(); // Atualiza a lista de clientes
            this.closeModal(); // Fecha o modal
          })
          .catch(error => console.error('Erro ao criar cliente:', error));
      },
      // Atualizar um cliente existente
      updateCliente() {
        axios.put(`http://localhost:5000/clientes/${this.editId}`, this.cliente) // Atualiza os dados no backend
          .then(() => {
            this.fetchClientes(); // Atualiza a lista de clientes
            this.closeModal(); // Fecha o modal
          })
          .catch(error => console.error('Erro ao atualizar cliente:', error));
      },
      // Excluir um cliente
      deleteCliente(clienteId) {
        axios.delete(`http://localhost:5000/clientes/${clienteId}`) // Exclui o cliente do backend
          .then(() => {
            this.fetchClientes(); // Atualiza a lista de clientes
          })
          .catch(error => console.error('Erro ao excluir cliente:', error));
      },
      // Resetar os campos do formulário
      resetForm() {
        this.cliente = { nome: '', email: '', telefone: '', cnpj: ''};
        this.editId = null;
      }
    }
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 800px;
  }
  </style>
  