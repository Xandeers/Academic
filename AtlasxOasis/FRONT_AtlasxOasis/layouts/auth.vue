<template>
  <div class="min-h-screen bg-bg text-[#E9EEEC] font-body flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <NuxtLink to="/" class="block text-center font-title text-xl text-accent mb-8 tracking-wide">
        AtlasXOasis
      </NuxtLink>
      <slot />
    </div>
  </div>
</template>