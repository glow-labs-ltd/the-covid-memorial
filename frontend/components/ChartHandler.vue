<template>
  <div class="chart-background">
    <transition-group name="fade-slow" tag="div" class="chart-wrapper">
      <!--
      <ChartOverview
        v-show="zoomedOut"
        key="overview"
        @zoomIn="zoomedOut = false"
      />
      -->
      <ChartMemoriam
        key="memoriam"
        @add="addNodeClick"
        @view="viewNodeClick"
        @zoomOut="zoomedOut = true"
      />
    </transition-group>
  </div>
</template>

<script>
export default {
  data() {
    return {
      zoomedOut: true,
    }
  },
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
  width: 100vw;
  height: 100vh;
  background-color: $background;
}

.chart-wrapper {
  width: 100%;
  height: 100%;
}
</style>
