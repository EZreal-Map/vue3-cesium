<template>
  <div class="container">
    <div
      class="box"
      :class="{ boxActive: activeBoxIndex === 1 }"
      @click="changeSelectBox(1)"
    >
      5年一遇洪水
    </div>
    <div
      class="box"
      :class="{ boxActive: activeBoxIndex === 2 }"
      @click="changeSelectBox(2)"
    >
      30年一遇洪水
    </div>
    <div
      class="box"
      :class="{ boxActive: activeBoxIndex === 3 }"
      @click="changeSelectBox(3)"
    >
      50年一遇洪水
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useFloodStore } from '../stores/flood'
const router = useRouter()
const route = useRoute()
const floodStore = useFloodStore()
const routerArray = ['5years', '30years', '50years']
let activeBoxIndex = ref(routerArray.indexOf(floodStore.years) + 1)

const changeSelectBox = (index) => {
  activeBoxIndex.value = index
  const newYears = routerArray[index - 1]

  console.log('切换洪水类型:', newYears)

  const newRoute = {
    name: 'flood',
    params: { years: newYears },
    query: route.query // 保留原有 query（如 ?type=glb/?type=png）
  }

  // 更新 floodStore 的 years (持久化存储)
  floodStore.setYears(routerArray[index - 1])
  // 正确方式获取完整 href 字符串
  const href = router.resolve(newRoute).href
  // 路由跳转（非刷新）
  // router.push(newRoute).catch(() => {})
  // 强制刷新页面（如果你确实需要重建场景）
  window.location.href = href
}
</script>

<style scoped>
.legend-container {
  background-color: rgba(255, 255, 255, 0.7);
  padding: 20px;
  border: 1px solid #ccc;
  max-width: 180px;
}
.box {
  width: 120px; /* 统一设置宽度 */
  background-color: #0a0991;
  color: #ffffff;
  padding: 10px 20px;
  margin: 10px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  font-size: 18px;
  cursor: pointer;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.container {
  background-color: rgba(255, 255, 255, 0.7);
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 20px;
}

.boxActive {
  background-color: #ffa500; /* 设置选中盒子的颜色 */
}
</style>
