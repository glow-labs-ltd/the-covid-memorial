<template>
  <div class="container scroll">
    <div class="info-wrapper limit-width">
      <div class="close">
        <a href="" @click.prevent="$router.push('/')"
          ><img src="~/assets/images/close-icon.svg" alt="Close"
        /></a>
      </div>
      <div class="info shadow">
        <h1>About The COVID Memorial</h1>
        <p>
          COVID-19 touched every corner of our world, with devastating
          consequences to human life. These tragic deaths should not be
          portrayed simply as a number.
        </p>
        <p>
          The COVID Memorial is a place to put a face and story to every number,
          and to commemorate all those who have sadly lost their lives due to
          the pandemic, either directly or indirectly.
        </p>
        <p>
          If you have lost a loved one, please share their story as part of this
          global memorial and ensure future generations remember the people and
          not just the numbers.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  transition: {
    name: 'fade-slow',
    mode: '',
  },
}
</script>

<style lang="scss" scoped></style>
