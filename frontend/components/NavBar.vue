<template>
  <nav class="navbar">
    <NuxtLink to="/" class="logo">
      <img
        src="~/assets/images/the-covid-memorial-logo.svg"
        alt="The COVID Memorial"
      />
    </NuxtLink>
    <h2 class="lost-count">1,854,764 <span>Sadly lost</span></h2>
    <img src="~/assets/images/search-icon.svg" class="search" alt="Search" />
    <img
      src="~/assets/images/menu-icon.svg"
      class="menu"
      alt="Menu"
      @click="menuClick"
    />
  </nav>
</template>

<script>
export default {
  methods: {
    menuClick() {
      this.$store.commit('toggleSideMenu')
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
  padding: 2rem 4rem;
  grid-gap: 4rem;

  > * {
    align-self: center;
  }

  .logo {
    width: 13rem;
    height: 6rem;
  }

  .lost-count {
    text-align: center;
    font-size: 3.75rem;
    font-weight: 400;

    span {
      font-size: 2.5rem;
    }
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
</style>
