<template>
  <div class="overview-info">
    <div>
      <button aria-label="What am I looking at?" @click="buttonClick">
        <img src="~/assets/images/info-icon.svg" alt="Info" />
      </button>
      <transition name="fade-slow" mode="out-in">
        <div
          v-if="showInfo"
          v-on-clickaway="buttonClick"
          class="overview-info-panel"
        >
          <h2>What am I looking at?</h2>
          <p>
            You are seeing a graphical representation of the global impact of
            COVID-19. Every dot represents a person who has sadly lost their
            life due to the pandemic. Enter the memorial to discover their
            stories, told by their loved ones.
          </p>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import { mixin as clickaway } from 'vue-clickaway'

export default {
  mixins: [clickaway],
  data() {
    return {
      showInfo: false,
    }
  },
  methods: {
    buttonClick() {
      this.showInfo = !this.showInfo
    },
  },
}
</script>

<style lang="scss" scoped>
.overview-info {
  position: absolute;
  left: 3rem;
  bottom: 12rem;

  button {
    padding: 0;
  }

  p {
    margin-top: 1rem;
    font-size: 1.6rem;
  }

  &-panel {
    position: absolute;
    bottom: 10rem;
    width: calc(100vw - 6rem);
    padding: 4rem;
    background-color: $surface;
    box-shadow: 0px 0px 16px 1px rgba($color: #090446, $alpha: 0.25);

    @media (min-width: $tablet) {
      left: 8rem;
      bottom: 8rem;
      width: 48rem;
    }
  }
}

button {
  padding: 1rem;

  img {
    width: 6.25rem;
    height: 6.25rem;
    display: inline;
    vertical-align: middle;
  }
}
</style>
