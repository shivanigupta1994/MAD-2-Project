import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state: {
    searchQuery: '',
    searchResults: [],
  },
  mutations: {
    setSearchQuery(state, query) {
      console.log('setSearchQuery mutation called with query:', query);
      state.searchQuery = query;
    },
    setSearchResults(state, results) {
      console.log('setSearchResults mutation called with results:', results);
      state.searchResults = results;
    },
  },
  actions: {
    async searchBooks({ commit }, query) {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/book/search?query=${query}`, {
          headers: {
            'Accept': 'application/json',
          },
        });
        commit('setSearchResults', response.data);
      } catch (error) {
        console.error("Error searching books:", error);
      }
    },
  },
})
