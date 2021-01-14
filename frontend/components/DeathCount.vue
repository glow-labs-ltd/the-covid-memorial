<template>
  <div>
    <h2 class="lost-count">{{ format(count) }} <span>Sadly lost</span></h2>
  </div>
</template>

<script>
export default {
  async fetch() {
    const timeline = await this.$axios.$get('https://corona-api.com/timeline')
    this.last2 = timeline.data.slice(0, 2)
    this.count = this.last2[0]?.deaths
  },
  data() {
    return {
      last2: null,
      count: null,
    }
  },
  computed: {
    deathRate() {
      if (this.last2) {
        const date0 = new Date(this.last2[0].date)
        const date1 = new Date(this.last2[1].date)
        const seconds = Math.ceil(date0 - date1)
        return (this.last2[0].deaths - this.last2[1].deaths) / seconds
      }
      return null
    },
  },
  mounted() {
    this.start()
  },
  methods: {
    format(number) {
      return number ? Math.floor(number).toLocaleString() : ''
    },
    start() {
      setInterval(() => this.incrementCount(), 1 / this.deathRate)
    },
    incrementCount() {
      if (this.count) {
        this.count += 1
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
