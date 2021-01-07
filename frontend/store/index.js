export const state = () => ({
  sideMenuOpen: false,
})

export const mutations = {
  toggleSideMenu(state) {
    state.sideMenuOpen = !state.sideMenuOpen
  },
}
