<template>
  <div class="add-comment">
    <transition name="fade-slow" mode="out-in">
      <form v-if="!done" id="comment-form" @submit.prevent="submit">
        <h3>Add a comment</h3>
        <input
          v-model="author"
          name="name"
          type="text"
          placeholder="Your name"
          maxlength="256"
          required
        />

        <textarea
          v-model="message"
          type="text"
          name="message"
          rows="3"
          placeholder="Your message"
          maxlength="240"
          required
        />

        <div class="submit-wrapper">
          <input
            type="submit"
            :value="loading ? 'Loading' : 'Submit'"
            class="submit"
          />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
      </form>

      <div v-else class="thanks">
        <h3>Your comment has been saved.</h3>
        <h3>Thank you.</h3>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  props: {
    deceasedId: {
      type: Number,
      required: true,
    },
    code: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      author: '',
      message: '',
      loading: false,
      done: false,
    }
  },
  computed: {
    error() {
      const error = this.$store.state.comment.error
      if (error?.code) {
        return 'Your link appears to be incorrect.'
      }
      if (error) {
        return 'An error occured submitting your comment. Please try again later.'
      }
      return null
    },
  },
  methods: {
    async submit() {
      if (this.loading) return

      this.loading = true
      const data = {
        author: this.author,
        message: this.message,
        deceased: this.deceasedId,
        code: this.code,
      }
      const response = await this.$store.dispatch('comment/postComment', data)
      if (response) {
        this.done = true
      }
      this.loading = false
    },
  },
}
</script>

<style lang="scss" scoped>
.add-comment {
  color: $primary;

  h3 {
    font-size: 2rem;
  }

  label {
    font-size: 1.5rem;
  }

  h3,
  input,
  textarea {
    margin: 0.5rem 0 1rem;
  }

  input,
  textarea {
    border: 2px solid $primary;
  }

  .submit-wrapper {
    text-align: right;
  }

  .submit {
    background-color: $secondary;
    color: $surface;
    max-width: 40%;
    margin-left: auto;
  }

  .thanks {
    text-align: center;
  }
}
</style>
