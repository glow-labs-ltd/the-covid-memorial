<template>
  <button @click="$emit('click')">
    <img src="~/assets/images/copy-icon.svg" />
    COPY LINK
  </button>
</template>

<script>
export default {}
</script>

<style lang="scss" scoped>
button {
  border: none;
  padding: 0;
  border-radius: 0;
  font-size: 1rem;

  img {
    width: 2.1rem;
    height: 2.4rem;
    margin: 0 auto 2px;
  }
}
</style>
