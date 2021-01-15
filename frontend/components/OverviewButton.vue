<template>
  <div>
    <button @click="overviewButtonClick">
      <span>{{ text }} </span>
    </button>
  </div>
</template>

<script>
export default {
  computed: {
    text() {
      return this.$store.state.overview
        ? 'Enter the memorial'
        : 'Go to overview'
    },
  },
  methods: {
    overviewButtonClick() {
      this.$store.commit(
        'setOverviewTransition',
        !this.$store.state.overviewTransition
      )
    },
  },
}
</script>

<style lang="scss" scoped>
button {
  font-size: 2rem;
  padding: 1rem;

  @media (min-width: $tablet) {
    font-size: 2.25rem;
    padding: 2rem;
  }

  img {
    width: 4.25rem;
    height: 4.25rem;
    display: inline;
    vertical-align: middle;
  }

  span {
    vertical-align: middle;
    margin: 0 1rem;
  }
}
</style>
