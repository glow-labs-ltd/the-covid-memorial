<template>
  <div class="wrapper">
    <div class="close">
      <a href="#" @click.prevent="$emit('close')"
        ><img src="~/assets/images/close-icon.svg" alt="Close"
      /></a>
    </div>
    <Share v-if="correctCode" class="share" />
    <div class="memoriam shadow">
      <div class="left">
        <img class="portrait" :src="image" />
        <div class="colour-bar" :class="colourClass"></div>
        <div class="details">
          <h1 class="name">{{ name }}</h1>
          <h2 class="city">{{ city }}</h2>
          <p class="age"></p>
        </div>
      </div>
      <div class="right">
        <div>
          <p class="message">{{ message }}</p>
          <div class="comment-section">
            <h3>Add a comment</h3>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    slug: {
      type: String,
      required: true,
    },
    code: {
      type: String,
      default: null,
    },
  },
  async fetch() {
    const response = await this.$axios.get(
      this.code
        ? `deceased/${this.slug}/?c=${this.code}`
        : `deceased/${this.slug}/`
    )
    this.memoriam = response.data
  },
  data() {
    return {
      memoriam: null,
    }
  },
  computed: {
    name() {
      return this.memoriam?.name
    },
    city() {
      return this.memoriam?.city
    },
    message() {
      const message = this.memoriam?.message
      if (message) {
        return `"${message}"`
      }
      return null
    },
    image() {
      return this.memoriam?.image
    },
    colourClass() {
      if (this.memoriam?.colour) {
        return `colour--${this.memoriam.colour}`
      }
      return 'colour--7'
    },
    correctCode() {
      if (this.code) return true
      return false
    },
  },
}
</script>

<style lang="scss" scoped>
.wrapper {
  margin: 2rem auto 0;
  max-width: 100rem;
  max-height: 75%;

  @media (min-width: $tablet) {
    margin: 8rem auto 0;
  }

  @media (min-width: $desktop) {
    margin: 10rem auto 0;
  }
}

.share {
  margin-bottom: 2rem;
}

.memoriam {
  display: grid;
  grid-template: auto / 1fr;
  height: 100%;
  width: 100%;
  text-align: left;
  background-color: $surface;
  overflow-y: scroll;
  padding-bottom: 10rem; // make sure you can scroll and view bottom

  @media (min-width: $tablet) {
    grid-template: 75vh / repeat(2, 1fr);
    max-height: 75vh;
    overflow-y: hidden;
    padding-bottom: 0;
  }

  .portrait {
    object-fit: cover;
    width: 100%;
    max-height: 50rem;
  }

  .colour-bar {
    height: 1rem;
  }

  .details {
    margin: 2rem;
  }

  .name {
    font-size: 2.25rem;
  }

  .age,
  .city {
    font-size: 1.5rem;
  }

  .left {
    max-height: 100%;
  }

  .right {
    padding: 2rem;
    max-height: 100%;

    @media (min-width: $tablet) {
      overflow-y: scroll;
    }
  }

  .message {
    margin: 2rem 1rem 2rem 0;
    text-align: justify;
    text-justify: inter-word;
    white-space: pre-line;
  }

  .comment-section {
    height: 20rem;
  }
}

.close {
  img {
    width: 4rem;
    height: 4rem;
    margin: 0 0 1rem auto;
  }
}
</style>
