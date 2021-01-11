<template>
  <div class="container">
    <div class="search-results">
      <h3>{{ count }} People</h3>
      <div class="results">
        <div v-for="result in results" :key="result.id" class="result">
          <img class="portrait" src="~/assets/images/placeholder.jpg" />
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
  computed: {
    count() {
      return this.$store.state.results?.count
    },
    results() {
      return this.$store.state.results?.results
    },
  },
  mounted() {
    this.$store.dispatch('getDeceased')
  },
  methods: {
    colourClass(colour) {
      if (colour) {
        return `colour--${colour}`
      }
      return null
    },
  },
}
</script>

<style lang="scss" scoped>
.search-results {
  padding: 4rem;
  height: 100%;
  width: 100%;
  text-align: left;

  @media (min-width: $tablet) {
    padding: 8rem;
  }

  @media (min-width: $desktop) {
    padding: 12rem;
  }

  h3 {
    margin-bottom: 1rem;
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
      max-width: 100%;
      display: block;
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
