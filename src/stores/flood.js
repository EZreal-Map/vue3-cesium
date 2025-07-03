import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useFloodStore = defineStore('flood', () => {
  const index = ref(0)
  const maxIndex = computed(() => subcontents.value.length)
  const years = ref('30years')
  let initReady = ref(false)
  let subcontents = ref([])
  let echartSeries = ref([])

  function setIndex(newIndex) {
    if (newIndex > maxIndex.value) {
      index.value = 1
    } else if (newIndex < 1) {
      index.value = maxIndex.value
    } else {
      index.value = newIndex
    }
  }

  function setYears(newYears) {
    years.value = newYears
  }

  async function initSubcontents(subcontentFilePath) {
    const response = await fetch(subcontentFilePath)
    const data = await response.text()
    subcontents.value = data.split('\n').map(parseFloat)
  }

  async function initEchartSeries(echartSeriesFilePath) {
    const response = await fetch(echartSeriesFilePath)
    const data = await response.text()
    echartSeries.value = data.split('\n').map(parseFloat)
  }

  return {
    index,
    maxIndex,
    years,
    initReady,
    subcontents,
    echartSeries,
    setIndex,
    setYears,
    initSubcontents,
    initEchartSeries
  }
})
