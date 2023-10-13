import { ref, computed, watch } from 'vue'
import { defineStore } from 'pinia'

export const useFloodStore = defineStore('flood', () => {
  let subcontents = ref([])
  const index = ref(0)
  const maxIndex = computed(() => subcontents.value.length)
  function setIndex(newIndex) {
    if (newIndex > maxIndex.value) {
      index.value = 1
    } else if (newIndex < 1) {
      index.value = maxIndex.value
    } else {
      index.value = newIndex
    }
  }
  async function initSubcontents(subcontentFilePath) {
    const response = await fetch(subcontentFilePath)
    const data = await response.text()
    subcontents.value = data.split('\n').map(parseFloat)
  }
  // watch(index, (newValue, oldValue) => {
  //   console.log(`count发生了变化，老值为${oldValue},新值为${newValue}`)
  // })

  return { subcontents, index, maxIndex, setIndex, initSubcontents }
})
