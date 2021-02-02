<template>
  <div class="copy">
    <transition name="fade-fast" mode="out-in">
      <div v-if="showAffirm" class="copy-affirm">Copied</div>
    </transition>
    <button @click="buttonClick">
      <img src="~/assets/images/copy-icon.svg" />
      COPY LINK
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showAffirm: false,
    }
  },
  methods: {
    buttonClick() {
      this.$emit('click')
      this.showAffirm = true
      setTimeout(
        function () {
          this.showAffirm = false
        }.bind(this),
        1500
      )
    },
  },
}
</script>

<style lang="scss" scoped>
.copy {
  position: relative;

  button {
    border: none;
    padding: 0;
    border-radius: 0;
    font-size: 1rem;
    box-shadow: none;

    img {
      width: 2.1rem;
      height: 2.4rem;
      margin: 0 auto 2px;
    }
  }

  &-affirm {
    position: absolute;
    bottom: 4rem;
    left: 50%;
    transform: translate(-50%, 0);
    z-index: 1;
    text-align: center;
    background-color: $primary;
    color: $surface;
    border-radius: 1rem;
    padding: 1rem;
    font-size: 1.5rem;
  }
}
</style>
