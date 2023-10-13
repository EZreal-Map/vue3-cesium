<template>
  <div class="container">
    <div>
      <div>
        <el-progress type="dashboard" :percentage="percentage">
          <span class="percentage-value">
            <span>{{ floodStore.index }} / </span>
            <span>{{ floodStore.maxIndex }}</span>
          </span>
        </el-progress>
        <!-- :color="colors" 这里还可以定义颜色环属性，待考虑 -->
      </div>

      <div>
        <el-link :underline="false">
          <el-icon size="40px">
            <CaretLeft @click="floodStore.index -= 1" />
          </el-icon>
        </el-link>
        <el-link :underline="false">
          <el-icon size="35px"><VideoPlay /></el-icon>
        </el-link>
        <el-link :underline="false">
          <el-icon size="40px">
            <CaretRight @click="floodStore.index += 1" />
          </el-icon>
        </el-link>
        <!-- <el-button></el-button> -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { CaretLeft, CaretRight, VideoPlay } from '@element-plus/icons-vue'
import { onMounted, ref, watchEffect } from 'vue'
import { useFloodStore } from '../stores/flood'

const percentage = ref(0)
const floodStore = useFloodStore()
onMounted(() => {
  watchEffect(() => {
    percentage.value = (floodStore.index / floodStore.maxIndex) * 100
  })
})
</script>

<style scoped>
.container {
  display: flex;
  align-items: center; /* 垂直居中对齐 */
  justify-content: center; /* 水平居中对齐 */
  height: 100%; /* 设置容器高度 */
}
</style>
