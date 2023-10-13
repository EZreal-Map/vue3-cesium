<template>
  <div class="common-layout">
    <el-container>
      <el-header height="0vh">
        <legendContainer class="legendContainer"></legendContainer>
        {{ floodStore.index }}
      </el-header>
      <el-main style="--el-main-padding: 0">
        <cesiumContainer> </cesiumContainer>
      </el-main>
      <el-footer height="20vh" style="--el-footer-padding: 0">
        <div class="footer-left">
          <dashboardContaioner></dashboardContaioner>
        </div>
        <div class="footer-right">
          <echartsContainer></echartsContainer>
        </div>
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
import legendContainer from '../components/legendContainer.vue'
import dashboardContaioner from '../components/dashboardContaioner.vue'
import { useFloodStore } from '../stores/flood'

const floodStore = useFloodStore()

;(async () => {
  console.log('hello start')
  await floodStore.initSubcontents(
    '@/../python/flood/30years/glb/subcontents.txt'
  )
  // console.log(floodStore.subcontents)
  await floodStore.initEchartSeries(
    '@/../python/flood/30years/glb/echartSeries.txt'
  )
  // console.log(floodStore.echartSeries)
  floodStore.initReady = true
  console.log(floodStore.initReady)
})()

// console.log(floodStore.subcontents[150])
</script>

<style>
.common-layout {
  height: 100vh;
  display: flex;
}
.footer-left {
  width: 10%;
  height: 100%;
  float: left;
  background-color: #ccc;
}

.footer-right {
  width: 90%;
  height: 100%;
  float: right;
  background-color: #ddd;
}
.legendContainer {
  position: absolute;
  top: 20px;
  left: 30px;
  z-index: 10;
}
</style>
