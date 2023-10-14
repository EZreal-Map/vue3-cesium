<template>
  <div class="legend-container">
    <div class="legend" ref="legend">
      <div
        v-for="(item, index) in legendItems"
        :key="index"
        class="legend-item"
      >
        <div class="color-box" :style="{ backgroundColor: item.color }"></div>
        <div class="label-text">{{ item.label }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  setup() {
    const intervals = [
      0,
      0.01,
      0.25,
      0.5,
      1.0,
      1.5,
      2.0,
      2.5,
      3,
      3.5,
      4,
      4.5,
      5,
      7.5,
      10,
      Infinity
    ]
    const length = intervals.length
    const startColor = [149, 208, 238]
    const endColor = [10, 9, 145]

    const legendItems = ref([])

    onMounted(() => {
      const gradientColors = generateColorGradient(
        intervals.length - 1,
        endColor,
        startColor
      )

      legendItems.value = intervals
        .slice(1)
        .map((end, index) => {
          const start = intervals[index]
          return {
            color: gradientColors[index],
            label: `${start.toFixed(2)} - ${end - 0.01}`
          }
        })
        .reverse()

      // 修改 label第一个lable > intervals倒数第二个数(最大值)
      legendItems.value[0].label = `> ${intervals[length - 2]}`
      legendItems.value[length - 2].label = `< ${intervals[1]}`
    })

    function generateColorGradient(numSegments, startColor, endColor) {
      const gradientColors = []
      for (let i = numSegments - 1; i >= 0; i--) {
        const t = i / (numSegments - 1)
        const r = Math.round(startColor[0] + (endColor[0] - startColor[0]) * t)
        const g = Math.round(startColor[1] + (endColor[1] - startColor[1]) * t)
        const b = Math.round(startColor[2] + (endColor[2] - startColor[2]) * t)
        gradientColors.push(`rgb(${r}, ${g}, ${b})`)
      }
      return gradientColors
    }

    return {
      legendItems
    }
  }
}
</script>

<style>
.legend-container {
  background-color: rgba(255, 255, 255, 0.7);
  padding: 20px;
  border: 1px solid #ccc;
  max-width: 180px;
}

.legend {
  color: #000;
  display: flex;
  flex-direction: column;
  font-size: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.color-box {
  width: 50px;
  height: 20px;
  border: 1px solid #000;
  margin-right: 10px;
}

.label-text {
  width: 80px;
  white-space: pre; /* 保留连续的空格 */
}
</style>
