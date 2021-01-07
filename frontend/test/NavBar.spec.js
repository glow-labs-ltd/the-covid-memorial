import { shallowMount, RouterLinkStub } from '@vue/test-utils'
import NavBar from '@/components/NavBar.vue'

describe('NavBar', () => {
  test('is a Vue instance', () => {
    const wrapper = shallowMount(NavBar, {
      stubs: {
        NuxtLink: RouterLinkStub,
      },
    })
    expect(wrapper.vm).toBeTruthy()
  })
})
