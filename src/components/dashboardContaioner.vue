<template>
  <div class="container">
    <div>
      <div>
        <el-progress type="dashboard" :percentage="percentage || 0">
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
            <CaretLeft @click="floodStore.setIndex(floodStore.index - 1)" />
          </el-icon>
        </el-link>
        <el-link :underline="false">
          <el-icon v-if="!intervalID" size="35px" @click="playStartHandle">
            <VideoPlay
          /></el-icon>
          <el-icon v-else size="35px" @click="stopInterval"
            ><VideoPause
          /></el-icon>
        </el-link>
        <el-link :underline="false">
          <el-icon size="40px">
            <CaretRight @click="floodStore.setIndex(floodStore.index + 1)" />
          </el-icon>
        </el-link>
        <!-- <el-button></el-button> -->
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  CaretLeft,
  CaretRight,
  VideoPlay,
  VideoPause
} from '@element-plus/icons-vue'
import { onMounted, ref, watchEffect } from 'vue'
import { useFloodStore } from '../stores/flood'

const percentage = ref(0)
const floodStore = useFloodStore()
onMounted(() => {
  watchEffect(() => {
    percentage.value = (floodStore.index / floodStore.maxIndex) * 100
  })
})

const intervalID = ref(null) // 创建 ref 变量

const playStartHandle = () => {
  if (intervalID.value === null) {
    intervalID.value = setInterval(() => {
      floodStore.setIndex(floodStore.index + 1)
    }, 200)
  }
}

const stopInterval = () => {
  if (intervalID.value !== null) {
    clearInterval(intervalID.value)
    intervalID.value = null
  }
}
</script>

<style scoped>
.container {
  display: flex;
  align-items: center; /* 垂直居中对齐 */
  justify-content: center; /* 水平居中对齐 */
  height: 100%; /* 设置容器高度 */
}
</style>
