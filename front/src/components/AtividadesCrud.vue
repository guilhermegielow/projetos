<template>
  <div>
    <Header />
    <div class="content">
    <div class="container mt-6">
    <button class="btn btn-primary" @click="showAddModal">Adicionar Atividade</button>

    <table class="table table-striped table-hover mt-3">
      <thead>
        <tr>
          <th>Descrição</th>
          <th>Cliente</th>
          <th>Projeto</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="atividade in atividades" :key="atividade.id">
          <td>{{ atividade.descricao }}</td>
          <td>{{ atividade.cliente_nome }}</td>
          <td>{{ atividade.projeto_nome }}</td>
          <td>
            <button class="btn btn-warning btn-sm" @click="editAtividade(atividade)">Editar</button>
            <button class="btn btn-danger btn-sm" @click="deleteAtividade(atividade.id)">Excluir</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Modal para Adicionar ou Editar Atividade -->
    <div v-if="modalVisible" class="modal fade show" tabindex="-1" role="dialog" style="display: block;">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">{{ isEditing ? 'Editar Atividade' : 'Adicionar Atividade' }}</h4>
          </div>
          <form @submit.prevent="isEditing ? updateAtividade() : createAtividade()">
            <div class="modal-body">
              <div class="form-group">
                <label for="descricao">Descrição</label>
                <input
                  type="text"
                  id="descricao"
                  class="form-control"
                  v-model="atividade.descricao"
                  required
                  placeholder="Descrição da atividade"
                />
              </div>
              <div class="form-group">
                <label for="cliente">Cliente</label>
                <select
                  id="cliente"
                  class="form-control"
                  v-model="atividade.cliente_id"
                  @change="filterProjetos"
                  required
                >
                  <option value="" disabled>Selecione o Cliente</option>
                  <option v-for="cliente in clientes" :key="cliente.id" :value="cliente.id">
                    {{ cliente.nome }}
                  </option>
                </select>
              </div>
              <div class="form-group">
                <label for="projeto">Projeto</label>
                <select
                  id="projeto"
                  class="form-control"
                  v-model="atividade.projeto_id"
                  required
                >
                  <option value="" disabled>Selecione o Projeto</option>
                  <option v-for="projeto in projetosFiltrados" :key="projeto.id" :value="projeto.id">
                    {{ projeto.nome }}
                  </option>
                </select>
              </div>
            </div>
            <div class="modal-footer">
              <button type="submit" class="btn btn-success">{{ isEditing ? 'Salvar' : 'Adicionar' }}</button>
              <button type="button" class="btn btn-default" @click="closeModal">Cancelar</button>
            </div>
          </form>
        </div>
      </div>
    </div>
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
      atividades: [], // Lista de atividades
      clientes: [], // Lista de clientes
      projetos: [], // Lista de todos os projetos
      projetosFiltrados: [], // Projetos filtrados pelo cliente selecionado
      atividade: { descricao: "", cliente_id: null, projeto_id: null }, // Dados da atividade
      modalVisible: false, // Controla a visibilidade do modal
      isEditing: false, // Define se é edição ou criação
      editId: null, // ID da atividade para editar
    };
  },
  mounted() {
    this.fetchAtividades();
    this.fetchClientes();
    this.fetchProjetos();
  },
  methods: {
    // Buscar atividades
    fetchAtividades() {
      axios
        .get("http://localhost:5000/atividades")
        .then((response) => {
          this.atividades = response.data;
        })
        .catch((error) => console.error("Erro ao buscar atividades:", error));
    },
    // Buscar clientes
    fetchClientes() {
      axios
        .get("http://localhost:5000/clientes")
        .then((response) => {
          this.clientes = response.data;
        })
        .catch((error) => console.error("Erro ao buscar clientes:", error));
    },
    // Buscar projetos
    fetchProjetos() {
      axios
        .get("http://localhost:5000/projetos")
        .then((response) => {
          this.projetos = response.data;
        })
        .catch((error) => console.error("Erro ao buscar projetos:", error));
    },
    // Filtrar projetos com base no cliente selecionado
    filterProjetos() {
      this.projetosFiltrados = this.projetos.filter(
        (projeto) => projeto.cliente_id === this.atividade.cliente_id
      );
    },
    // Exibir modal de adição
    showAddModal() {
      this.resetForm();
      this.modalVisible = true;
      this.isEditing = false;
    },
    // Fechar modal
    closeModal() {
      this.modalVisible = false;
    },
    // Exibir modal para editar
    editAtividade(atividade) {
      this.atividade = {
        descricao: atividade.descricao,
        cliente_id: atividade.cliente_id,
        projeto_id: atividade.projeto_id,
      };
      this.filterProjetos(); // Filtrar projetos com base no cliente da atividade
      this.editId = atividade.id;
      this.isEditing = true;
      this.modalVisible = true;
    },
    // Criar atividade
    createAtividade() {
      axios
        .post("http://localhost:5000/atividades", this.atividade)
        .then(() => {
          this.fetchAtividades();
          this.closeModal();
        })
        .catch((error) => console.error("Erro ao criar atividade:", error));
    },
    // Atualizar atividade
    updateAtividade() {
      axios
        .put(`http://localhost:5000/atividades/${this.editId}`, this.atividade)
        .then(() => {
          this.fetchAtividades();
          this.closeModal();
        })
        .catch((error) => console.error("Erro ao atualizar atividade:", error));
    },
    // Excluir atividade
    deleteAtividade(atividadeId) {
      axios
        .delete(`http://localhost:5000/atividades/${atividadeId}`)
        .then(() => {
          this.fetchAtividades();
        })
        .catch((error) => console.error("Erro ao excluir atividade:", error));
    },
    // Resetar formulário
    resetForm() {
      this.atividade = { descricao: "", cliente_id: null, projeto_id: null };
      this.projetosFiltrados = [];
      this.editId = null;
    },
  },
};
</script>

<style scoped>
.container {
  margin-top: 60px;
  max-width: 800px;
}
</style>
