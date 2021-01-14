<template>
  <div>
    <div class="button-wrapper">
      <AddButton v-if="!$store.state.overview" class="add-button" />
      <OverviewButton class="overview-button" />
    </div>
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
.button-wrapper {
  position: absolute;
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
  flex-direction: column;
  top: 5rem;
  right: 5rem;

  > * {
    margin-bottom: 2rem;
  }
}
</style>
