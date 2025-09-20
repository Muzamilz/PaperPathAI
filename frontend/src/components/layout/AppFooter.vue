<template>
  <footer class="bg-gray-900 text-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <!-- Company Info -->
        <div class="col-span-1 lg:col-span-2">
          <div class="mb-4">
            <img 
              src="/src/paperpath_logo.svg" 
              alt="PaperPath Logo" 
              class="h-12 w-auto object-contain"
            />
          </div>
          <p class="text-gray-300 mb-6 max-w-md">
            {{ $t('footer.description', 'Your trusted partner for academic success. We provide comprehensive student services to help you achieve your educational goals.') }}
          </p>
          
          <!-- Social Media Links -->
          <div class="flex space-x-4 rtl:space-x-reverse">
            <a
              v-for="social in socialLinks"
              :key="social.name"
              :href="social.url"
              :aria-label="social.name"
              class="text-gray-400 hover:text-white transition-colors duration-200"
              target="_blank"
              rel="noopener noreferrer"
            >
              <component :is="social.icon" class="w-6 h-6" />
            </a>
          </div>
        </div>

        <!-- Quick Links -->
        <div>
          <h3 class="text-lg font-semibold mb-4">{{ $t('footer.quickLinks', 'Quick Links') }}</h3>
          <ul class="space-y-2">
            <li v-for="link in quickLinks" :key="link.name">
              <router-link
                :to="getLocalizedRoute(link.route)"
                class="text-gray-300 hover:text-white transition-colors duration-200"
              >
                {{ $t(`nav.${link.name}`) }}
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Contact Information -->
        <div>
          <h3 class="text-lg font-semibold mb-4">{{ $t('footer.contactInfo', 'Contact Info') }}</h3>
          <div class="space-y-3">
            <!-- Email -->
            <div class="flex items-center space-x-3 rtl:space-x-reverse">
              <svg class="w-5 h-5 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <a 
                :href="`mailto:${contactInfo.email}`"
                class="text-gray-300 hover:text-white transition-colors duration-200"
              >
                {{ contactInfo.email }}
              </a>
            </div>

            <!-- Phone -->
            <div class="flex items-center space-x-3 rtl:space-x-reverse">
              <svg class="w-5 h-5 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
              <a 
                :href="`tel:${contactInfo.phone}`"
                class="text-gray-300 hover:text-white transition-colors duration-200"
              >
                {{ contactInfo.phone }}
              </a>
            </div>

            <!-- WhatsApp -->
            <div class="flex items-center space-x-3 rtl:space-x-reverse">
              <svg class="w-5 h-5 text-gray-400 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893A11.821 11.821 0 0020.885 3.488"/>
              </svg>
              <a 
                :href="`https://wa.me/${contactInfo.whatsapp}`"
                class="text-gray-300 hover:text-white transition-colors duration-200"
                target="_blank"
                rel="noopener noreferrer"
              >
                {{ contactInfo.whatsapp }}
              </a>
            </div>

            <!-- Address -->
            <div class="flex items-start space-x-3 rtl:space-x-reverse">
              <svg class="w-5 h-5 text-gray-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <span class="text-gray-300">
                {{ $t(`footer.address.${currentLanguage}`, contactInfo.address[currentLanguage]) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom Section -->
      <div class="border-t border-gray-800 mt-8 pt-8">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <p class="text-gray-400 text-sm">
            {{ $t('footer.copyright', '© 2024 Student Services. All rights reserved.') }}
          </p>
          
          <!-- Additional Links -->
          <div class="flex space-x-6 rtl:space-x-reverse mt-4 md:mt-0">
            <a
              v-for="link in legalLinks"
              :key="link.name"
              :href="link.url"
              class="text-gray-400 hover:text-white text-sm transition-colors duration-200"
            >
              {{ $t(`footer.${link.name}`) }}
            </a>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
import { useLanguageStore } from '@/stores/language'

const languageStore = useLanguageStore()

// Computed properties
const currentLanguage = computed(() => languageStore.currentLanguage)

// Navigation data
const quickLinks = [
  { name: 'home', route: 'home' },
  { name: 'services', route: 'services' },
  { name: 'portfolio', route: 'portfolio' },
  { name: 'contact', route: 'contact' }
]

const socialLinks = [
  {
    name: 'Facebook',
    url: 'https://facebook.com/studentservices',
    icon: 'FacebookIcon'
  },
  {
    name: 'Twitter',
    url: 'https://twitter.com/studentservices',
    icon: 'TwitterIcon'
  },
  {
    name: 'LinkedIn',
    url: 'https://linkedin.com/company/studentservices',
    icon: 'LinkedInIcon'
  },
  {
    name: 'Instagram',
    url: 'https://instagram.com/studentservices',
    icon: 'InstagramIcon'
  }
]

const legalLinks = [
  { name: 'privacy', url: '/privacy' },
  { name: 'terms', url: '/terms' },
  { name: 'cookies', url: '/cookies' }
]

// Contact information
const contactInfo = {
  email: 'info@studentservices.com',
  phone: '+1 (555) 123-4567',
  whatsapp: '15551234567',
  address: {
    en: '123 Academic Street, Education City, EC 12345',
    ar: '123 شارع الأكاديمية، مدينة التعليم، EC 12345'
  }
}

// Methods
const getLocalizedRoute = (routeName, params = {}) => {
  return languageStore.getLocalizedRoute(routeName, params)
}
</script>

<!-- Social Media Icon Components -->
<script>
// Simple icon components for social media
const FacebookIcon = {
  template: `
    <svg fill="currentColor" viewBox="0 0 24 24">
      <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
    </svg>
  `
}

const TwitterIcon = {
  template: `
    <svg fill="currentColor" viewBox="0 0 24 24">
      <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
    </svg>
  `
}

const LinkedInIcon = {
  template: `
    <svg fill="currentColor" viewBox="0 0 24 24">
      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
    </svg>
  `
}

const InstagramIcon = {
  template: `
    <svg fill="currentColor" viewBox="0 0 24 24">
      <path d="M12.017 0C8.396 0 7.989.016 6.756.072 5.526.127 4.718.302 4.019.57a5.962 5.962 0 00-2.153 1.4A5.962 5.962 0 00.434 4.019C.166 4.718-.009 5.526-.064 6.756-.12 7.989-.136 8.396-.136 12.017c0 3.621.016 4.028.072 5.261.055 1.23.23 2.038.498 2.737a5.962 5.962 0 001.4 2.153 5.962 5.962 0 002.153 1.4c.699.268 1.507.443 2.737.498 1.233.056 1.64.072 5.261.072 3.621 0 4.028-.016 5.261-.072 1.23-.055 2.038-.23 2.737-.498a5.962 5.962 0 002.153-1.4 5.962 5.962 0 001.4-2.153c.268-.699.443-1.507.498-2.737.056-1.233.072-1.64.072-5.261 0-3.621-.016-4.028-.072-5.261-.055-1.23-.23-2.038-.498-2.737a5.962 5.962 0 00-1.4-2.153A5.962 5.962 0 0019.778.57C19.079.302 18.271.127 17.041.072 15.808.016 15.401 0 11.78 0h.237zm-.117 2.178c3.556 0 3.97.016 5.37.072 1.295.059 1.998.271 2.466.45.62.24 1.062.528 1.527.992.464.465.752.907.992 1.527.179.468.391 1.171.45 2.466.056 1.4.072 1.814.072 5.37 0 3.556-.016 3.97-.072 5.37-.059 1.295-.271 1.998-.45 2.466-.24.62-.528 1.062-.992 1.527-.465.464-.907.752-1.527.992-.468.179-1.171.391-2.466.45-1.4.056-1.814.072-5.37.072-3.556 0-3.97-.016-5.37-.072-1.295-.059-1.998-.271-2.466-.45-.62-.24-1.062-.528-1.527-.992-.464-.465-.752-.907-.992-1.527-.179-.468-.391-1.171-.45-2.466-.056-1.4-.072-1.814-.072-5.37 0-3.556.016-3.97.072-5.37.059-1.295.271-1.998.45-2.466.24-.62.528-1.062.992-1.527.465-.464.907-.752 1.527-.992.468-.179 1.171-.391 2.466-.45 1.4-.056 1.814-.072 5.37-.072z"/>
      <path d="M12.017 5.838a6.179 6.179 0 100 12.358 6.179 6.179 0 000-12.358zm0 10.18a4.001 4.001 0 110-8.003 4.001 4.001 0 010 8.003zm7.846-10.405a1.441 1.441 0 11-2.883 0 1.441 1.441 0 012.883 0z"/>
    </svg>
  `
}

export default {
  components: {
    FacebookIcon,
    TwitterIcon,
    LinkedInIcon,
    InstagramIcon
  }
}
</script>

<style scoped>
/* Additional styles for RTL support */
.rtl .space-x-2 > :not([hidden]) ~ :not([hidden]) {
  --tw-space-x-reverse: 1;
}

.rtl .space-x-3 > :not([hidden]) ~ :not([hidden]) {
  --tw-space-x-reverse: 1;
}

.rtl .space-x-4 > :not([hidden]) ~ :not([hidden]) {
  --tw-space-x-reverse: 1;
}

.rtl .space-x-6 > :not([hidden]) ~ :not([hidden]) {
  --tw-space-x-reverse: 1;
}
</style>