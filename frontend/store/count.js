export const state = () => ({
  last2: null,
  count: null,
  country: null,
})

export const mutations = {
  setLast2(state, last2) {
    state.last2 = last2
    state.count = last2[0]?.deaths
  },
  increment(state) {
    if (state.count) state.count += 1
  },
  setCountry(state, value) {
    state.country = value
  },
}

export const getters = {
  deathRate: (state) => {
    if (state.last2) {
      const date0 = new Date(state.last2[0].date)
      const date1 = new Date(state.last2[1].date)
      const time = Math.ceil(date0 - date1)
      if (time === 0) return 0
      return (state.last2[0].deaths - state.last2[1].deaths) / time
    }
    return null
  },
}

export const actions = {
  async getDeathCount({ state, commit }) {
    let timeline

    if (!state.country) {
      const response = await this.$axios.$get('https://corona-api.com/timeline')
      timeline = response.data
    } else {
      const response = await this.$axios.$get(
        `https://corona-api.com/countries/${state.country}`
      )
      timeline = response.data.timeline
    }

    commit('setLast2', timeline.slice(0, 2))
  },
}
