<template>
  <transition name="fade-slow" mode="out-in">
    <div v-if="showInstructions" class="instructions">
      <img src="~/assets/images/mouse-icon.svg" />
      <span>Click and drag to explore</span>
    </div>
  </transition>
</template>

<script>
export default {
  data() {
    return {
      timerRunning: true,
    }
  },
  computed: {
    showInstructions() {
      return this.$store.state.firstTime && this.timerRunning
    },
  },
  mounted() {
    setTimeout(
      function () {
        this.timerRunning = false
        this.$store.commit('setFirstTime', false)
      }.bind(this),
      10000
    )
  },
}
</script>

<style lang="scss" scoped>
.instructions {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 3rem;
  font-weight: 700;
  padding: 3rem;
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 12rem;
  pointer-events: none;
  z-index: 10;
  text-align: center;
  min-width: 50rem;

  @media (max-width: $tablet) {
    display: none;
  }

  img {
    width: 5rem;
    height: 5rem;
    display: inline;
    vertical-align: middle;
  }

  span {
    vertical-align: middle;
    margin: 0 1rem;
  }
}
</style>
