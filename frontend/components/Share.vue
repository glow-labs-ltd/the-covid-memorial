<template>
  <div class="share shadow">
    <h2>Share your memoriam</h2>
    <p>
      In order to protect your comments we only allow people to comment if you
      give them the special link to do it.
    </p>
    <p>
      <strong>
        NOTE: Please make sure you make a note of the commenting link as it
        won’t be available after you leave this screen.
      </strong>
    </p>
    <div class="links">
      <div>
        <h3>Share: Allow comments</h3>
        <div class="url">
          <input type="text" :value="linkComments" readonly />
          <CopyButton @click="copy(linkComments)" />
        </div>
        <div class="social">
          <a
            v-if="facebookCommentsShare"
            :href="facebookCommentsShare"
            target="_blank"
            rel="noopener noreferrer"
          >
            <img
              src="~/assets/images/facebook-icon.svg"
              alt="facebook share with comments"
            />
          </a>
          <a
            v-if="twitterCommentsShare"
            :href="twitterCommentsShare"
            target="_blank"
            rel="noopener noreferrer"
          >
            <img
              src="~/assets/images/twitter-icon.svg"
              alt="twitter share with comments"
            />
          </a>
        </div>
      </div>
      <div class="divider"></div>
      <div>
        <h3>Share: No comments</h3>
        <div class="url">
          <input type="text" :value="linkNoComments" readonly />
          <CopyButton @click="copy(linkNoComments)" />
        </div>
        <div class="social">
          <a
            v-if="facebookNoCommentsShare"
            :href="facebookNoCommentsShare"
            target="_blank"
            rel="noopener noreferrer"
          >
            <img
              src="~/assets/images/facebook-icon.svg"
              alt="facebook share without comments"
            />
          </a>
          <a
            v-if="twitterNoCommentsShare"
            :href="twitterNoCommentsShare"
            target="_blank"
            rel="noopener noreferrer"
          >
            <img
              src="~/assets/images/twitter-icon.svg"
              alt="twitter share without comments"
            />
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { clipboardCopy } from '@/utilities/clipboard'

export default {
  props: {
    name: {
      type: String,
      default: null,
    },
  },
  computed: {
    linkComments() {
      return process.client ? window.location.href : null
    },
    linkNoComments() {
      if (process.client) {
        const full = window.location.href
        return full.substring(0, full.lastIndexOf('/'))
      }
      return null
    },
    shareText() {
      return this.name
        ? `${this.name} - The COVID Memorial`
        : 'The COVID Memorial'
    },
    facebookCommentsShare() {
      return process.client ? this.facebookShare(this.linkComments) : null
    },
    facebookNoCommentsShare() {
      return process.client ? this.facebookShare(this.linkNoComments) : null
    },
    twitterCommentsShare() {
      return process.client ? this.twitterShare(this.linkComments) : null
    },
    twitterNoCommentsShare() {
      return process.client ? this.twitterShare(this.linkNoComments) : null
    },
  },
  methods: {
    copy(link) {
      clipboardCopy(link)
    },
    facebookShare(link) {
      return `https://www.facebook.com/sharer/sharer.php?u=${link}&title=${this.shareText}`
    },
    twitterShare(link) {
      return `https://twitter.com/intent/tweet?text=${this.shareText}&url=${link}`
    },
  },
}
</script>

<style lang="scss" scoped>
.share {
  background-color: $surface;
  padding: 2rem;

  h2 {
    font-size: 3.75rem;
  }

  p {
    font-size: 1.75rem;
    margin: 1rem 0;
  }

  .links {
    display: grid;
    grid-template: auto / 1fr;
    grid-gap: 1rem;
    margin: 2rem 0;

    @media (min-width: $phone) {
      grid-template: auto / 1fr auto 1fr;
      grid-gap: 2.5rem;
    }

    .divider {
      border-left: 1px solid $primary-light;
    }

    h3 {
      margin-bottom: 1rem;
    }

    .url {
      display: grid;
      grid-template: auto / 1fr auto;
      grid-gap: 1rem;

      input {
        font-size: 1.5rem;
      }
    }

    .social {
      display: grid;
      grid-template: auto / repeat(2, auto) 1fr;
      grid-gap: 2rem;
      margin-top: 1rem;

      img {
        width: 4.25rem;
        height: 4.25rem;
      }
    }
  }
}
</style>
