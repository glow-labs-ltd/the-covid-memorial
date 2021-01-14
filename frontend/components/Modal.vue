<template>
  <transition name="fade-slow">
    <div v-if="visible" class="modal__backdrop">
      <div
        ref="modal"
        class="main__content modal"
        role="dialog"
        aria-labelledby="modalTitle"
        aria-describedby="modalDescription"
      >
        <header class="modal__header">
          <slot name="header">Modal header</slot>
          <a
            href="#"
            aria-label="Close modal"
            class="modal__exit"
            @click="$emit('close')"
            ><img src="~/assets/images/close-icon.svg" alt="Close"
          /></a>
        </header>
        <section class="modal__body">
          <slot name="body">Modal Body</slot>
        </section>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'Modal',
  props: {
    visible: {
      type: Boolean,
      default: false,
    },
  },
}
</script>

<style lang="scss" scoped>
.modal {
  display: grid;
  background: $surface;
  box-shadow: 2px 4px 8px 1px rgba($color: #090446, $alpha: 0.25);
  border-radius: 2rem;
  padding: 0;
  margin: auto;

  &__backdrop {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    overflow-y: auto;
    z-index: 1001;
    background-color: rgba(0, 0, 0, 0.3);
  }

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 2rem 0 2rem;

    @media (min-width: $tablet) {
      padding: 3rem 4rem 0 4rem;
    }

    & > * {
      margin: auto 0;
    }

    & > button {
      margin-top: 0;
      margin-left: 1rem;
    }
  }

  &__body {
    padding: 0 2rem 3rem 2rem;

    @media (min-width: $tablet) {
      padding: 0 4rem 3rem 4rem;
    }
  }

  &__exit {
    width: 4rem;
    height: 4rem;
  }
}

.small {
  max-width: 80rem;
}

.generic-modal {
  padding: 4rem 0;

  &__header {
    font-weight: 700;
    margin: 0;
  }

  h1 {
    font-size: 3.4rem;
  }

  &__wrapper {
    margin-top: 2rem;
  }
}

.modal-form__actions {
  display: grid;
  grid-template: auto / 1fr;

  &--inline {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
  }

  a {
    text-align: right;
    display: inline-block;
    padding: 0.2em 0;
    margin: 1rem 0;
    color: $primary;
    font-size: 1.75rem;
  }
}

.modal-form__actions > * {
  justify-self: end;
  margin-top: 2rem;
}

.modal-form__button {
  min-width: 14rem;
  min-height: 6rem;
  padding: 1.5rem;
  margin: 1rem;
}
</style>
