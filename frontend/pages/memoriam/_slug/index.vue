<template>
  <div class="container">
    <Memoriam :slug="this.$route.params.slug" @close="close" />
  </div>
</template>

<script>
export default {
  transition: {
    name: 'fade-slow',
    mode: '',
  },
  methods: {
    close() {
      this.$router.push('/')
    },
  },
}
</script>

<style lang="scss" scoped></style>
