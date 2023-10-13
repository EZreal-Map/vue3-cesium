<template>
  <div>
    <div class="legend-container">
      <canvas ref="canvas" width="70" height="253"></canvas>
    </div>
    <div class="legend-container legend-container-right">
      <div class="legend-text" v-for="num in [5, 4, 3, 2, 0.01]" :key="num">
        {{ num }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const canvas = ref(null) // ref 绑定dom的时候，需要放在setup里面
onMounted(() => {
  console.log(canvas)
  const ctx = canvas.value.getContext('2d')
  console.log(ctx)

  const start_color = [149, 208, 238]
  const end_color = [10, 9, 145]

  const gradient = ctx.createLinearGradient(0, 0, 0, canvas.value.height)
  gradient.addColorStop(1, `rgb(${start_color.join(',')})`)
  gradient.addColorStop(0, `rgb(${end_color.join(',')})`)

  ctx.fillStyle = gradient
  ctx.fillRect(0, 0, canvas.value.width, canvas.value.height)
})
</script>

<style scoped>
.legend-container {
  display: inline-block;
  vertical-align: top;
}

.legend-text {
  color: black;
  font-size: 16px;
  background-color: rgba(255, 255, 255, 0.5);
  padding-bottom: 40px;
  font-weight: 700;
}

.legend-text:last-child {
  padding-bottom: 0;
}
</style>
