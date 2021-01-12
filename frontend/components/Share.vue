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
          <input
            id="comments-link"
            type="text"
            :value="linkComments"
            readonly
          />
          <CopyButton @click="copy(linkComments)" />
        </div>
        <div class="social">
          <img src="~/assets/images/facebook-icon.svg" />
          <img src="~/assets/images/twitter-icon.svg" />
        </div>
      </div>
      <div class="divider"></div>
      <div>
        <h3>Share: No comments</h3>
        <div class="url">
          <input
            id="comments-link"
            type="text"
            :value="linkNoComments"
            readonly
          />
          <CopyButton @click="copy(linkNoComments)" />
        </div>
        <div class="social">
          <img src="~/assets/images/facebook-icon.svg" />
          <img src="~/assets/images/twitter-icon.svg" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { clipboardCopy } from '@/utilities/clipboard'

export default {
  computed: {
    linkComments() {
      if (process.client) {
        return window.location.href
      }
      return null
    },
    linkNoComments() {
      if (process.client) {
        const full = window.location.href
        return full.substring(0, full.lastIndexOf('/'))
      }
      return null
    },
  },
  methods: {
    copy(link) {
      clipboardCopy(link)
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
      display: flex;
      margin-top: 1rem;

      img {
        width: 4.25rem;
        height: 4.25rem;
        margin-right: 2rem;
      }
    }
  }
}
</style>
