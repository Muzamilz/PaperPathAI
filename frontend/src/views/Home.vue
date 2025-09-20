<template>
  <div class="min-h-screen bg-white">
    <!-- Hero Section -->
    <div class="relative bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 overflow-hidden">
      <!-- Background Pattern -->
      <div class="absolute inset-0 bg-black bg-opacity-10"></div>
      <div class="absolute inset-0 bg-gradient-to-r from-blue-600/20 to-transparent"></div>
      
      <!-- Floating Elements -->
      <div class="absolute top-20 left-10 w-20 h-20 bg-white bg-opacity-10 rounded-full blur-xl animate-pulse"></div>
      <div class="absolute top-40 right-20 w-32 h-32 bg-white bg-opacity-5 rounded-full blur-2xl animate-pulse delay-1000"></div>
      <div class="absolute bottom-20 left-1/4 w-16 h-16 bg-white bg-opacity-10 rounded-full blur-xl animate-pulse delay-500"></div>
      
      <div class="relative container mx-auto px-4 py-20 lg:py-32">
        <div class="max-w-6xl mx-auto">
          <div class="grid lg:grid-cols-2 gap-12 items-center">
            <!-- Content -->
            <div class="text-white space-y-8">
              <div class="space-y-6">
                <div class="inline-flex items-center px-4 py-2 bg-white bg-opacity-20 rounded-full text-sm font-medium backdrop-blur-sm">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  {{ $t('home.academicExcellence') }}
                </div>
                
                <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
                  {{ $t('home.welcome') }}
                </h1>
                
                <p class="text-lg md:text-xl opacity-90 leading-relaxed max-w-lg">
                  {{ $t('home.description') }}
                </p>
              </div>
              
              <div class="flex flex-col sm:flex-row gap-4">
                <router-link
                  :to="getLocalizedRoute('ServiceRequest')"
                  class="btn-primary inline-flex items-center justify-center group"
                >
                  {{ $t('services.requestService') }}
                  <svg class="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>
                </router-link>
                
                <router-link
                  :to="getLocalizedRoute('portfolio')"
                  class="btn-secondary inline-flex items-center justify-center"
                >
                  {{ $t('portfolio.title') }}
                </router-link>
              </div>
              
              <!-- Stats -->
              <div class="grid grid-cols-3 gap-6 pt-8 border-t border-white border-opacity-20">
                <div class="text-center">
                  <div class="text-2xl font-bold">500+</div>
                  <div class="text-sm opacity-80">{{ $t('home.projectsCompleted') }}</div>
                </div>
                <div class="text-center">
                  <div class="text-2xl font-bold">98%</div>
                  <div class="text-sm opacity-80">{{ $t('home.successRate') }}</div>
                </div>
                <div class="text-center">
                  <div class="text-2xl font-bold">24/7</div>
                  <div class="text-sm opacity-80">{{ $t('home.support') }}</div>
                </div>
              </div>
            </div>
            
            <!-- Visual -->
            <div class="relative">
              <div class="relative z-10">
                <!-- Main illustration container -->
                <div class="bg-white bg-opacity-10 backdrop-blur-sm rounded-3xl p-8 border border-white border-opacity-20">
                  <div class="grid grid-cols-2 gap-4">
                    <!-- Academic icons -->
                    <div class="bg-white bg-opacity-20 rounded-2xl p-6 text-center">
                      <svg class="w-12 h-12 mx-auto mb-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                      </svg>
                      <p class="text-sm font-medium">{{ $t('portfolio.research') }}</p>
                    </div>
                    
                    <div class="bg-white bg-opacity-20 rounded-2xl p-6 text-center">
                      <svg class="w-12 h-12 mx-auto mb-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      <p class="text-sm font-medium">{{ $t('home.writing') }}</p>
                    </div>
                    
                    <div class="bg-white bg-opacity-20 rounded-2xl p-6 text-center">
                      <svg class="w-12 h-12 mx-auto mb-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                      <p class="text-sm font-medium">{{ $t('portfolio.analysis') }}</p>
                    </div>
                    
                    <div class="bg-white bg-opacity-20 rounded-2xl p-6 text-center">
                      <svg class="w-12 h-12 mx-auto mb-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                      </svg>
                      <p class="text-sm font-medium">{{ $t('home.ideas') }}</p>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Background decoration -->
              <div class="absolute -top-4 -right-4 w-24 h-24 bg-yellow-400 bg-opacity-20 rounded-full blur-xl"></div>
              <div class="absolute -bottom-4 -left-4 w-32 h-32 bg-green-400 bg-opacity-20 rounded-full blur-xl"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Services Section -->
    <div class="py-20 bg-gray-50">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            {{ $t('services.title') }}
          </h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <!-- Research Assistance -->
          <div class="group card p-8 hover:scale-105 transition-all duration-300 relative overflow-hidden">
            <div class="absolute top-0 right-0 w-20 h-20 bg-blue-500 bg-opacity-10 rounded-full -mr-10 -mt-10 group-hover:scale-150 transition-transform duration-500"></div>
            <div class="relative z-10">
              <div class="w-14 h-14 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center mb-6 group-hover:rotate-6 transition-transform duration-300">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900 mb-4 group-hover:text-blue-600 transition-colors">{{ $t('home.researchAssistance') }}</h3>
              <p class="text-gray-600 leading-relaxed mb-6">
                {{ $t('home.researchDescription') }}
              </p>
              <div class="flex items-center text-blue-600 font-medium text-sm group-hover:translate-x-2 transition-transform">
                {{ $t('home.learnMore') }}
                <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </div>
            </div>
          </div>

          <!-- Project Help -->
          <div class="group card p-8 hover:scale-105 transition-all duration-300 relative overflow-hidden">
            <div class="absolute top-0 right-0 w-20 h-20 bg-green-500 bg-opacity-10 rounded-full -mr-10 -mt-10 group-hover:scale-150 transition-transform duration-500"></div>
            <div class="relative z-10">
              <div class="w-14 h-14 bg-gradient-to-br from-green-500 to-green-600 rounded-2xl flex items-center justify-center mb-6 group-hover:rotate-6 transition-transform duration-300">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900 mb-4 group-hover:text-green-600 transition-colors">{{ $t('home.projectHelp') }}</h3>
              <p class="text-gray-600 leading-relaxed mb-6">
                {{ $t('home.projectDescription') }}
              </p>
              <div class="flex items-center text-green-600 font-medium text-sm group-hover:translate-x-2 transition-transform">
                {{ $t('home.learnMore') }}
                <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </div>
            </div>
          </div>

          <!-- Academic Support -->
          <div class="group card p-8 hover:scale-105 transition-all duration-300 relative overflow-hidden">
            <div class="absolute top-0 right-0 w-20 h-20 bg-purple-500 bg-opacity-10 rounded-full -mr-10 -mt-10 group-hover:scale-150 transition-transform duration-500"></div>
            <div class="relative z-10">
              <div class="w-14 h-14 bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center mb-6 group-hover:rotate-6 transition-transform duration-300">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900 mb-4 group-hover:text-purple-600 transition-colors">{{ $t('home.academicSupport') }}</h3>
              <p class="text-gray-600 leading-relaxed mb-6">
                {{ $t('home.academicSupportDescription') }}
              </p>
              <div class="flex items-center text-purple-600 font-medium text-sm group-hover:translate-x-2 transition-transform">
                {{ $t('home.learnMore') }}
                <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Portfolio Section -->
    <div class="py-20 bg-white">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            {{ $t('portfolio.title') }}
          </h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <!-- Portfolio Item 1 -->
          <div class="group card-interactive animate-fade-in-up animate-stagger-1 overflow-hidden">
            <div class="relative h-48 bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center overflow-hidden">
              <div class="absolute inset-0 bg-black bg-opacity-20 group-hover:bg-opacity-10 transition-all duration-300"></div>
              <svg class="w-16 h-16 text-white opacity-80 group-hover:scale-110 transition-transform duration-300 relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
              
              <!-- Overlay on hover -->
              <div class="absolute inset-0 bg-blue-600 bg-opacity-90 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                <div class="text-white text-center">
                  <svg class="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  <p class="text-sm font-medium">{{ $t('portfolio.viewProject') }}</p>
                </div>
              </div>
            </div>
            <div class="p-6">
              <div class="flex items-center justify-between mb-3">
                <h3 class="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">{{ $t('home.project1Title') }}</h3>
                <span class="badge badge-info">{{ $t('portfolio.research') }}</span>
              </div>
              <p class="text-gray-600 text-sm mb-4 leading-relaxed">{{ $t('home.project1Description') }}</p>
              <div class="flex items-center justify-between">
                <div class="flex items-center text-sm text-gray-500">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ $t('portfolio.duration2weeks') }}
                </div>
                <div class="flex items-center space-x-1">
                  <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
                  <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                  <div class="w-2 h-2 bg-purple-500 rounded-full"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Portfolio Item 2 -->
          <div class="group card-interactive animate-fade-in-up animate-stagger-2 overflow-hidden">
            <div class="relative h-48 bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center overflow-hidden">
              <div class="absolute inset-0 bg-black bg-opacity-20 group-hover:bg-opacity-10 transition-all duration-300"></div>
              <svg class="w-16 h-16 text-white opacity-80 group-hover:scale-110 transition-transform duration-300 relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              
              <!-- Overlay on hover -->
              <div class="absolute inset-0 bg-green-600 bg-opacity-90 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                <div class="text-white text-center">
                  <svg class="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  <p class="text-sm font-medium">{{ $t('portfolio.viewProject') }}</p>
                </div>
              </div>
            </div>
            <div class="p-6">
              <div class="flex items-center justify-between mb-3">
                <h3 class="text-lg font-semibold text-gray-900 group-hover:text-green-600 transition-colors">{{ $t('home.project2Title') }}</h3>
                <span class="badge badge-success">{{ $t('portfolio.analysis') }}</span>
              </div>
              <p class="text-gray-600 text-sm mb-4 leading-relaxed">{{ $t('home.project2Description') }}</p>
              <div class="flex items-center justify-between">
                <div class="flex items-center text-sm text-gray-500">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ $t('portfolio.duration3weeks') }}
                </div>
                <div class="flex items-center space-x-1">
                  <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                  <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
                  <div class="w-2 h-2 bg-yellow-500 rounded-full"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Portfolio Item 3 -->
          <div class="group card-interactive animate-fade-in-up animate-stagger-3 overflow-hidden">
            <div class="relative h-48 bg-gradient-to-br from-purple-400 to-purple-600 flex items-center justify-center overflow-hidden">
              <div class="absolute inset-0 bg-black bg-opacity-20 group-hover:bg-opacity-10 transition-all duration-300"></div>
              <svg class="w-16 h-16 text-white opacity-80 group-hover:scale-110 transition-transform duration-300 relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2m-9 0h10m-10 0a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V6a2 2 0 00-2-2" />
              </svg>
              
              <!-- Overlay on hover -->
              <div class="absolute inset-0 bg-purple-600 bg-opacity-90 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                <div class="text-white text-center">
                  <svg class="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  <p class="text-sm font-medium">{{ $t('portfolio.viewProject') }}</p>
                </div>
              </div>
            </div>
            <div class="p-6">
              <div class="flex items-center justify-between mb-3">
                <h3 class="text-lg font-semibold text-gray-900 group-hover:text-purple-600 transition-colors">{{ $t('home.project3Title') }}</h3>
                <span class="badge" style="background-color: #f3e8ff; color: #7c3aed;">{{ $t('portfolio.design') }}</span>
              </div>
              <p class="text-gray-600 text-sm mb-4 leading-relaxed">{{ $t('home.project3Description') }}</p>
              <div class="flex items-center justify-between">
                <div class="flex items-center text-sm text-gray-500">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ $t('portfolio.duration1week') }}
                </div>
                <div class="flex items-center space-x-1">
                  <div class="w-2 h-2 bg-purple-500 rounded-full"></div>
                  <div class="w-2 h-2 bg-pink-500 rounded-full"></div>
                  <div class="w-2 h-2 bg-indigo-500 rounded-full"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Contact Section -->
    <div id="contact-section" class="py-20 bg-gray-50">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            {{ $t('contact.title') }}
          </h2>
        </div>

        <div class="max-w-2xl mx-auto">
          <div class="card-elevated p-8 animate-fade-in-up">
            <form @submit.prevent="handleSubmit" class="space-y-6">
              <div class="form-group animate-fade-in-up animate-stagger-1">
                <label class="form-label">{{ $t('contact.name') }}</label>
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
              
              <div class="form-group animate-fade-in-up animate-stagger-2">
                <label class="form-label">{{ $t('contact.email') }}</label>
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
              
              <div class="form-group animate-fade-in-up animate-stagger-3">
                <label class="form-label">{{ $t('contact.subject') }}</label>
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
              
              <div class="form-group animate-fade-in-up animate-stagger-4">
                <label class="form-label">{{ $t('contact.message') }}</label>
                <textarea
                  v-model="form.message"
                  rows="4"
                  :placeholder="$t('contact.messagePlaceholder')"
                  class="form-input resize-none"
                  :class="{ 'error': errors.message }"
                  required
                ></textarea>
                <div v-if="errors.message" class="form-error">{{ errors.message }}</div>
              </div>
              
              <div class="text-center animate-fade-in-up animate-stagger-5">
                <button
                  type="submit"
                  :disabled="isSubmitting"
                  class="btn-primary touch-feedback"
                  :class="{ 'btn-loading': isSubmitting }"
                >
                  <span v-if="!isSubmitting" class="flex items-center">
                    {{ $t('contact.send') }}
                    <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    </svg>
                  </span>
                  <span v-else class="flex items-center">
                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    {{ $t('common.submitting') }}
                  </span>
                </button>
              </div>
              
              <!-- Success Message -->
              <div v-if="showSuccess" class="text-center animate-fade-in-up">
                <div class="inline-flex items-center px-4 py-2 bg-green-100 text-green-800 rounded-lg">
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ $t('contact.success') }}
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Floating Action Button -->
    <FloatingActionButton />
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useI18n } from 'vue-i18n'
import { useLanguageStore } from '@/stores/language'
import FloatingActionButton from '@/components/ui/FloatingActionButton.vue'

const { t: $t } = useI18n()

const languageStore = useLanguageStore()

// Form state
const form = reactive({
  name: '',
  email: '',
  subject: '',
  message: ''
})

const errors = reactive({})
const isSubmitting = ref(false)
const showSuccess = ref(false)

// Methods
const getLocalizedRoute = (routeName, params = {}) => {
  return languageStore.getLocalizedRoute(routeName, params)
}

const validateForm = () => {
  // Clear previous errors
  Object.keys(errors).forEach(key => delete errors[key])
  
  let isValid = true
  
  if (!form.name.trim()) {
    errors.name = $t('common.required')
    isValid = false
  }
  
  if (!form.email.trim()) {
    errors.email = $t('common.required')
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = $t('common.invalidEmail')
    isValid = false
  }
  
  if (!form.subject.trim()) {
    errors.subject = $t('common.required')
    isValid = false
  }
  
  if (!form.message.trim()) {
    errors.message = $t('common.required')
    isValid = false
  } else if (form.message.trim().length < 10) {
    errors.message = $t('contact.messageMinLength')
    isValid = false
  }
  
  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) {
    // Show validation error notification
    if (window.$notify) {
      window.$notify.error($t('contact.validationError'), $t('contact.fixErrors'))
    }
    return
  }
  
  isSubmitting.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Show success notification
    if (window.$notify) {
      window.$notify.success($t('contact.success'), $t('contact.successMessage'))
    }
    
    // Reset form
    Object.keys(form).forEach(key => form[key] = '')
    
  } catch (error) {
    console.error('Failed to send message:', error)
    
    // Show error notification
    if (window.$notify) {
      window.$notify.error($t('contact.error'), $t('contact.errorMessage'))
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>