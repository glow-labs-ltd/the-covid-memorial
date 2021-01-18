<template>
  <nav class="navbar">
    <NuxtLink to="/" class="logo">
      <img
        src="~/assets/images/the-covid-memorial-logo.svg"
        alt="The COVID Memorial"
      />
    </NuxtLink>
    <DeathCount />
    <img
      src="~/assets/images/search-icon.svg"
      class="nav-item search"
      alt="Search"
      @click="searchClick"
    />
    <transition name="slide" mode="out-in">
      <img
        :key="menuIcon"
        :src="menuIcon"
        class="nav-item menu"
        alt="Menu"
        @click="menuClick"
      />
    </transition>
  </nav>
</template>

<script>
export default {
  computed: {
    menuIcon() {
      if (!this.$store.state.sideMenuOpen) {
        return require('~/assets/images/menu-icon.svg')
      }
      return require('~/assets/images/menu-close-icon.svg')
    },
  },
  methods: {
    menuClick() {
      this.$store.commit('toggleSideMenu')
    },
    searchClick() {
      this.$router.push('/search')
    },
  },
}
</script>

<style lang="scss" scoped>
.navbar {
  display: grid;
  grid-template: auto / auto 1fr auto auto;
  background-color: $surface;
  color: $primary;
  overflow: hidden;
  position: fixed;
  bottom: 0;
  width: 100%;
  padding: 2rem;
  grid-gap: 2rem;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.5);
  height: 10rem;

  @media (min-width: $tablet) {
    grid-template: auto / auto 1fr auto auto;
    grid-gap: 4rem;
    padding: 2rem 4rem;
  }

  > * {
    align-self: center;
  }

  .logo {
    width: 6rem;
    max-height: 3rem;

    @media (min-width: $phone) {
      width: 10rem;
      max-height: 5rem;
    }

    @media (min-width: $tablet) {
      width: 13rem;
      max-height: 6rem;
    }
  }

  .nav-item {
    cursor: pointer;
  }

  .search {
    width: 3.5rem;
    height: 3.5rem;
  }

  .menu {
    width: 5.75rem;
    height: 3.75rem;
  }
}

.slide-leave-active,
.slide-enter-active {
  transition: $fast;
}
.slide-enter {
  transform: translate(25%, 0);
  opacity: 0;
}
.slide-leave-to {
  transform: translate(-25%, 0);
  opacity: 0;
}
</style>
