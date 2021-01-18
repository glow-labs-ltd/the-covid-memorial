<template>
  <div>
    <button aria-label="Zoom out to overview" @click="buttonClick">
      <img src="~/assets/images/zoom-out-icon.svg" />
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
  padding: 1rem;

  img {
    width: 4.25rem;
    height: 4.25rem;
    display: inline;
    vertical-align: middle;

    @media (min-width: $tablet) {
      width: 6.25rem;
      height: 6.25rem;
    }
  }
}
</style>
