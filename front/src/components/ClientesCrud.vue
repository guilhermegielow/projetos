<template>
  <div>
    <Header />
    <div class="content">
      <div class="container mt-6">
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
                :state="emailState"
              ></b-form-input>
              <b-form-invalid-feedback v-if="!validEmail && cliente.email">
                O e-mail informado não é válido.
              </b-form-invalid-feedback>
            </b-form-group>
            <b-form-group label="Telefone" label-for="telefone">
              <b-form-input
                id="telefone"
                v-model="cliente.telefone"
                required
                maxlength="11"
                placeholder="Telefone do cliente"
                @input="filtrarNumeros"
              ></b-form-input>
            </b-form-group>
            <b-form-group label="CNPJ" label-for="cnpj">
              <b-form-input
                id="cnpj"
                v-model="cliente.cnpj"
                required
                maxlength="14"
                placeholder="CNPJ do cliente"
                @input="filtrarNumeros"
              ></b-form-input>
            </b-form-group>
            <b-button type="submit" variant="success" class="mr-2" :disabled="!validEmail">{{ isEditing ? 'Salvar' : 'Adicionar' }}</b-button>
            <b-button variant="secondary" @click="closeModal">Cancelar</b-button>
          </b-form>
        </b-modal>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Header from "./HeaderPage.vue";

export default {
  components: {
    Header,
  },
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
      cliente: { nome: '', email: '', telefone: '', cnpj: '' }, // Dados do cliente
      isEditing: false, // Define se é edição ou criação
      editId: null, // ID do cliente para editar
    };
  },
  mounted() {
    this.fetchClientes();
  },
  computed: {
    validEmail() {
      const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      return regex.test(this.cliente.email); 
    },
    emailState() {
      return this.validEmail ? true : false; 
    }
  },
  methods: {
    fetchClientes() {
      axios.get('http://localhost:5000/clientes')
          .then(response => {
            this.clientes = response.data;
        })
        .catch(error => console.error('Erro ao consultar cliente:', error));
    },
    showAddModal() {
      this.resetForm();
      this.modalVisible = true;
      this.isEditing = false;
    },
    editCliente(cliente) {
      this.cliente = { ...cliente };
      this.editId = cliente.id;
      this.modalVisible = true;
      this.isEditing = true;
    },
    closeModal() {
      this.modalVisible = false;
    },
    createCliente() {
      axios.post('http://localhost:5000/clientes', this.cliente)
        .then(() => {
          this.fetchClientes();
          this.closeModal();
        })
        .catch(error => console.error('Erro ao criar cliente:', error));
    },
    updateCliente() {
      axios.put(`http://localhost:5000/clientes/${this.editId}`, this.cliente)
        .then(() => {
          this.fetchClientes();
          this.closeModal();
        })
        .catch(error => console.error('Erro ao atualizar cliente:', error));
    },
    deleteCliente(clienteId) {
      axios.delete(`http://localhost:5000/clientes/${clienteId}`)
        .then(() => {
          this.fetchClientes();
        })
        .catch(error => console.error('Erro ao excluir cliente:', error));
    },
    resetForm() {
      this.cliente = { nome: '', email: '', telefone: '', cnpj: '' };
      this.editId = null;
    }
  }
};
</script>

<style scoped>
.container {
  margin-top: 60px;
  max-width: 800px;
}
</style>
