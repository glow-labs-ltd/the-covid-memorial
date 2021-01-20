export const state = () => ({
  today: null,
  yesterday: null,
  count: null,
})

export const mutations = {
  setFigures(state, { today, yesterday }) {
    state.count = today
    state.today = today
    state.yesterday = yesterday
  },
  increment(state) {
    if (state.count) state.count += 1
  },
}

export const getters = {
  deathRate: (state) => {
    if (state.today && state.yesterday) {
      return (state.today - state.yesterday) / 86400000
    }
    return null
  },
}

export const actions = {
  async getDeathCount({ commit }) {
    const todayAPI = this.$axios.$get('https://disease.sh/v3/covid-19/all')
    const yesterdayAPI = this.$axios.$get(
      'https://disease.sh/v3/covid-19/all?yesterday=true'
    )
    const today = await todayAPI
    const yesterday = await yesterdayAPI

    commit('setFigures', {
      today: today.deaths,
      yesterday: yesterday.deaths,
    })
  },
}
