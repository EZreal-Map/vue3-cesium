import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useStateStore = defineStore(
  'state',
  () => {
    const visibility = ref(true)

    function negateVisibility() {
      visibility.value = !visibility.value
    }

    return {
      visibility,
      negateVisibility
    }
  },
  {
    persist: {
      paths: ['visibility']
    }
  }
)
