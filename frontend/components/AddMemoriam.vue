<template>
  <div>
    <Modal :visible="$store.state.addModal" @close="close">
      <h2 id="modalTitle" slot="header" class="generic-modal__header">
        Add memoriam
      </h2>
      <div slot="body" class="generic-modal__wrapper">
        <form id="add">
          <div class="row">
            <label for="name">Their name</label>
            <input type="text" name="name" />
          </div>

          <div class="row dates">
            <div>
              <label for="birth_date">Date of birth</label>
              <input type="date" name="birth_date" />
            </div>

            <div>
              <label for="death_date">Date of death</label>
              <input type="date" name="death_date" />
            </div>

            <div>
              <label for="age">Age</label>
              <input type="number" name="age" />
            </div>
          </div>

          <input
            type="submit"
            value="Submit"
            class="submit"
            @click.prevent="submit"
          />
        </form>
      </div>
    </Modal>
  </div>
</template>

<script>
export default {
  methods: {
    close() {
      this.$store.commit('setAddModal', false)
    },
    submit() {
      //   console.log('submit')
    },
  },
}
</script>

<style lang="scss" scoped>
label {
  text-align: left;
  display: block;
}

input {
  width: 100%;
}

.row {
  margin-bottom: 2rem;
}

.dates {
  display: grid;
  grid-template: auto / repeat(3, auto);
  grid-gap: 1rem;
}

.submit {
  background-color: $secondary;
  color: $surface;
}
</style>
