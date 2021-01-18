<template>
  <div>
    <ChartHandler />
    <Nuxt />
    <SideMenu />
    <NavBar />
  </div>
</template>

<script>
export default {}
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
  background-color: rgba(0, 0, 0, 0.3);
}

.scroll {
  overflow-y: auto;
  max-height: calc(100% - 10rem);
}

.limit-width {
  max-width: 100rem;
  margin: 0 auto;
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

textarea {
  resize: vertical;
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

.shadow {
  box-shadow: 0px 2px 13px 0px rgba(0, 0, 0, 0.23);
}

.error {
  font-weight: 600;
  color: $error;
}

.info-wrapper {
  padding: 2rem;

  @media (min-width: $tablet) {
    padding: 6rem;
  }

  .close {
    img {
      width: 4rem;
      height: 4rem;
      margin: 0 0 1rem auto;
    }
  }
}

.info {
  padding: 6rem;
  background-color: $surface;

  h2 {
    font-size: 2.5rem;
    margin: 3rem 0 2rem;
  }

  p {
    margin: 2rem 0;
    line-height: 1.5;
  }

  ul.list {
    list-style-type: none;
    padding: 0;

    li {
      margin: 0.5rem 0;
    }
  }
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
  transition: opacity $slow $standard-easing;
}
.fade-slow-enter,
.fade-slow-leave-to {
  opacity: 0;
}

.fade-fast-enter-active,
.fade-fast-leave-active {
  transition: opacity $fast $standard-easing;
}
.fade-fast-enter,
.fade-fast-leave-to {
  opacity: 0;
}

.fade-group-enter-active,
.fade-group-leave-active {
  transition: opacity $fast $standard-easing;
}
.fade-group-enter,
.fade-group-leave-to {
  opacity: 0;
}
.fade-group-enter-active {
  transition-delay: $fast;
}
</style>
