import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createI18n } from 'vue-i18n'
import { createRouter, createWebHistory } from 'vue-router'
import App from '../App.vue'

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  messages: {
    en: { welcome: 'Welcome' },
    ar: { welcome: 'مرحبا' }
  }
})

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } }
  ]
})

describe('App', () => {
  it('renders properly', () => {
    const wrapper = mount(App, {
      global: {
        plugins: [i18n, router]
      }
    })
    expect(wrapper.find('#app').exists()).toBe(true)
  })

  it('sets RTL direction for Arabic', async () => {
    const wrapper = mount(App, {
      global: {
        plugins: [i18n, router]
      }
    })
    
    // Change to Arabic
    i18n.global.locale.value = 'ar'
    await wrapper.vm.$nextTick()
    
    expect(wrapper.find('#app').attributes('dir')).toBe('rtl')
    expect(wrapper.find('#app').classes()).toContain('rtl')
  })
})