<template>
  <div>
    <Modal :visible="$store.state.addModal" @close="close">
      <h2 id="modalTitle" slot="header" class="generic-modal__header">
        Add memoriam
      </h2>
      <div slot="body" class="generic-modal__wrapper">
        <hr />
        <form id="add" @submit.prevent="submit">
          <div class="row image-section">
            <ImageUpload ref="imageUpload" />
          </div>

          <div class="row">
            <label for="name">Their name <span class="required">*</span></label>
            <input v-model="name" type="text" name="name" required />
          </div>

          <div class="row dates">
            <div>
              <label for="birth_date">Date of birth</label>
              <input v-model="birth_date" type="date" name="birth_date" />
            </div>

            <div>
              <label for="death_date">Date of death</label>
              <input v-model="death_date" type="date" name="death_date" />
            </div>

            <div>
              <label for="age">Age</label>
              <input v-model="age" type="number" name="age" min="0" max="140" />
            </div>
          </div>

          <div class="row">
            <label for="colour">Choose a colour</label>
            <v-select
              v-model="colour"
              :options="colours"
              :searchable="false"
              class="colour-select"
              :class="selectedColourClass"
            >
              <template slot="option" slot-scope="option">
                <div :class="`colour colour--${option.value}`">&nbsp;</div>
              </template>
            </v-select>
          </div>

          <div class="row">
            <label for="country">Country</label>
            <v-select v-model="country" :options="countries" />
          </div>

          <div class="row">
            <label for="city">Town / City</label>
            <input v-model="city" type="text" name="city" />
          </div>

          <div class="row">
            <label for="message">Your message</label>
            <textarea
              v-model="message"
              type="text"
              name="message"
              rows="6"
              maxlength="2500"
            />
          </div>

          <div class="row">
            <div class="ticks">
              <div>
                <input
                  id="amend"
                  v-model="amend"
                  type="checkbox"
                  name="amend"
                  value="amend"
                  required
                />
                <label for="amend"
                  >I understand I am not able to amend my memorium once it has
                  been submitted.</label
                >
              </div>
              <div>
                <input
                  id="terms"
                  v-model="terms"
                  type="checkbox"
                  name="terms"
                  value="terms"
                  required
                />
                <label for="terms">I have read and understood the terms.</label>
              </div>
            </div>
          </div>

          <div class="row">
            <input type="submit" value="Submit" class="submit" />
          </div>
        </form>

        <div v-if="$store.state.error" class="error">
          {{ $store.state.error }}
        </div>
      </div>
    </Modal>
  </div>
</template>

<script>
const countryList = require('i18n-iso-countries')
countryList.registerLocale(require('i18n-iso-countries/langs/en.json'))

export default {
  data() {
    return {
      name: null,
      birth_date: null,
      death_date: null,
      age: null,
      colour: null,
      country: null,
      city: null,
      message: null,
      amend: false,
      terms: false,
      colours: [
        { value: 0, label: 'Red' },
        { value: 1, label: 'Orange' },
        { value: 2, label: 'Yellow' },
        { value: 3, label: 'Green' },
        { value: 4, label: 'Blue' },
        { value: 5, label: 'Purple' },
        { value: 6, label: 'Pink' },
        { value: 7, label: 'Black' },
      ],
      countries: Object.entries(
        countryList.getNames('en')
      ).map(([key, value]) => ({ value: key, label: value })),
    }
  },
  computed: {
    selectedColourClass() {
      if (this.colour) {
        return `colour--${this.colour.value}`
      }
      return null
    },
  },
  methods: {
    close() {
      this.$store.commit('setAddModal', false)
    },
    async submit() {
      const data = {
        name: this.name,
        birth_date: this.birth_date,
        death_date: this.death_date,
        age: this.age,
        colour: this.colour?.value,
        country: this.country?.value,
        city: this.city,
        message: this.message,
      }

      const formData = new FormData()
      for (const key in data) {
        if (data[key]) formData.append(key, data[key])
      }

      const croppedImage = await this.$refs.imageUpload.getCroppedImage()
      if (croppedImage)
        formData.append('image', croppedImage.blob, croppedImage.fileName)

      const response = await this.$store.dispatch('postDeceased', formData)
      if (response) {
        this.$store.commit('setAddModal', false)
        this.$router.push({
          name: 'memoriam-slug-code',
          params: { slug: response.slug, code: response.code },
        })
      }
    },
  },
}
</script>

<style lang="scss" scoped>
hr {
  margin: 2rem 0;
}

label {
  text-align: left;
  display: block;

  .required {
    color: #cc2d2d;
    font-weight: 400;
  }
}

.row {
  margin-bottom: 2rem;
}

.dates {
  display: grid;
  grid-template: auto / auto;
  grid-gap: 2rem;

  @media (min-width: $tablet) {
    grid-template: auto / repeat(3, auto);
    grid-gap: 1rem 2rem;
  }
}

.colour-select {
  width: 20rem;

  ::v-deep {
    .vs__selected {
      color: $surface;
      font-weight: 600;
    }

    .vs__open-indicator,
    .vs__clear {
      fill: $secondary;
    }
  }
}

.colour {
  color: $surface;
  font-weight: 600;
  text-align: center;
  padding: 1em;
}

.ticks {
  display: grid;
  grid-template: auto auto / auto;

  > * {
    justify-self: left;
  }

  label {
    display: inline;
    font-size: 1.5rem;
    font-weight: 400;
    margin-left: 1rem;
    text-align: left;
    vertical-align: middle;
  }
}

.submit {
  background-color: $secondary;
  color: $surface;
  font-size: 2.5rem;
  font-weight: 600;
}

.error {
  color: red;
}
</style>
