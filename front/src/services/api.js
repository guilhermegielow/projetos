import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:5000'
});

// Funções para cada CRUD (clientes, projetos, atividades)
export const getClientes = () => api.get('/clientes');
export const getProjetos = () => api.get('/projetos');
export const getAtividades = () => api.get('/atividades');

export const createCliente = (data) => api.post('/clientes', data);
export const createProjeto = (data) => api.post('/projetos', data);
export const createAtividade = (data) => api.post('/atividades', data);

// Funções de atualização
export const updateCliente = (id, data) => api.put(`/clientes/${id}`, data);
export const updateProjeto = (id, data) => api.put(`/projetos/${id}`, data);
export const updateAtividade = (id, data) => api.put(`/atividades/${id}`, data);

// Funções de exclusão
export const deleteCliente = (id) => api.delete(`/clientes/${id}`);
export const deleteProjeto = (id) => api.delete(`/projetos/${id}`);
export const deleteAtividade = (id) => api.delete(`/atividades/${id}`);

export default api;