<template>
  <div class="wrapper scroll">
    <div class="limit-width">
      <div class="close">
        <button v-if="codeVerified" @click="toggleShareExpanded">
          Share this memorial
        </button>
        <a href="#" @click.prevent="$emit('close')"
          ><img src="~/assets/images/close-icon.svg" alt="Close"
        /></a>
      </div>
      <Share :name="name" :expanded="shareExpanded" class="share-panel" />
      <div class="memoriam shadow">
        <div class="left">
          <img v-if="image" class="portrait" :src="image" />
          <div class="colour-bar" :class="colourClass"></div>
          <div class="details">
            <h1 class="name">{{ name }}</h1>
            <h3 class="dates">{{ dates }}</h3>
            <h2 class="city">{{ cityCountry }}</h2>
            <h2 class="occupation">{{ occupation }}</h2>
          </div>
        </div>
        <div class="right">
          <div>
            <p class="message">{{ message }}</p>
            <Comments
              v-if="id"
              :deceased-id="id"
              :code="codeVerified"
              :has-content="message != null"
            />
            <div v-if="error" class="not-found">
              <h2>Memorial not found</h2>
              <p>Thank you for visiting The COVID Memorial.</p>
              <p>
                Unfortunately, the individual memorial you are looking for does
                not exist. Please check you have the correct link.
              </p>
              <p>
                The memorial you are looking for may have been removed due to
                one of the following reasons:
              </p>
              <ul>
                <li>We received a request to delete the memorial</li>
                <li>
                  The memorial violated our
                  <NuxtLink to="/terms">terms of service</NuxtLink>
                </li>
              </ul>
            </div>
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
    try {
      const data = await this.$axios.$get(
        this.code
          ? `deceased/${this.slug}/?c=${this.code}`
          : `deceased/${this.slug}/`
      )
      this.memoriam = data
    } catch (e) {
      this.error = e?.response?.status ?? 'error'
    }
  },
  data() {
    return {
      memoriam: null,
      error: null,
      shareExpanded: false,
    }
  },
  computed: {
    id() {
      return this.memoriam?.id
    },
    name() {
      return this.memoriam?.name
    },
    occupation() {
      return this.memoriam?.occupation
    },
    cityCountry() {
      const city = this.memoriam?.city ?? ''
      const country = this.memoriam?.country ?? ''
      if (city && country) {
        return `${city}, ${country}`
      }
      return `${city} ${country}`
    },
    dates() {
      const birth = this.memoriam?.birth_date
        ? new Date(this.memoriam?.birth_date)
        : null
      const death = this.memoriam?.death_date
        ? new Date(this.memoriam?.death_date)
        : null
      const age = this.memoriam?.age

      if (birth & death) {
        const age = Math.floor((death - birth) / (1000 * 60 * 60 * 24 * 365))
        return `${birth.getFullYear()} - ${death.getFullYear()} (${age} years)`
      }

      let dates = ''
      if (birth) dates = `Born ${birth.getFullYear()}`
      if (death) dates = `Died ${death.getFullYear()}`
      if (age) dates += ` (${age} years)`
      return dates
    },
    message() {
      const message = this.memoriam?.message
      if (message) return `"${message}"`
      return null
    },
    image() {
      return this.memoriam?.image
    },
    colourClass() {
      const cssClass = []
      if (this.memoriam?.colour) {
        cssClass.push(`colour--${this.memoriam.colour}`)
      } else {
        cssClass.push('colour--7')
      }

      if (!this.memoriam?.image) {
        cssClass.push('colour-large')
      }

      return cssClass
    },
    codeVerified() {
      return this.memoriam?.can_comment ? this.code : null
    },
  },
  methods: {
    toggleShareExpanded() {
      this.shareExpanded = !this.shareExpanded
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

.share-panel {
  margin-top: 1rem;
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

  .colour-large {
    height: 50rem;
  }

  .details {
    margin: 2rem;
  }

  .name {
    font-size: 2.25rem;
  }

  .dates,
  .city,
  .occupation {
    font-size: 1.75rem;
    font-weight: 400;
    margin: 1rem 0;
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0 2rem;

  @media (min-width: $tablet) {
    align-items: flex-end;
    margin: 0;
  }

  a {
    margin-left: auto;
  }

  img {
    width: 4rem;
    height: 4rem;
    border: 3px solid $surface;
    border-radius: 50%;
  }
}

.not-found {
  h2 {
    margin-bottom: 2rem;
  }

  p {
    margin-bottom: 2rem;
    line-height: 1.4;
  }

  li {
    margin-bottom: 1rem;
  }
}
</style>
