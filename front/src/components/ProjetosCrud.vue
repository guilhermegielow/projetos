<template>
    <div>
        <h2>Projetos</h2>
        <ul>
            <li v-for="projeto in projetos" :key="projeto.id">
                {{ projeto.nome }} - {{ projeto.descricao }}
                <button @click="addAtividade(projeto.id)">Adicionar Atividade</button>
            </li>
        </ul>
    </div>
</template>

<script>
import api from '@/services/api';

export default {
    data() {
        return {
            projetos: []
        };
    },
    methods: {
        async fetchProjetos() {
            const response = await api.get('/projetos');
            this.projetos = response.data;
        },
        async addAtividade(projetoId) {
            const descricao = prompt('Descrição da atividade:');
            await api.post('/atividades', { descricao, projeto_id: projetoId });
        }
    },
    created() {
        this.fetchProjetos();
    }
};
</script>