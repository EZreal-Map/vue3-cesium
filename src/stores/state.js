import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useStateStore = defineStore(
  'state',
  () => {
    const visibility = ref(true)
    const showBuliding = ref(true)

    function negateVisibility() {
      visibility.value = !visibility.value
    }
    function negateshowBuliding() {
      showBuliding.value = !showBuliding.value
    }

    return {
      visibility,
      showBuliding,
      negateVisibility,
      negateshowBuliding
    }
  },
  {
    persist: {
      paths: ['visibility', 'showBuliding']
    }
  }
)
