<template>
    <div class="container mt-4">
      <b-button @click="showAddModal" variant="primary">Adicionar Projeto</b-button>
      
      <b-table :items="projetos" :fields="fields" hover responsive striped>
        <template #cell(actions)="data">
          <b-button size="sm" @click="editProjeto(data.item)" variant="warning">Editar</b-button>
          <b-button size="sm" @click="deleteProjeto(data.item.id)" variant="danger">Excluir</b-button>
        </template>
      </b-table>
  
      <!-- Modal para Adicionar ou Editar Projeto -->
      <b-modal v-model="modalVisible" :hide-footer="true" :title="isEditing ? 'Editar Projeto' : 'Adicionar Projeto'">
        <b-form @submit.prevent="isEditing ? updateProjeto() : createProjeto()">
          <b-form-group label="Nome" label-for="nome">
            <b-form-input
              id="nome"
              v-model="projeto.nome"
              required
              placeholder="Nome do projeto"
            ></b-form-input>
          </b-form-group>
          <b-form-group label="Descrição" label-for="descricao">
            <b-form-input
              id="descricao"
              v-model="projeto.descricao"
              required
              placeholder="Descrição do projeto"
            ></b-form-input>
          </b-form-group>
          <b-form-group label="Cliente" label-for="cliente">
            <b-form-select
              id="cliente"
              v-model="projeto.cliente_id"
              :options="clientesOptions"
              required
            ></b-form-select>
          </b-form-group>
          <b-form-group label="Status" label-for="status">
            <b-form-select
              id="status"
              v-model="projeto.status_projeto_id"
              :options="statusOptions"
              required
            ></b-form-select>
          </b-form-group>
          <b-button type="submit" variant="success" class="mr-2">{{ isEditing ? 'Salvar' : 'Adicionar' }}</b-button>
          <b-button variant="secondary" @click="closeModal">Cancelar</b-button>
        </b-form>
      </b-modal>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        projetos: [], // Lista de projetos
        fields: [
          { key: "nome", label: "Nome" },
          { key: "descricao", label: "Descrição" },
          { key: "cliente_nome", label: "Cliente" },
          { key: "status_projeto_nome", label: "Status" },
          { key: "actions", label: "Ações" },
        ],
        modalVisible: false, // Controla a exibição do modal
        projeto: { nome: "", descricao: "", cliente_id: null, status_projeto_id: null }, // Dados do projeto
        clientesOptions: [], // Opções para o select de clientes
        statusOptions: [], // Opções para o select de status
        isEditing: false, // Define se é edição ou criação
        editId: null, // ID do projeto para editar
      };
    },
    mounted() {
      this.fetchProjetos();
      this.fetchClientes();
      this.fetchStatus();
    },
    methods: {
      // Buscar projetos
      fetchProjetos() {
        axios
          .get("http://localhost:5000/projetos")
          .then((response) => {
            this.projetos = response.data;
          })
          .catch((error) => console.error("Erro ao consultar projetos:", error));
      },
      // Buscar clientes
      fetchClientes() {
        axios
          .get("http://localhost:5000/clientes")
          .then((response) => {
            this.clientesOptions = response.data.map((cliente) => ({
              value: cliente.id,
              text: cliente.nome,
            }));
          })
          .catch((error) => console.error("Erro ao carregar clientes:", error));
      },
      // Buscar status do projeto
      fetchStatus() {
        axios
          .get("http://localhost:5000/status_projetos")
          .then((response) => {
            this.statusOptions = response.data.map((status) => ({
              value: status.id,
              text: status.nome,
            }));
          })
          .catch((error) => console.error("Erro ao carregar status do projeto:", error));
      },
      // Exibir modal de adição
      showAddModal() {
        this.resetForm();
        this.modalVisible = true;
        this.isEditing = false;
      },
      // Exibir modal para editar
      editProjeto(projeto) {
        this.projeto = {
          nome: projeto.nome,
          descricao: projeto.descricao,
          cliente_id: projeto.cliente_id,
          status_projeto_id: projeto.status_projeto_id,
        };
        this.editId = projeto.id;
        this.modalVisible = true;
        this.isEditing = true;
      },
      // Fechar modal
      closeModal() {
        this.modalVisible = false;
      },
      // Criar projeto
      createProjeto() {
        axios
          .post("http://localhost:5000/projetos", this.projeto)
          .then(() => {
            this.fetchProjetos();
            this.closeModal();
          })
          .catch((error) => console.error("Erro ao criar projeto:", error));
      },
      // Atualizar projeto
      updateProjeto() {
        axios
          .put(`http://localhost:5000/projetos/${this.editId}`, this.projeto)
          .then(() => {
            this.fetchProjetos();
            this.closeModal();
          })
          .catch((error) => console.error("Erro ao atualizar projeto:", error));
      },
      // Excluir projeto
      deleteProjeto(projetoId) {
        axios
          .delete(`http://localhost:5000/projetos/${projetoId}`)
          .then(() => {
            this.fetchProjetos();
          })
          .catch((error) => console.error("Erro ao excluir projeto:", error));
      },
      // Resetar formulário
      resetForm() {
        this.projeto = { nome: "", descricao: "", cliente_id: null, status_projeto_id: null };
        this.editId = null;
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 800px;
  }
  </style>
  