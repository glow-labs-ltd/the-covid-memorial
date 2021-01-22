<template>
  <div class="chart-background">
    <transition-group name="fade-slow" tag="div" class="chart-wrapper">
      <ChartOverview v-if="$store.state.overview" key="overview" />
      <ChartMemoriam
        v-else
        key="memoriam"
        @add="addNodeClick"
        @view="viewNodeClick"
      />
    </transition-group>
  </div>
</template>

<script>
export default {
  methods: {
    addNodeClick() {
      this.$store.commit('setAddModal', !this.$store.state.addModal)
    },
    viewNodeClick(deceasedId) {
      this.$router.push({ name: 'memoriam-slug', params: { slug: deceasedId } })
    },
  },
}
</script>

<style lang="scss" scoped>
.chart-background {
  width: 100%;
  height: 100%;
  background-color: $background;
}

.chart-wrapper {
  width: 100%;
  height: 100%;
}
</style>
