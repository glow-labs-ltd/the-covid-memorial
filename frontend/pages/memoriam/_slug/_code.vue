<template>
  <div class="container">
    <Memoriam
      :slug="this.$route.params.slug"
      :code="this.$route.params.code"
      @close="close"
    />
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
