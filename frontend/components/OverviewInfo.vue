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
          class="overview-info-panel__wrapper"
        >
          <div class="close">
            <a href="" @click.prevent="buttonClick"
              ><img src="~/assets/images/close-icon.svg" alt="Close"
            /></a>
          </div>
          <div class="overview-info-panel">
            <h2>What am I looking at?</h2>
            <p>
              You are viewing a graphical representation of the global impact of
              COVID-19. The growing number of dots represents the number of
              people around the world who sadly died in the last 24 hours as a
              result of COVID. Enter the memorial to discover their stories,
              told by their loved ones.
            </p>
          </div>
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
      showInfo: null,
    }
  },
  mounted() {
    setTimeout(
      function () {
        if (this.showInfo === null) this.showInfo = true
      }.bind(this),
      5000
    )
  },
  methods: {
    buttonClick() {
      this.showInfo = !this?.showInfo ?? false
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

  h2 {
    font-size: 2.5rem;

    @media (min-width: $tablet) {
      font-size: 3rem;
    }
  }

  p {
    margin-top: 1rem;
    font-size: 1.6rem;
    line-height: 1.5;

    @media (min-width: $tablet) {
      font-size: 1.8rem;
    }
  }

  .close {
    position: absolute;
    top: -5rem;
    right: 0;
  }

  &-panel__wrapper {
    position: absolute;
    bottom: 10rem;
    width: calc(100vw - 6rem);
    z-index: 1;

    @media (min-width: $tablet) {
      left: 8rem;
      bottom: 8rem;
      width: 48rem;
    }
  }

  &-panel {
    padding: 3rem;
    background-color: $surface;
    box-shadow: 0px 0px 16px 1px rgba($color: #090446, $alpha: 0.25);

    @media (min-width: $tablet) {
      padding: 4rem;
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
