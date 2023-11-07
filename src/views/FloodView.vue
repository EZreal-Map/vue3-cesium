<template>
  <div class="common-layout">
    <el-container>
      <el-header height="0vh">
        <transition name="fade">
          <legendContainer
            v-show="stateStore.visibility"
            class="legendContainer"
          >
          </legendContainer>
        </transition>
        <transition name="fade">
          <selectContainer
            class="selectContainer"
            v-show="stateStore.visibility"
          ></selectContainer>
        </transition>
      </el-header>

      <el-main class="main" style="--el-main-padding: 0">
        <cesiumContainer> </cesiumContainer>
        <div class="buttonPanel">
          <div class="buttonPanel-left">
            <el-link :underline="false">
              <el-icon
                v-if="stateStore.visibility"
                size="40px"
                @click="stateStore.negateVisibility"
              >
                <Bottom
              /></el-icon>
              <el-icon v-else size="40px" @click="stateStore.negateVisibility"
                ><Top
              /></el-icon>
            </el-link>
          </div>
          <div class="buttonPanel-right">
            <el-link :underline="false">
              <el-icon
                v-if="stateStore.showBuliding"
                size="40px"
                @click="stateStore.negateshowBuliding"
              >
                <View
              /></el-icon>
              <el-icon v-else size="40px" @click="stateStore.negateshowBuliding"
                ><Hide
              /></el-icon>
            </el-link>
          </div>
        </div>
      </el-main>

      <el-footer
        :class="stateStore.visibility ? 'active' : 'inactive'"
        class="footerContainer"
        style="--el-footer-padding: 0"
      >
        <!-- <div class="footerContainer"> -->
        <div class="footer-left">
          <dashboardContaioner></dashboardContaioner>
        </div>
        <div class="footer-right">
          <echartsContainer></echartsContainer>
        </div>
        <!-- </div> -->
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
import selectContainer from '../components/selectContainer.vue'
import { useFloodStore } from '../stores/flood'
import { useStateStore } from '../stores/state'
import { useRoute } from 'vue-router'
import { Top, Bottom, View, Hide } from '@element-plus/icons-vue'

const floodStore = useFloodStore()
const stateStore = useStateStore()

const route = useRoute()
console.log('hello start :', route.params.years)
floodStore.setYears(route.params.years)
;(async () => {
  //绝对路径来解决这个问题
  await floodStore.initSubcontents(
    `/python/flood/${floodStore.years}/glb/subcontents.txt`
  )
  // console.log(floodStore.subcontents)
  await floodStore.initEchartSeries(
    `/python/flood/${floodStore.years}/glb/echartSeries.txt`
  )
  // console.log(floodStore.echartSeries)
  floodStore.initReady = true // 子文件数据+echartSeries数据加载完成
  // console.log(floodStore.initReady)
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
  background-color: rgb(149, 208, 238);
}

.footer-right {
  width: 90%;
  height: 100%;
  float: right;
  background-color: rgb(149, 208, 238);
}
.legendContainer {
  position: absolute;
  top: 20px;
  left: 30px;
  z-index: 10;
}

.selectContainer {
  position: absolute;
  top: 20px;
  right: 30px;
  z-index: 10;
}

.main {
  position: relative;
}

.buttonPanel-left {
  display: inline-block;
  position: absolute;
  left: 10px;
  bottom: 10px;
}
.buttonPanel-right {
  display: inline-block;
  position: absolute;
  right: 10px;
  bottom: 10px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.active {
  height: 180px;
  transition: height 1s; /* 设置高度变化的过渡效果，持续1秒 */
}

.inactive {
  height: 0;
  transition: height 1s; /* 设置高度变化的过渡效果，持续1秒 */
}
</style>
