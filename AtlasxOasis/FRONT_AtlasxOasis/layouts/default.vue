<template>
  <div class="min-h-screen bg-bg text-[#E9EEEC] flex flex-col">
    <AppHeader />
    <main class="flex-1 px-7 py-5 max-w-[1140px] mx-auto w-full">
      <slot />
    </main>
    <footer class="bg-s1 border border-white/10 rounded-xl mx-7 mb-7 h-11 flex items-center justify-center gap-5 text-[11px] text-muted">
      <span class="font-title text-accent">AtlasXOasis</span>
      <span>©2026</span>
      <span>CGU</span>
      <span>Contact</span>
    </footer>
  </div>
</template>
