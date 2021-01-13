export const state = () => ({
  comments: [],
  page: 0,
  error: null,
})

export const mutations = {
  setComments(state, { comments, page }) {
    state.comments = comments
    state.page = page
  },
  setError(state, value) {
    state.error = value
  },
}

export const actions = {
  async postComment({ commit }, data) {
    try {
      commit('setError', null)
      return await this.$axios.$post('comment/', data)
    } catch (e) {
      commit('setError', e.response.data)
    }
  },

  async getComments({ state, commit }, id) {
    const response = await this.$axios.$get(
      `comment/${id}/?limit=10&offset=${state.newPage * 10}`
    )
    if (response) {
      commit('setComments', {
        comments: response.results,
        page: state.newPage + 1,
      })
    }
  },
}
