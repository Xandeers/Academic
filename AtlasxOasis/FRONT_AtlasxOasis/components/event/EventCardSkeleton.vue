<template>
  <div class="skeleton-card">
    <div class="skeleton skeleton--img" />
    <div class="skeleton-body">
      <div class="skeleton skeleton--cat" />
      <div class="skeleton skeleton--title" />
      <div class="skeleton skeleton--meta" />
    </div>
    <div class="skeleton-footer">
      <div class="skeleton skeleton--price" />
      <div class="skeleton skeleton--btn" />
    </div>
  </div>
</template>

<style scoped>
.skeleton-card { background: var(--s1); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
.skeleton {
  background: linear-gradient(90deg, var(--s2) 0%, var(--s3) 50%, var(--s2) 100%);
  background-size: 200% 100%; border-radius: 4px;
  animation: shimmer 1.4s ease infinite;
}
.skeleton--img   { height: 140px; border-radius: 0; }
.skeleton--cat   { height: 10px; width: 60px; }
.skeleton--title { height: 14px; width: 85%; }
.skeleton--meta  { height: 10px; width: 65%; }
.skeleton--price { height: 16px; width: 48px; }
.skeleton--btn   { height: 28px; width: 80px; border-radius: 6px; }
.skeleton-body { padding: 14px 16px; display: flex; flex-direction: column; gap: 10px; }
.skeleton-footer { padding: 12px 16px; border-top: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; }
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
</style>