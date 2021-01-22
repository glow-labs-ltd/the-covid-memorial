<template>
  <div class="container scroll">
    <div class="info-wrapper limit-width">
      <div class="close">
        <a href="" @click.prevent="$router.push('/')"
          ><img src="~/assets/images/close-icon.svg" alt="Close"
        /></a>
      </div>
      <div class="info shadow">
        <h1>Donate</h1>
        <p>
          The COVID Memorial is a not-for-profit project. Please help us to keep
          this memorial alive by donating today.
        </p>
        <form
          action="https://www.paypal.com/donate"
          method="post"
          target="_top"
        >
          <input type="hidden" name="hosted_button_id" value="LL2JDNDNYC8BA" />
          <input
            type="image"
            :src="require('~/assets/images/donation-button.svg')"
            border="0"
            name="submit"
            title="Make a donation with PayPal"
            alt="Make a donation with PayPal button"
          />
          <img
            alt=""
            border="0"
            src="https://www.paypal.com/en_GB/i/scr/pixel.gif"
            width="1"
            height="1"
          />
        </form>
        <p>
          All donations will be spent on the running of the memorial, and we
          will donate any excess amounts to
          <a href="https://msf.org.uk/" target="_blank"
            >Médecins Sans Frontières' (Doctors Without Borders)</a
          >
          COVID emergency appeal.
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

<style lang="scss" scoped>
form {
  text-align: center;
}

input {
  border: none;
  border-radius: 0;
  padding: 0;
  width: 206px;
  height: 67px;
}
</style>
