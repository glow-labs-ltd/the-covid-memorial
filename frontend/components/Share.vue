<template>
  <div>
    <transition name="share">
      <div v-if="expanded" class="share shadow">
        <div class="share__content">
          <p>
            <strong>
              Please bookmark this page or make a note of these links, as they
              will no longer be available once you leave this screen.
            </strong>
          </p>
          <client-only>
            <div class="links">
              <div>
                <h3>Share: Allow comments</h3>
                <p>
                  Only the people you share this link with can leave comments on
                  this memorial.
                </p>
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
                  <a
                    v-if="whatsappCommentsShare"
                    :href="whatsappCommentsShare"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <img
                      src="~/assets/images/whatsapp-icon.svg"
                      alt="whatsapp share with comments"
                    />
                  </a>
                </div>
              </div>
              <div class="divider"></div>
              <div>
                <h3>Share: No comments</h3>
                <p>
                  This link allows people to view this memorial but prevents
                  them from leaving comments.
                </p>
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
                  <a
                    v-if="whatsappNoCommentsShare"
                    :href="whatsappNoCommentsShare"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <img
                      src="~/assets/images/whatsapp-icon.svg"
                      alt="whatsapp share without comments"
                    />
                  </a>
                </div>
              </div>
            </div>
          </client-only>
        </div>
      </div>
    </transition>
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
    expanded: {
      type: Boolean,
      default: false,
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
    whatsappCommentsShare() {
      return process.client ? this.whatsappShare(this.linkComments) : null
    },
    whatsappNoCommentsShare() {
      return process.client ? this.whatsappShare(this.linkNoComments) : null
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
    whatsappShare(link) {
      return `https://api.whatsapp.com/send?text=${this.shareText}%0D%0A${link}`
    },
  },
}
</script>

<style lang="scss" scoped>
.share {
  background-color: $surface;

  &__content {
    padding: 2rem;
  }

  h2 {
    font-size: 3.25rem;
    cursor: pointer;

    @media (min-width: $phone) {
      font-size: 3.75rem;
    }

    button {
      margin-left: 2rem;
      padding: 1rem;
    }

    img {
      width: 2.5rem;
      height: 2.5rem;
      transition: transform $slow;
    }

    .expanded {
      transform: rotate(180deg);
    }
  }

  p {
    font-size: 1.75rem;
    margin: 1rem 0;
  }

  .links {
    display: grid;
    grid-template: auto / 1fr;
    grid-gap: 1rem;
    margin: 2rem 0 0;

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

.share-enter-active,
.share-leave-active {
  transition: all $slow $standard-easing;
  max-height: 48rem;

  @media (min-width: $tablet) {
    max-height: 32rem;
  }
}
.share-enter,
.share-leave-to {
  opacity: 0;
  max-height: 0px;
}
</style>
