<template>
  <div>
    <AddButton class="add-button" />
    <AddMemoriam />
  </div>
</template>

<script>
export default {
  mounted() {
    this.$store.dispatch('getDeceased')
  },
  methods: {},
}
</script>

<style lang="scss" scoped>
.add-button {
  position: absolute;
  top: 5rem;
  right: 5rem;
}
</style>
