<template>
  <nav class="navbar">
    <NuxtLink to="/" class="logo">
      <img
        src="~/assets/images/the-covid-memorial-logo.svg"
        alt="The COVID Memorial"
      />
    </NuxtLink>
    <h2 class="lost-count">1,854,764 <span>Sadly lost</span></h2>
    <div>
      <transition name="fade-slow">
        <input
          v-show="$store.state.showSearch"
          ref="searchField"
          v-model="searchQuery"
          type="text"
          class="search-field"
          @keyup.enter="search"
        />
      </transition>
    </div>
    <img
      src="~/assets/images/search-icon.svg"
      class="search"
      alt="Search"
      @click="toggleSearch"
    />
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
  computed: {
    searchQuery: {
      get() {
        return this.$store.state.searchQuery
      },
      set(value) {
        this.$store.commit('setSearchQuery', value)
      },
    },
  },
  methods: {
    menuClick() {
      this.$store.commit('toggleSideMenu')
    },
    toggleSearch() {
      this.$store.commit('setShowSearch', !this.$store.state.showSearch)
      if (this.$store.state.showSearch) {
        this.$nextTick(() => {
          this.$refs.searchField.focus()
        })
      }
    },
    search() {
      this.$store.dispatch('search')
      this.$router.push('/search')
    },
  },
}
</script>

<style lang="scss" scoped>
.navbar {
  display: grid;
  grid-template: auto / auto 1fr auto auto auto;
  background-color: $surface;
  color: $primary;
  overflow: hidden;
  position: fixed;
  bottom: 0;
  width: 100%;
  padding: 2rem 4rem;
  grid-gap: 4rem;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.5);

  > * {
    align-self: center;
  }

  .logo {
    width: 10rem;
    max-height: 5rem;

    @media (min-width: $tablet) {
      width: 13rem;
      max-height: 6rem;
    }
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

  .search-field {
    border: none;
    border-bottom: 1px solid $secondary;
    border-radius: 0;
    max-width: 40rem;

    &:focus {
      box-shadow: 0 0 8px -4px $secondary;
      outline: none;
    }
  }

  .menu {
    width: 5.75rem;
    height: 3.75rem;
  }
}
</style>
