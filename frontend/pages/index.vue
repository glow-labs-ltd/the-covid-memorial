<template>
  <div>
    <div class="button-wrapper">
      <transition name="fade-slow" mode="out-in">
        <AddButton v-if="!$store.state.overview" class="add-button" />
      </transition>
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
  right: 3rem;

  @media (min-width: $tablet) {
    right: 5rem;
  }

  > * {
    margin-bottom: 1.5rem;
  }
}
</style>
