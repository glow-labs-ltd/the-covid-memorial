<template>
  <div>
    <div class="button-wrapper button-wrapper__left">
      <transition name="fade-slow" mode="out-in">
        <ZoomOutButton
          v-if="!$store.state.overviewTransition && !$store.state.overview"
        />
      </transition>
    </div>
    <div class="button-wrapper button-wrapper__right">
      <transition name="fade-slow" mode="out-in">
        <OverviewButton
          v-if="!$store.state.overviewTransition && $store.state.overview"
          class="overview-button"
        />
      </transition>
      <transition name="fade-slow" mode="out-in">
        <AddButton v-if="!$store.state.overview" class="add-button" />
      </transition>
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
  flex-direction: column;
  top: 5rem;

  &__right {
    justify-content: flex-end;
    align-items: flex-end;
    right: 3rem;

    @media (min-width: $tablet) {
      right: 5rem;
    }
  }

  &__left {
    justify-content: flex-start;
    align-items: flex-start;
    left: 3rem;

    @media (min-width: $tablet) {
      left: 5rem;
    }
  }

  > * {
    margin-bottom: 1.5rem;
  }
}
</style>
