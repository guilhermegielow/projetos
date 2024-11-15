<template>
  <div>
    <Header />
    <div class="content">
      <div class="container mt-6">
        <b-button @click="showAddModal" variant="primary">Adicionar Atividade</b-button>
        
        <b-table :items="atividades" :fields="fields" hover responsive striped>
          <template #cell(actions)="data">
            <b-button size="sm" @click="editAtividade(data.item)" variant="warning">Editar</b-button>
            <b-button size="sm" @click="deleteAtividade(data.item.id)" variant="danger">Excluir</b-button>
          </template>
        </b-table>

        <!-- Modal para Adicionar ou Editar Atividade -->
        <b-modal v-model="modalVisible" :hide-footer="true" :title="isEditing ? 'Editar Atividade' : 'Adicionar Atividade'">
          <b-form @submit.prevent="isEditing ? updateAtividade() : createAtividade()">
            <b-form-group label="Descrição" label-for="descricao">
              <b-form-input
                id="descricao"
                v-model="atividade.descricao"
                required
                placeholder="Descrição da atividade"
              ></b-form-input>
            </b-form-group>

            <b-form-group label="Cliente" label-for="cliente">
              <b-form-select
                id="cliente"
                v-model="atividade.cliente_id"
                @change="filterProjetos"
                :options="clientesOptions"
                required
              ></b-form-select>
            </b-form-group>

            <b-form-group label="Projeto" label-for="projeto">
              <b-form-select
                id="projeto"
                v-model="atividade.projeto_id"
                :options="projetosFiltrados"
                required
              ></b-form-select>
            </b-form-group>

            <b-button type="submit" variant="success" class="mr-2">{{ isEditing ? 'Salvar' : 'Adicionar' }}</b-button>
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
      atividades: [],
      clientes: [],
      projetos: [],
      atividade: { descricao: "", cliente_id: null, projeto_id: null },
      modalVisible: false,
      isEditing: false,
      editId: null,
      fields: [
        { key: 'descricao', label: 'Descrição' },
        { key: 'cliente_nome', label: 'Cliente' },
        { key: 'projeto_nome', label: 'Projeto' },
        { key: 'actions', label: 'Ações' },
      ],
    };
  },
  mounted() {
    this.fetchAtividades();
    this.fetchClientes();
    this.fetchProjetos();
  },
  computed: {
    clientesOptions() {
      return this.clientes.map(cliente => ({ value: cliente.id, text: cliente.nome }));
    },
    projetosFiltrados() {
      return this.projetos
        .filter(projeto => projeto.cliente_id === this.atividade.cliente_id)
        .map(projeto => ({ value: projeto.id, text: projeto.nome }));
    },
  },
  methods: {
    fetchAtividades() {
      axios
        .get("http://localhost:5000/atividades")
        .then((response) => {
          this.atividades = response.data;
        })
        .catch((error) => console.error("Erro ao buscar atividades:", error));
    },
    fetchClientes() {
      axios
        .get("http://localhost:5000/clientes")
        .then((response) => {
          this.clientes = response.data;
        })
        .catch((error) => console.error("Erro ao buscar clientes:", error));
    },
    fetchProjetos() {
      axios
        .get("http://localhost:5000/projetos")
        .then((response) => {
          this.projetos = response.data;
        })
        .catch((error) => console.error("Erro ao buscar projetos:", error));
    },
    showAddModal() {
      this.resetForm();
      this.modalVisible = true;
      this.isEditing = false;
    },
    closeModal() {
      this.modalVisible = false;
    },
    editAtividade(atividade) {
      this.atividade = { ...atividade };
      this.filterProjetos();
      this.editId = atividade.id;
      this.isEditing = true;
      this.modalVisible = true;
    },
    createAtividade() {
      axios
        .post("http://localhost:5000/atividades", this.atividade)
        .then(() => {
          this.fetchAtividades();
          this.closeModal();
        })
        .catch((error) => console.error("Erro ao criar atividade:", error));
    },
    updateAtividade() {
      axios
        .put(`http://localhost:5000/atividades/${this.editId}`, this.atividade)
        .then(() => {
          this.fetchAtividades();
          this.closeModal();
        })
        .catch((error) => console.error("Erro ao atualizar atividade:", error));
    },
    deleteAtividade(atividadeId) {
      axios
        .delete(`http://localhost:5000/atividades/${atividadeId}`)
        .then(() => {
          this.fetchAtividades();
        })
        .catch((error) => console.error("Erro ao excluir atividade:", error));
    },
    resetForm() {
      this.atividade = { descricao: "", cliente_id: null, projeto_id: null };
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
