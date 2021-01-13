export const state = () => ({
  comments: [],
  next: null,
  page: 0,
  error: null,
})

export const mutations = {
  setComments(state, { comments, next, page }) {
    state.comments = comments
    state.next = next
    state.page = page
  },
  appendComment(state, comment) {
    state.comments = state.comments.concat(comment)
  },
  clearComments(state) {
    state.comments = []
    state.next = null
    state.page = 0
  },
  setError(state, value) {
    state.error = value
  },
}

export const actions = {
  async postComment({ state, commit }, data) {
    try {
      commit('setError', null)
      const response = await this.$axios.$post('comment/', data)

      // add the new comment to the array
      if (!state.next) commit('appendComment', response)
      return response
    } catch (e) {
      commit('setError', e.response.data)
    }
  },

  async getComments({ state, commit }, { id, append }) {
    if (!append) commit('clearComments')

    const response = await this.$axios.$get(
      `comment/${id}/?limit=10&offset=${state.page * 10}`
    )
    if (response) {
      commit('setComments', {
        comments: [...state.comments, ...response.results],
        next: response.next,
        page: state.page + 1,
      })
    }
  },
}
