<template>
  <div>
    <button @click="buttonClick">
      <span>Enter the memorial</span>
    </button>
  </div>
</template>

<script>
export default {
  methods: {
    buttonClick() {
      this.$store.commit('setOverviewTransition', true)
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

  span {
    vertical-align: middle;
    margin: 0 1rem;
  }
}
</style>
