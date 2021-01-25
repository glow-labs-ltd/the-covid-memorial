<template>
  <transition name="fade-slow" mode="out-in">
    <div v-if="showInstructions" class="instructions">
      <img src="~/assets/images/mouse-icon.svg" />
      <span class="touch">Drag to explore</span>
      <span class="mouse">Click and drag to explore</span>
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
      8000
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
  min-width: 53rem;

  img {
    width: 5rem;
    height: 5rem;
    display: inline;
    vertical-align: middle;

    @media (pointer: coarse) {
      width: 4rem;
      height: 4rem;
      content: url('~assets/images/touch-icon.svg');
    }
  }

  span {
    vertical-align: middle;
    margin: 0 1rem;
  }

  span.touch {
    display: none;
  }

  @media (pointer: coarse) {
    min-width: 40rem;

    span.touch {
      display: inline;
    }

    span.mouse {
      display: none;
    }
  }
}
</style>
