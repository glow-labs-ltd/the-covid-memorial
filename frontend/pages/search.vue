<template>
  <div class="container">
    <div class="search-results scroll">
      <div class="close">
        <a href="" @click.prevent="close"
          ><img src="~/assets/images/close-icon.svg" alt="Close"
        /></a>
      </div>
      <form class="query shadow" @submit.prevent="search(false)">
        <h1>Search</h1>
        <input
          ref="searchField"
          v-model="searchQuery"
          type="text"
          autocomplete="off"
        />
        <h3>{{ count }}</h3>
      </form>
      <div class="results">
        <transition-group name="fade-group" class="transition">
          <div
            v-for="result in results"
            :key="result.id"
            class="result shadow"
            @click="clickResult(result.slug)"
          >
            <img
              class="portrait"
              :src="result.image || require('~/assets/images/placeholder.jpg')"
            />
            <div class="colour-bar" :class="colourClass(result.colour)"></div>
            <div class="details">
              <h2 class="name">{{ result.name }}</h2>
              <h3 class="city">{{ result.city }}</h3>
            </div>
          </div>
        </transition-group>
      </div>
      <transition name="fade-fast">
        <div v-if="moreResults" class="more">
          <button @click="search(true)">Load more</button>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  transition: {
    name: 'fade-slow',
    mode: '',
  },
  computed: {
    count() {
      const count = this.$store.state.searchCount
      if (count) return `${this.$store.state.searchCount} People`
      return 'No results'
    },
    results() {
      return this.$store.state.searchResults
    },
    moreResults() {
      if (this.$store.state.searchNext) return true
      return false
    },
    searchQuery: {
      get() {
        return this.$store.state.searchQuery
      },
      set(value) {
        this.$store.commit('setSearchQuery', value)
      },
    },
  },
  mounted() {
    this.$refs.searchField.focus()
  },
  methods: {
    colourClass(colour) {
      if (colour) {
        return `colour--${colour}`
      }
      return 'colour--7'
    },
    clickResult(id) {
      this.$router.push({ name: 'memoriam-slug', params: { slug: id } })
    },
    close() {
      this.$router.push('/')
    },
    search(append) {
      this.$store.dispatch('search', append)
    },
  },
}
</script>

<style lang="scss" scoped>
.query {
  padding: 2rem;
  margin-bottom: 2rem;
  background-color: $surface;

  input {
    font-size: 3rem;
    padding: 1rem 0;
    border: none;
    border-bottom: 2px solid $secondary;
    border-radius: 0;
    transition: border-color $fast $standard-easing;

    &:focus {
      box-shadow: none;
      border-bottom: 2px solid $active;
      outline: none;
    }
  }
}

.search-results {
  padding: 2rem;
  width: 100%;
  text-align: left;

  @media (min-width: $tablet) {
    padding: 8rem;
  }

  @media (min-width: $desktop) {
    padding: 10rem;
  }

  h4 {
    margin: 1rem 0;
    a {
      text-decoration: none;
      color: $primary;
      font-size: 2rem;
    }
  }

  h3 {
    padding-top: 2rem;
  }
}

.results > .transition {
  display: grid;
  grid-template: auto / repeat(2, 1fr);
  grid-gap: 2rem;

  @media (min-width: $phone) {
    grid-template: auto / repeat(3, 1fr);
    grid-gap: 2rem;
  }

  @media (min-width: $tablet) {
    grid-template: auto / repeat(4, 1fr);
    grid-gap: 3rem;
  }

  @media (min-width: $desktop) {
    grid-template: auto / repeat(5, 1fr);
    grid-gap: 5rem;
  }

  .result {
    background-color: $surface;

    .portrait {
      width: 100%;
    }

    .colour-bar {
      width: 100%;
      height: 1rem;
    }

    .details {
      margin: 1rem;
    }

    .name {
      font-size: 2rem;
      font-weight: 400;
    }

    .city {
      font-size: 1.6rem;
      font-weight: 400;
      margin-top: 0.5rem;
    }
  }
}

.more {
  text-align: center;

  button {
    margin: 4rem 0 2rem;
    font-size: 2.25rem;
    padding: 2rem 8rem;
    background-color: $secondary;
    color: $surface;
  }
}
</style>
