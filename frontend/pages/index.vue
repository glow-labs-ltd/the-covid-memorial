<template>
  <div class="container">
    <covid-chart />
    <AddButton class="add-button" />
    <AddMemoriam />
  </div>
</template>

<script>
import CovidChart from '@/components/covid-chart.vue'

export default {
  components: {
    CovidChart,
  },
  mounted() {
    this.$store.dispatch('getDeceased')
  },
}
</script>

<style lang="scss" scoped>
.container {
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  position: relative;
}

.add-button {
  position: absolute;
  top: 5rem;
  right: 5rem;
}
</style>
