import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useColorStore = defineStore('color', () => {
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
    Infinity
  ]
  const length = ref(intervals.length)
  const startColor = [149, 208, 238]
  const endColor = [10, 9, 145]
  const legendItems = ref([])

  const generateColorGradient = (numSegments, startColor, endColor) => {
    const gradientColors = []
    for (let i = numSegments - 1; i >= 0; i--) {
      const t = i / (numSegments - 1)
      const r = Math.round(startColor[0] + (endColor[0] - startColor[0]) * t)
      const g = Math.round(startColor[1] + (endColor[1] - startColor[1]) * t)
      const b = Math.round(startColor[2] + (endColor[2] - startColor[2]) * t)
      gradientColors.push([r, g, b])
    }
    return gradientColors
  }

  const gradientColors = generateColorGradient(
    intervals.length - 1,
    endColor,
    startColor
  )
  console.log('gradientColors:', gradientColors)

  legendItems.value = intervals
    .slice(1)
    .map((end, index) => {
      const start = intervals[index]
      return {
        color: `rgb(${gradientColors[index].join(', ')})`,
        label: `${start.toFixed(2)} - ${end - 0.01}`
      }
    })
    .reverse()

  // 修改 label第一个lable > intervals倒数第二个数(最大值)
  legendItems.value[0].label = `> ${intervals[length.value - 2]}`
  legendItems.value[length.value - 2].label = `< ${intervals[1]}`

  return {
    intervals,
    length,
    gradientColors,
    legendItems
  }
})
