<template>
  <div>
    <AddComment v-if="code" :deceased-id="deceasedId" :code="code" />
    <hr v-else-if="hasContent" />
    <div v-if="comments.length > 0" class="comments">
      <h3>Comments</h3>
      <div v-for="comment in comments" :key="comment.id" class="comment">
        <h4 class="author">{{ comment.author }}</h4>
        <p class="message">{{ comment.message }}</p>
      </div>
      <transition name="fade-fast">
        <div v-if="moreResults" class="more">
          <button @click="loadMore">Load more</button>
        </div>
      </transition>
    </div>
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
      default: null,
    },
    hasContent: {
      type: Boolean,
      default: true,
    },
  },
  computed: {
    comments() {
      return this.$store.state.comment.comments
    },
    moreResults() {
      return this.$store.state.comment.next
    },
  },
  mounted() {
    this.$store.dispatch('comment/getComments', {
      id: this.deceasedId,
      append: false,
    })
  },
  methods: {
    loadMore() {
      this.$store.dispatch('comment/getComments', {
        id: this.deceasedId,
        append: true,
      })
    },
  },
}
</script>

<style lang="scss" scoped>
.comments {
  h3 {
    font-size: 2.2rem;
  }
}

.comment {
  color: $primary;
  margin: 2rem 0;

  .author {
    font-size: 2.25rem;
    margin: 1rem 0;
  }

  .message {
    font-size: 1.75rem;
  }
}

.more {
  text-align: center;

  button {
    margin: 2rem 0;
    padding: 1rem 6rem;
    background-color: $secondary;
    color: $surface;
  }
}

hr {
  margin: 2rem 0;
}
</style>
