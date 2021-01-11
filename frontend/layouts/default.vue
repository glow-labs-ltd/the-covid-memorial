<template>
  <div>
    <CovidChart class="background" @add="addNodeClick" @view="viewNodeClick" />
    <Nuxt />
    <SideMenu />
    <NavBar />
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

<style lang="scss">
html {
  font-family: 'Lora', serif;
  font-size: 8px;
  word-spacing: 1px;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
}

body {
  font-size: 2rem;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
}

:focus {
  box-shadow: 0 0 0 4px $active;
  outline: none;
}

.container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
}

img {
  display: block;
}

button {
  display: inline-block;
  border: 4px solid black;
  background: $surface;
  border-radius: 6rem;
  font-size: 2rem;
  color: $primary;
  font-weight: 700;
  padding: 2rem;
  font-family: inherit;
  cursor: pointer;
}

input,
textarea {
  border: 2px solid black;
  border-radius: 6rem;
  font-size: 2rem;
  font-family: inherit;
  padding: 1rem 2rem;
  min-height: 2.7em;
  width: 100%;
}

input[type='checkbox'] {
  display: inline-block;
  width: 3rem;
  height: 2rem;
  vertical-align: middle;
}

textarea {
  border-radius: 1rem;
}

label {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 1rem;
}

.colour--0 {
  background-color: $palette1;
}
.colour--1 {
  background-color: $palette2;
}
.colour--2 {
  background-color: $palette3;
}
.colour--3 {
  background-color: $palette4;
}
.colour--4 {
  background-color: $palette5;
}
.colour--5 {
  background-color: $palette6;
}
.colour--6 {
  background-color: $palette7;
}
.colour--7 {
  background-color: $palette8;
}

.fade-slow-enter-active,
.fade-slow-leave-active {
  transition: all $slow $standard-easing;
}
.fade-slow-enter,
.fade-slow-leave-to {
  opacity: 0;
}

.fade-fast-enter-active,
.fade-fast-leave-active {
  transition: all $fast $standard-easing;
}
.fade-fast-enter,
.fade-fast-leave-to {
  opacity: 0;
}
</style>
