<template>
  <div class="container">
    <div class="search-results scroll">
      <div class="close">
        <a href="#" @click.prevent="close"
          ><img src="~/assets/images/close-icon.svg" alt="Close"
        /></a>
      </div>
      <h3>{{ count }}</h3>
      <div class="results">
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
      </div>
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
      const count = this.$store.state.results?.count
      if (count) return `${this.$store.state.results?.count} People`
      return 'No results'
    },
    results() {
      return this.$store.state.results?.results
    },
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
  },
}
</script>

<style lang="scss" scoped>
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
    padding-bottom: 1rem;
  }

  .close {
    img {
      width: 4rem;
      height: 4rem;
      margin: 0 0 1rem auto;
    }
  }
}

.results {
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
</style>
