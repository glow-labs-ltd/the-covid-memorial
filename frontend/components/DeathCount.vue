<template>
  <div>
    <h2 class="lost-count">
      {{ format($store.state.count.count) }} <span>Sadly&nbsp;lost</span>
    </h2>
  </div>
</template>

<script>
export default {
  async fetch() {
    await this.$store.dispatch('count/getDeathCount')
  },
  mounted() {
    this.start()
  },
  methods: {
    format(number) {
      return number ? Math.floor(number).toLocaleString() : ''
    },
    start() {
      const deathRate = this.$store.getters['count/deathRate']
      if (deathRate > 0) {
        setInterval(() => this.$store.commit('count/increment'), 1 / deathRate)
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.lost-count {
  text-align: center;
  font-size: 2.75rem;
  font-weight: 400;

  @media (min-width: $phone) {
    font-size: 3rem;
  }

  @media (min-width: $tablet) {
    font-size: 3.75rem;
  }

  span {
    font-size: 2.5rem;
  }
}
</style>
