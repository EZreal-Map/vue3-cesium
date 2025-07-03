import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useStateStore = defineStore(
  'state',
  () => {
    const visibility = ref(true)
    const showBuliding = ref(true)
    const playInterval = ref(null)

    function negateVisibility() {
      visibility.value = !visibility.value
    }
    function negateshowBuliding() {
      showBuliding.value = !showBuliding.value
    }

    function setPlayInterval(interval) {
      playInterval.value = interval
    }

    return {
      visibility,
      showBuliding,
      negateVisibility,
      negateshowBuliding,
      playInterval,
      setPlayInterval
    }
  },
  {
    persist: {
      paths: ['visibility', 'showBuliding']
    }
  }
)
