<template>
  <div>
    <Modal :visible="$store.state.addModal" @close="close">
      <h2 id="modalTitle" slot="header" class="generic-modal__header">
        Add memorial
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
              <input
                v-model="birth_date"
                type="date"
                name="birth_date"
                placeholder="yyyy-mm-dd"
                :max="maxDate"
              />
            </div>

            <div>
              <label for="death_date">Date of death</label>
              <input
                v-model="death_date"
                type="date"
                name="death_date"
                placeholder="yyyy-mm-dd"
                :max="maxDate"
              />
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
            <label for="country">Country <span class="required">*</span></label>
            <v-select
              v-model="country"
              :options="countries"
              class="country-select"
            >
              <template #search="{ attributes, events }">
                <input
                  class="vs__search"
                  :required="!country"
                  v-bind="attributes"
                  v-on="events"
                />
              </template>
            </v-select>
          </div>

          <div class="row">
            <label for="city">Town / City</label>
            <input v-model="city" type="text" name="city" />
          </div>

          <div class="row">
            <label for="occupation">Occupation</label>
            <input v-model="occupation" type="text" name="occupation" />
          </div>

          <div class="row">
            <label for="message"
              >Tell their story <span class="required">*</span></label
            >
            <textarea
              v-model="message"
              type="text"
              name="message"
              rows="6"
              maxlength="2500"
              required
            />
            <p class="note">{{ messageLength }} / 2500 character limit</p>
          </div>

          <div class="row">
            <div class="ticks">
              <input
                id="amend"
                v-model="amend"
                type="checkbox"
                name="amend"
                value="amend"
                required
              />
              <label for="amend"
                >I understand I am not able to amend my memorial once it has
                been submitted.</label
              >
              <input
                id="terms"
                v-model="terms"
                type="checkbox"
                name="terms"
                value="terms"
                required
              />
              <label for="terms"
                >I have read and agreed to the
                <a href="/terms" target="_blank">terms of service</a>
                (opens in new window).</label
              >
              <input
                id="privacy"
                v-model="privacy"
                type="checkbox"
                name="privacy"
                value="privacy"
                required
              />
              <label for="privacy"
                >I have read and agreed to the
                <a href="/terms#privacy" target="_blank">privacy notice</a>
                (opens in new window).</label
              >
            </div>
          </div>

          <div class="row">
            <p class="submit-disclaimer">
              Please be aware that it may take up to 24 hours for your
              submission to appear in search results.
            </p>
            <input
              type="submit"
              :value="submitText"
              :disabled="loading"
              class="submit"
            />
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
      occupation: null,
      message: null,
      amend: false,
      terms: false,
      privacy: false,
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
      countries: Object.entries(countryList.getNames('en')).map(
        ([key, value]) => ({ value: key, label: value })
      ),
      loading: false,
    }
  },
  computed: {
    selectedColourClass() {
      if (this.colour) {
        return `colour--${this.colour.value}`
      }
      return null
    },
    maxDate() {
      const now = new Date()
      return now.toISOString().split('T')[0]
    },
    messageLength() {
      return this.message?.length || 0
    },
    submitText() {
      return !this.loading ? 'Submit' : 'Loading...'
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
        occupation: this.occupation,
        message: this.message,
      }

      const formData = new FormData()
      for (const key in data) {
        if (data[key]) formData.append(key, data[key])
      }

      const croppedImage = await this.$refs.imageUpload.getCroppedImage()
      if (croppedImage)
        formData.append('image', croppedImage.blob, croppedImage.fileName)

      this.loading = true
      const response = await this.$store.dispatch('postDeceased', formData)
      if (response) {
        this.$store.commit('setAddModal', false)
        this.$router.push({
          name: 'memoriam-slug-code',
          params: { slug: response.slug, code: response.code },
        })
      }
      this.loading = false
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
  border-radius: 1rem;

  ::v-deep {
    .vs__selected {
      color: $surface;
    }
  }
}

.colour-select,
.country-select {
  ::v-deep {
    .vs__selected {
      font-weight: 600;
    }

    .vs__open-indicator,
    .vs__clear {
      fill: $secondary;
    }

    .vs__dropdown-toggle {
      border: 2px solid $primary;
      border-radius: 1rem;
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
  grid-template: auto / auto auto;
  grid-gap: 1rem;

  input {
    margin: auto;
  }

  label {
    font-size: 1.5rem;
    font-weight: 400;
    text-align: left;
    margin: auto 0;
    cursor: pointer;
  }
}

.submit {
  background-color: $secondary;
  color: $surface;
  font-size: 2.5rem;
  font-weight: 600;
  cursor: pointer;

  &-disclaimer {
    margin-bottom: 2rem;
    font-weight: 700;
  }
}

.error {
  color: red;
}
</style>
