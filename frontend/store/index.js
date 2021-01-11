export const state = () => ({
  sideMenuOpen: false,
  addModal: false,
  deceased: [],
  error: null,
  deceasedLoading: false,
  showSearch: false,
  searchQuery: null,
  results: null,
})

export const mutations = {
  toggleSideMenu(state) {
    state.sideMenuOpen = !state.sideMenuOpen
  },
  setAddModal(state, value) {
    state.addModal = value
  },
  setShowSearch(state, value) {
    state.showSearch = value
  },
  setSearchQuery(state, value) {
    state.searchQuery = value
  },
  setResults(state, value) {
    state.results = value
  },
  setError(state, value) {
    state.error = value
  },
  appendDeceased(state, value) {
    state.deceased = state.deceased.concat(value)
  },
  shiftDeceased(state) {
    state.deceased.shift()
  },
  emptyDeceased(state) {
    state.deceased = []
  },
  setDeceasedLoading(state, value) {
    state.deceasedLoading = value
  },
}

export const actions = {
  async getDeceased({ commit }) {
    commit('setDeceasedLoading', true)
    const deceased = await this.$axios.$get('deceased/')
    commit('appendDeceased', deceased)
    commit('setDeceasedLoading', false)
  },

  nextDeceased({ state, commit }) {
    if (state.deceased.length > 0) {
      const deceased = state.deceased[0]
      commit('shiftDeceased')
      return deceased
    }
    return null
  },

  async postDeceased({ commit }, data) {
    try {
      commit('setError', null)
      const response = await this.$axios.$post('deceased/', data)
      if (response) commit('setAddModal', false)
    } catch (e) {
      commit('setError', e.response.data)
    }
  },

  async search({ state, commit }) {
    try {
      commit('setError', null)
      const response = await this.$axios.$get(`search/?q=${state.searchQuery}`)
      if (response) commit('setResults', response)
    } catch (e) {
      commit('setError', e.response.data)
    }
  },
}
