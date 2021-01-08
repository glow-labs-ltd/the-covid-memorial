<template>
  <div>
    <button @click="addButtonClick">
      <img src="~/assets/images/add-icon.svg" />
      <span>Add memoriam</span>
    </button>
  </div>
</template>

<script>
export default {
  methods: {
    addButtonClick() {
      this.$store.commit('setAddModal', !this.$store.state.addModal)
    },
  },
}
</script>

<style lang="scss" scoped>
button {
  font-size: 2.25rem;

  img {
    width: 4.25rem;
    height: 4.25rem;
    display: inline;
    vertical-align: middle;
  }

  span {
    vertical-align: middle;
    margin: 0 1rem;
  }
}
</style>
