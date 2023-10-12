<template>
  <div class="common-layout">
    <el-container>
      <el-header height="5vh">Header</el-header>
      <el-main style="--el-main-padding: 0">
        <cesiumContainer> </cesiumContainer>
      </el-main>
      <el-footer height="25vh" style="--el-footer-padding: 0">
        <echartsContainer></echartsContainer>
      </el-footer>
    </el-container>
  </div>

  <!-- <div class="rightContainer">
    <cesiumContainer>
    </cesiumContainer>
  </div> -->
</template>
<script setup>
import cesiumContainer from '../components/cesiumContainer.vue'
import echartsContainer from '../components/echartsContainer.vue'
</script>

<style>
.common-layout {
  height: 100vh; /* 设置容器高度为视口高度 */
  display: flex; /* 使用弹性布局 */
  /* flex-direction: column; 垂直排列子元素 */
}
</style>
