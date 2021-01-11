<template>
  <div class="container">
    <div class="memoriam">
      <div class="left">
        <img class="portrait" src="~/assets/images/placeholder.jpg" />
        <div class="details">
          <h1 class="name">{{ name }}</h1>
          <h2 class="city">{{ city }}</h2>
          <p class="age"></p>
        </div>
      </div>
      <div class="right">
        <div class="close">
          <button @click="close">Close</button>
        </div>
        <div>
          <p class="message">"{{ message }}"</p>
          <div class="comment-section">
            <h3>Add a comment</h3>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  async fetch() {
    const response = await this.$axios.get(
      `deceased/${this.$route.params.slug}/`
    )
    this.memoriam = response.data
  },
  data() {
    return {
      memoriam: null,
    }
  },
  computed: {
    name() {
      return this.memoriam?.name
    },
    city() {
      return this.memoriam?.city
    },
    message() {
      // return this.memoriam?.message
      return 'Lorem ipsum dolor sit amet, consectetur adipiscing elit,\n\n   sed do eiusmod tempor incididunt ut labore\n\n et dolore magna aliqua. Bibendum arcu vitae elementum curabitur. Scelerisque felis imperdiet proin fermentum leo vel. Massa id neque aliquam vestibulum morbi. At consectetur lorem donec massa sapien faucibus et. Nibh tortor id aliquet lectus proin nibh. Eget duis at tellus at urna condimentum mattis. Morbi non arcu risus quis varius quam quisque id. Arcu cursus vitae congue mauris rhoncus. Blandit libero volutpat sed cras ornare. Orci phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Fermentum leo vel orci porta non pulvinar neque. Auctor urna nunc id cursus metus aliquam eleifend mi. Massa sapien faucibus et molestie. Sed ullamcorper morbi tincidunt ornare massa eget. Quisque non tellus orci ac auctor augue mauris. Nunc faucibus a pellentesque sit. Dolor magna eget est lorem ipsum dolor sit amet consectetur. Dignissim enim sit amet venenatis. Elit scelerisque mauris pellentesque pulvinar pellentesque habitant morbi tristique. Purus semper eget duis at tellus at urna condimentum mattis. Eget nunc scelerisque viverra mauris in aliquam sem fringilla. Vitae proin sagittis nisl rhoncus. Ipsum faucibus vitae aliquet nec ullamcorper sit amet. Egestas congue quisque egestas diam. Ac auctor augue mauris augue neque gravida in fermentum et. Ut tellus elementum sagittis vitae et leo duis ut. Libero enim sed faucibus turpis. Mi eget mauris pharetra et ultrices neque ornare.\n\n Pretium lectus quam id leo in. Cras semper auctor neque vitae tempus quam pellentesque nec.\n\n Suspendisse ultrices gravida dictum fusce ut.'
    },
  },
  transition: {
    name: 'fade-slow',
    mode: '',
  },
  methods: {
    close() {
      this.$router.push('/')
    },
  },
}
</script>

<style lang="scss" scoped>
.memoriam {
  display: grid;
  grid-template: auto / 1fr;
  height: 100%;
  width: 100%;
  text-align: left;
  max-width: 100rem;
  max-height: 85%;
  margin: 4rem auto 0;
  background-color: $surface;
  overflow-y: scroll;

  @media (min-width: $tablet) {
    grid-template: 75vh / repeat(2, 1fr);
    max-height: 75vh;
    margin: 8rem auto 0;
    overflow-y: hidden;
  }

  @media (min-width: $desktop) {
    margin: 12rem auto 0;
  }

  .portrait {
    object-fit: cover;
    width: 100%;
    max-height: 50rem;
  }

  .details {
    margin: 2rem;
  }

  .name {
    font-size: 2.25rem;
  }

  .age,
  .city {
    font-size: 1.5rem;
  }

  .left {
    max-height: 100%;
  }

  .right {
    display: grid;
    grid-template: auto 1fr / auto;
    padding: 2rem;
    max-height: 100%;

    @media (min-width: $tablet) {
      overflow-y: scroll;
    }
  }

  .message {
    margin: 2rem 1rem 2rem 0;
    text-align: justify;
    text-justify: inter-word;
    white-space: pre-line;
  }

  .close {
    text-align: right;
  }

  .comment-section {
    height: 20rem;
  }
}
</style>
