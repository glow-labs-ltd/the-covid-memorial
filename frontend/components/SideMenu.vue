<template>
  <div>
    <transition name="slide">
      <aside v-show="sideMenu">
        <NuxtLink to="/" class="logo">
          <img
            src="~/assets/images/the-covid-memorial-logo.svg"
            alt="The COVID Memorial"
          />
        </NuxtLink>
        <div class="links">
          <NuxtLink to="/about">About</NuxtLink>
          <a href="">Data sources</a>
          <a href="">Terms &amp; Privacy</a>
          <a href="">Contact TCM</a>
        </div>
        <div class="foot">
          <img src="~/assets/images/instagram-icon.svg" alt="Instagram" />
          <img src="~/assets/images/twitter-icon.svg" alt="Twitter" />
          <span>© The COVID Memorial is Copyright 2021</span>
        </div>
      </aside>
    </transition>
  </div>
</template>

<script>
export default {
  computed: {
    sideMenu() {
      return this.$store.state.sideMenuOpen
    },
  },
  watch: {
    $route() {
      this.close()
    },
  },
  methods: {
    close() {
      return this.$store.commit('closeSideMenu')
    },
  },
}
</script>

<style lang="scss" scoped>
aside {
  background-color: $surface;
  color: $primary;
  overflow: hidden;
  position: fixed;
  top: 0;
  right: 0;
  height: 100vh;
  max-width: 90vw;
  min-width: 40rem;

  display: grid;
  grid-template: auto auto 1fr / 1fr;
  grid-gap: 4rem;
  padding: 4rem;

  @media (min-width: $desktop) {
    right: 0;
    max-height: none;
  }

  .logo {
    width: 50%;
    margin-left: auto;
  }

  .links {
    a {
      font-size: 3.75rem;
      text-decoration: none;
      color: $primary;
      display: block;
      padding: 1rem 0;
    }
  }

  .foot {
    margin-top: auto;
    padding-bottom: 10rem;
    display: grid;
    grid-template: auto / auto auto 1fr;
    grid-gap: 1rem;

    img {
      width: 4.25rem;
      height: 4.25rem;
    }

    span {
      font-size: 1.75rem;
      margin: auto;
    }
  }
}

.slide-enter-active,
.slide-leave-active {
  animation-fill-mode: forwards;
  animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
}

.slide-enter-active {
  animation-duration: 0.3s;
  animation-name: slideXRightIn;
}

.slide-leave-active {
  animation-duration: 0.2s;
  animation-name: slideXRightOut;
}

.slide-enter,
.slide-leave-to {
  opacity: 0;
}

@keyframes slideXRightIn {
  from {
    opacity: 0;
    transform: translateX(8rem);
  }
  to {
    opacity: 1;
  }
}
.slideXRightIn {
  animation-name: slideXRightIn;
}
@keyframes slideXRightOut {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
    transform: translateX(8rem);
  }
}
.slideXRightOut {
  animation-name: slideXRightOut;
}
</style>
