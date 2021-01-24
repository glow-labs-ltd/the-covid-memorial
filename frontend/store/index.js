export const state = () => ({
  sideMenuOpen: false,
  addModal: false,
  deceased: [],
  error: null,
  deceasedLoading: false,
  searchQuery: null,
  searchResults: null,
  searchCount: null,
  searchNext: null,
  searchLast: {},
  searchPage: 1,
  overview: true,
  overviewTransition: false,
  firstTime: true,
})

export const mutations = {
  toggleSideMenu(state) {
    state.sideMenuOpen = !state.sideMenuOpen
  },
  closeSideMenu(state) {
    state.sideMenuOpen = false
  },
  setAddModal(state, value) {
    state.addModal = value
  },
  setSearchQuery(state, value) {
    state.searchQuery = value
  },
  setSearchResults(state, { results, count, next }) {
    state.searchResults = results
    state.searchCount = count
    state.searchNext = next
  },
  setSearchLast(state, value) {
    state.searchLast = value
  },
  clearSearchResults(state) {
    state.searchResults = []
    state.searchCount = 0
    state.searchNext = null
    state.searchPage = 1
  },
  incrementSearchPage(state) {
    state.searchPage += 1
  },
  setError(state, value) {
    state.error = value
  },
  setOverview(state, value) {
    state.overview = value
  },
  setOverviewTransition(state, value) {
    state.overviewTransition = value
  },
  setFirstTime(state, value) {
    state.firstTime = value
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
    try {
      commit('setDeceasedLoading', true)
      const deceased = await this.$axios.$get('deceased/')
      commit('appendDeceased', deceased)
    } catch (e) {
      // for not, not much to do
      if (e.response.status === 429) return
    } finally {
      commit('setDeceasedLoading', false)
    }
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
      return response
    } catch (e) {
      commit('setError', e.response.data)
    }
  },

  async search({ state, commit }, append) {
    try {
      if (append && state.searchNext) commit('incrementSearchPage')

      const sameQuery = state.searchLast?.query === state.searchQuery
      const samePage = state.searchLast?.page === state.searchPage
      if (sameQuery && samePage) return
      if (!sameQuery) commit('clearSearchResults')

      commit('setError', null)
      const response = await this.$axios.$get(
        `search/?q=${state.searchQuery}&limit=10&offset=${
          (state.searchPage - 1) * 10
        }`
      )

      if (response) {
        commit('setSearchLast', {
          query: state.searchQuery,
          page: state.searchPage,
        })
        const results = append
          ? [...state.searchResults, ...response.results]
          : response.results

        commit('setSearchResults', {
          results,
          count: response.count,
          next: response.next,
        })
      }
    } catch (e) {
      commit('setError', e.response.data)
    }
  },
}
