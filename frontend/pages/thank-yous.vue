<template>
  <div class="container scroll">
    <div class="info-wrapper limit-width">
      <div class="close">
        <a href="" @click.prevent="$router.push('/')"
          ><img src="~/assets/images/close-icon.svg" alt="Close"
        /></a>
      </div>
      <div class="info shadow">
        <h1>Thank You's</h1>
        <p>
          We want to thank the following people who have dedicated their free
          time to help bring this memorial to life.
        </p>
        <h2>For creating The COVID Memorial</h2>
        <ul class="list">
          <li>
            The
            <a href="https://findothers.com/" target="_blank">Find Others</a>
            team:
          </li>
          <li>Amar Chauhan</li>
          <li>Georgina Hollis</li>
          <li>Anthony Faconti</li>
          <li>Kamal Daniels</li>
          <li>Sam Carty</li>
        </ul>

        <h2>For publicising The COVID Memorial</h2>
        <ul class="list">
          <li>
            <a
              href="https://www.shapehistory.com/"
              target="_blank"
              rel="noopener noreferrer"
              >Shape History</a
            >
          </li>
        </ul>

        <h2>For providing legal advice to The COVID Memorial</h2>
        <ul class="list">
          <li>
            <a
              href="https://www.freeths.co.uk/"
              target="_blank"
              rel="noopener noreferrer"
              >Freeths LLP</a
            >
          </li>
          <li>Will Richmond-Coggan</li>
        </ul>

        <h2>And thank you to all of our kind donors.</h2>
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
