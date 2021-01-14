<template>
  <div class="wrapper scroll">
    <div class="limit-width">
      <div class="close">
        <a href="#" @click.prevent="$emit('close')"
          ><img src="~/assets/images/close-icon.svg" alt="Close"
        /></a>
      </div>
      <Share v-if="codeVerified" :name="name" class="share" />
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
            <Comments v-if="id" :deceased-id="id" :code="codeVerified" />
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
    const data = await this.$axios.$get(
      this.code
        ? `deceased/${this.slug}/?c=${this.code}`
        : `deceased/${this.slug}/`
    )
    this.memoriam = data
  },
  data() {
    return {
      memoriam: null,
    }
  },
  computed: {
    id() {
      return this.memoriam?.id
    },
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
      return this.memoriam?.image || require('~/assets/images/placeholder.jpg')
    },
    colourClass() {
      if (this.memoriam?.colour) {
        return `colour--${this.memoriam.colour}`
      }
      return 'colour--7'
    },
    codeVerified() {
      return this.memoriam?.can_comment ? this.code : null
    },
  },
}
</script>

<style lang="scss" scoped>
.wrapper {
  padding: 2rem 0;

  @media (min-width: $tablet) {
    padding: 8rem 0;
  }
}

.limit-width {
  max-width: 100rem;
  margin: 0 auto;
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

  @media (min-width: $tablet) {
    grid-template: auto / repeat(2, 1fr);
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
