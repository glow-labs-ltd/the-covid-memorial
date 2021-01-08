export const state = () => ({
  sideMenuOpen: false,
  addModal: false,
  deceased: [],
})

export const mutations = {
  toggleSideMenu(state) {
    state.sideMenuOpen = !state.sideMenuOpen
  },
  setAddModal(state, value) {
    state.addModal = value
  },
  appendDeceased(state, value) {
    // state.deceased.push(value)
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
}
