<template>
  <div class="card-elevated p-8 animate-fade-in-up">
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ $t('contact.sendMessage') }}</h2>
      <p class="text-gray-600">{{ $t('contact.description') }}</p>
    </div>
    
    <form @submit.prevent="handleSubmit" class="space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Name -->
        <div class="form-group animate-fade-in-up animate-stagger-1">
          <label class="form-label">{{ $t('contact.name') }} *</label>
          <input
            v-model="form.name"
            type="text"
            :placeholder="$t('contact.namePlaceholder')"
            class="form-input"
            :class="{ 'error': errors.name }"
            required
          />
          <div v-if="errors.name" class="form-error">{{ errors.name }}</div>
        </div>
        
        <!-- Email -->
        <div class="form-group animate-fade-in-up animate-stagger-2">
          <label class="form-label">{{ $t('contact.email') }} *</label>
          <input
            v-model="form.email"
            type="email"
            :placeholder="$t('contact.emailPlaceholder')"
            class="form-input"
            :class="{ 'error': errors.email }"
            required
          />
          <div v-if="errors.email" class="form-error">{{ errors.email }}</div>
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Phone -->
        <div class="form-group animate-fade-in-up animate-stagger-3">
          <label class="form-label">{{ $t('contact.phone') }}</label>
          <input
            v-model="form.phone"
            type="tel"
            :placeholder="$t('contact.phonePlaceholder')"
            class="form-input"
            :class="{ 'error': errors.phone }"
          />
          <div v-if="errors.phone" class="form-error">{{ errors.phone }}</div>
        </div>
        
        <!-- Preferred Contact Method -->
        <div class="form-group animate-fade-in-up animate-stagger-4">
          <label class="form-label">{{ $t('contact.preferredContact') }}</label>
          <select
            v-model="form.preferredContact"
            class="form-input"
          >
            <option value="email">{{ $t('contact.email') }}</option>
            <option value="phone">{{ $t('contact.phone') }}</option>
            <option value="either">{{ $t('contact.either') }}</option>
          </select>
        </div>
      </div>
      
      <!-- Subject -->
      <div class="form-group animate-fade-in-up animate-stagger-5">
        <label class="form-label">{{ $t('contact.subject') }} *</label>
        <input
          v-model="form.subject"
          type="text"
          :placeholder="$t('contact.subjectPlaceholder')"
          class="form-input"
          :class="{ 'error': errors.subject }"
          required
        />
        <div v-if="errors.subject" class="form-error">{{ errors.subject }}</div>
      </div>
      
      <!-- Message -->
      <div class="form-group animate-fade-in-up animate-stagger-6">
        <label class="form-label">{{ $t('contact.message') }} *</label>
        <textarea
          v-model="form.message"
          rows="5"
          :placeholder="$t('contact.messagePlaceholder')"
          class="form-input resize-none"
          :class="{ 'error': errors.message }"
          required
        ></textarea>
        <div v-if="errors.message" class="form-error">{{ errors.message }}</div>
        <div class="text-sm text-gray-500 mt-1">
          {{ form.message.length }}/500 {{ $t('common.characters') }}
        </div>
      </div>
      
      <!-- Submit Button -->
      <div class="text-center animate-fade-in-up animate-stagger-7">
        <button
          type="submit"
          :disabled="isSubmitting"
          class="btn-primary touch-feedback w-full md:w-auto"
          :class="{ 'btn-loading': isSubmitting }"
        >
          <span v-if="!isSubmitting" class="flex items-center justify-center">
            {{ $t('contact.send') }}
            <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </span>
          <span v-else class="flex items-center justify-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ $t('common.submitting') }}
          </span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// Form state
const form = reactive({
  name: '',
  email: '',
  phone: '',
  subject: '',
  message: '',
  preferredContact: 'email'
})

const errors = reactive({})
const isSubmitting = ref(false)

// Validation
const validateForm = () => {
  // Clear previous errors
  Object.keys(errors).forEach(key => delete errors[key])
  
  let isValid = true
  
  if (!form.name.trim()) {
    errors.name = t('common.required')
    isValid = false
  }
  
  if (!form.email.trim()) {
    errors.email = t('common.required')
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = t('common.invalidEmail')
    isValid = false
  }
  
  if (form.phone && !/^[\+]?[1-9][\d]{0,15}$/.test(form.phone.replace(/\s/g, ''))) {
    errors.phone = t('common.invalidPhone')
    isValid = false
  }
  
  if (!form.subject.trim()) {
    errors.subject = t('common.required')
    isValid = false
  }
  
  if (!form.message.trim()) {
    errors.message = t('common.required')
    isValid = false
  } else if (form.message.trim().length < 10) {
    errors.message = t('contact.messageMinLength')
    isValid = false
  } else if (form.message.length > 500) {
    errors.message = t('contact.messageMaxLength')
    isValid = false
  }
  
  return isValid
}

// Form submission
const handleSubmit = async () => {
  if (!validateForm()) {
    // Show validation error notification
    if (window.$notify) {
      window.$notify.error(t('contact.validationError'), t('contact.fixErrors'))
    }
    return
  }
  
  isSubmitting.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Show success notification
    if (window.$notify) {
      window.$notify.success(t('contact.success'), t('contact.successMessage'))
    }
    
    // Reset form
    Object.keys(form).forEach(key => {
      if (key === 'preferredContact') {
        form[key] = 'email'
      } else {
        form[key] = ''
      }
    })
    
  } catch (error) {
    console.error('Failed to send message:', error)
    
    // Show error notification
    if (window.$notify) {
      window.$notify.error(t('contact.error'), t('contact.errorMessage'))
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>