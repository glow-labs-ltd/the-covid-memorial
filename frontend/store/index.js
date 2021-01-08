export const state = () => ({
  sideMenuOpen: false,
  addModal: false,
  deceased: [],
  deceasedLoading: false,
})

export const mutations = {
  toggleSideMenu(state) {
    state.sideMenuOpen = !state.sideMenuOpen
  },
  setAddModal(state, value) {
    state.addModal = value
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
}
