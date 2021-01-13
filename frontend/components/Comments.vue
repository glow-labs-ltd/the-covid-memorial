<template>
  <div>
    <AddComment :deceased-id="deceasedId" />
    <div class="comments">
      <div v-for="comment in comments" :key="comment.id" class="comment">
        <h4 class="author">{{ comment.author }}</h4>
        <p class="message">{{ comment.message }}</p>
      </div>
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
  },
  computed: {
    comments() {
      return this.$store.state.comment.comments
    },
  },
  mounted() {
    this.$store.dispatch('comments/getComments', this.deceasedId)
  },
}
</script>

<style lang="scss" scoped>
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
</style>
