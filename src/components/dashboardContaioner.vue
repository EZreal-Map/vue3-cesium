<template>
  <div class="container">
    <div>
      <div>
        <el-progress
          ref="dashBoardDom"
          type="dashboard"
          :percentage="50"
          :color="colors"
        />
      </div>

      <div>
        <el-link :underline="false">
          <el-icon size="40px"><CaretLeft /></el-icon>
        </el-link>
        <el-link :underline="false">
          <el-icon size="35px"><VideoPlay /></el-icon>
        </el-link>
        <el-link :underline="false">
          <el-icon size="40px"><CaretRight /></el-icon>
        </el-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { CaretLeft, CaretRight, VideoPlay } from '@element-plus/icons-vue'
import { onMounted, ref } from 'vue'
const dashBoardDom = ref(null)

onMounted(() => {
  const span = dashBoardDom.value.$el.querySelector('span')
  span.innerHTML = '123/175'
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
