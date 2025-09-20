<template>
  <div class="contact-info bg-white rounded-lg shadow-lg p-6">
    <h3 class="text-xl font-semibold mb-6">{{ $t('contact.getInTouch') }}</h3>
    
    <div class="space-y-6">
      <!-- Address -->
      <div class="flex items-start">
        <div class="flex-shrink-0">
          <svg class="w-6 h-6 text-blue-600 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>
        <div class="ml-4 rtl:ml-0 rtl:mr-4">
          <h4 class="text-lg font-medium text-gray-900">{{ $t('contact.address') }}</h4>
          <p class="mt-1 text-gray-600">
            {{ $t('footer.address.' + $i18n.locale) }}
          </p>
        </div>
      </div>

      <!-- Phone -->
      <div class="flex items-start">
        <div class="flex-shrink-0">
          <svg class="w-6 h-6 text-blue-600 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
          </svg>
        </div>
        <div class="ml-4 rtl:ml-0 rtl:mr-4">
          <h4 class="text-lg font-medium text-gray-900">{{ $t('contact.phone') }}</h4>
          <div class="mt-1 space-y-1">
            <p class="text-gray-600">
              <a href="tel:+1234567890" class="hover:text-blue-600 transition-colors">
                +1 (234) 567-8900
              </a>
            </p>
            <p class="text-gray-600">
              <a href="tel:+1234567891" class="hover:text-blue-600 transition-colors">
                +1 (234) 567-8901
              </a>
            </p>
          </div>
        </div>
      </div>

      <!-- Email -->
      <div class="flex items-start">
        <div class="flex-shrink-0">
          <svg class="w-6 h-6 text-blue-600 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        </div>
        <div class="ml-4 rtl:ml-0 rtl:mr-4">
          <h4 class="text-lg font-medium text-gray-900">{{ $t('contact.email') }}</h4>
          <div class="mt-1 space-y-1">
            <p class="text-gray-600">
              <a href="mailto:info@studentservices.com" class="hover:text-blue-600 transition-colors">
                info@studentservices.com
              </a>
            </p>
            <p class="text-gray-600">
              <a href="mailto:support@studentservices.com" class="hover:text-blue-600 transition-colors">
                support@studentservices.com
              </a>
            </p>
          </div>
        </div>
      </div>

      <!-- Business Hours -->
      <div class="flex items-start">
        <div class="flex-shrink-0">
          <svg class="w-6 h-6 text-blue-600 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div class="ml-4 rtl:ml-0 rtl:mr-4">
          <h4 class="text-lg font-medium text-gray-900">{{ $t('contact.businessHours') }}</h4>
          <div class="mt-1 space-y-1 text-gray-600">
            <p>{{ $t('contact.weekdays') }}: 9:00 AM - 6:00 PM</p>
            <p>{{ $t('contact.saturday') }}: 10:00 AM - 4:00 PM</p>
            <p>{{ $t('contact.sunday') }}: {{ $t('contact.closed') }}</p>
          </div>
        </div>
      </div>

      <!-- Social Media -->
      <div class="flex items-start">
        <div class="flex-shrink-0">
          <svg class="w-6 h-6 text-blue-600 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2m-9 0h10m-9 0a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V6a2 2 0 00-2-2m-9 0V4" />
          </svg>
        </div>
        <div class="ml-4 rtl:ml-0 rtl:mr-4">
          <h4 class="text-lg font-medium text-gray-900">{{ $t('contact.followUs') }}</h4>
          <div class="mt-2 flex space-x-4 rtl:space-x-reverse">
            <!-- Facebook -->
            <a href="#" class="text-gray-400 hover:text-blue-600 transition-colors">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
              </svg>
            </a>
            <!-- Twitter -->
            <a href="#" class="text-gray-400 hover:text-blue-400 transition-colors">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
              </svg>
            </a>
            <!-- LinkedIn -->
            <a href="#" class="text-gray-400 hover:text-blue-700 transition-colors">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
              </svg>
            </a>
            <!-- Instagram -->
            <a href="#" class="text-gray-400 hover:text-pink-600 transition-colors">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 6.62 5.367 11.987 11.988 11.987 6.62 0 11.987-5.367 11.987-11.987C24.014 5.367 18.637.001 12.017.001zM8.449 16.988c-1.297 0-2.448-.49-3.323-1.297C4.198 14.895 3.708 13.744 3.708 12.447s.49-2.448 1.297-3.323C5.902 8.198 7.053 7.708 8.35 7.708s2.448.49 3.323 1.297c.897.875 1.387 2.026 1.387 3.323s-.49 2.448-1.297 3.323c-.875.897-2.026 1.387-3.323 1.387zm7.718 0c-1.297 0-2.448-.49-3.323-1.297-.897-.875-1.387-2.026-1.387-3.323s.49-2.448 1.297-3.323c.875-.897 2.026-1.387 3.323-1.387s2.448.49 3.323 1.297c.897.875 1.387 2.026 1.387 3.323s-.49 2.448-1.297 3.323c-.875.897-2.026 1.387-3.323 1.387z"/>
              </svg>
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Emergency Contact -->
    <div class="mt-8 p-4 bg-red-50 border border-red-200 rounded-lg">
      <div class="flex">
        <svg class="w-5 h-5 text-red-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L4.35 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
        <div class="ml-3 rtl:ml-0 rtl:mr-3">
          <h4 class="text-sm font-medium text-red-800">{{ $t('contact.urgentInquiries') }}</h4>
          <p class="mt-1 text-sm text-red-700">
            {{ $t('contact.urgentInquiriesText') }}
            <a href="tel:+1234567999" class="font-medium underline hover:text-red-900">
              +1 (234) 567-9999
            </a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Contact information component
</script>

<style scoped>
/* Custom styles for contact info */
a {
  transition: color 0.2s ease-in-out;
}
</style>