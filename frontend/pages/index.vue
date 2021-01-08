<template>
  <div class="container">
    <covid-chart @add="addNodeClick" @view="viewNodeClick" />
    <AddButton class="add-button" />
    <AddMemoriam />
  </div>
</template>

<script>
export default {
  mounted() {
    this.$store.dispatch('getDeceased')
  },
  methods: {
    addNodeClick() {
      this.$store.commit('setAddModal', !this.$store.state.addModal)
    },
    viewNodeClick(deceasedId) {
      alert(`View memorium id ${deceasedId}`)
    },
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
