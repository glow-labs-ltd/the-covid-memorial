export const state = () => ({
  sideMenuOpen: false,
  addModal: false,
  deceased: [],
  error: null,
})

export const mutations = {
  toggleSideMenu(state) {
    state.sideMenuOpen = !state.sideMenuOpen
  },
  setAddModal(state, value) {
    state.addModal = value
  },
  setError(state, value) {
    state.error = value
  },
  appendDeceased(state, value) {
    state.deceased = [...state.deceased, value]
  },
  emptyDeceased(state) {
    state.deceased = []
  },
}

export const actions = {
  async getDeceased({ commit }) {
    const deceased = await this.$axios.$get('deceased/')
    commit('appendDeceased', deceased)
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
}
