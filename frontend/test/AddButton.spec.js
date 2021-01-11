import { shallowMount, RouterLinkStub } from '@vue/test-utils'
import AddButton from '@/components/AddButton.vue'

describe('AddButton', () => {
  test('is a Vue instance', () => {
    const wrapper = shallowMount(AddButton, {
      stubs: {
        NuxtLink: RouterLinkStub,
      },
    })
    expect(wrapper.vm).toBeTruthy()
  })
})
