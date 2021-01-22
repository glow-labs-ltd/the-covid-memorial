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
          <NuxtLink to="/thank-yous">Thank you's</NuxtLink>
          <NuxtLink to="/data-sources">Data sources</NuxtLink>
          <NuxtLink to="/terms">Terms &amp; Privacy</NuxtLink>
          <NuxtLink to="/donate">Donate</NuxtLink>
        </div>
        <div class="foot">
          <div class="icons">
            <div></div>

            <a href="https://www.instagram.com/covidmemorials/" target="_blank">
              <img src="~/assets/images/instagram-icon.svg" alt="Instagram" />
            </a>
            <a href="https://www.twitter.com/covidmemorials" target="_blank">
              <img src="~/assets/images/twitter-icon.svg" alt="Twitter" />
            </a>
            <a
              href="https://www.facebook.com/The-Covid-Memorial-100915478635289"
              target="_blank"
            >
              <img src="~/assets/images/facebook-icon.svg" alt="Facebook" />
            </a>
          </div>
          <a
            href="mailto:contact@thecovid.memorial"
            target="_blank"
            class="foot__contact"
            >contact@thecovid.memorial</a
          >
          <span
            >© The COVID Memorial Limited<br />Company number: 13152416</span
          >
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
  position: fixed;
  top: 0;
  right: 0;
  max-width: 90vw;
  min-width: 40rem;
  overflow-y: auto;
  display: grid;
  grid-template: auto auto 1fr / 1fr;
  grid-gap: 4rem;
  padding: 4rem 4rem 2rem;
  height: 100vh;
  max-height: calc(100% - 10rem);

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
    margin: auto 0 0;
    display: grid;

    > * {
      margin: 0.75rem 0;
    }

    .icons {
      display: grid;
      grid-template: auto / 1fr auto auto auto;
      grid-gap: 1rem;
    }

    img {
      width: 4.25rem;
      height: 4.25rem;
    }

    span {
      font-size: 1.75rem;
      margin-left: auto;
      text-align: right;
    }

    &__contact {
      grid-column: 1 / -1;
      font-size: 2rem;
      text-align: right;
      text-decoration: none;
      color: $primary;
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
