<template>
  <div id="cesiumContainer"></div>
</template>

<script setup>
import * as Cesium from 'cesium'
import { onMounted, watchEffect, watch } from 'vue'
import { useFloodStore } from '@/stores/flood'
const floodStore = useFloodStore()
import { ElMessage } from 'element-plus'
import { useColorStore } from '@/stores/color'
const colorStore = useColorStore()
import { useStateStore } from '@/stores/state'
const stateStore = useStateStore()

onMounted(async () => {
  Cesium.Ion.defaultAccessToken =
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJlODBjMmY1YS00NjZjLTQwZjUtYTVhNy05NDBiODliYWYwMzUiLCJpZCI6MTU1ODM0LCJpYXQiOjE2OTAwOTA4MTN9.s-rWLcdw5_e2j9Fz2l41ydsl23lAVJg2Q3XhThRUeRM'
  const viewer = new Cesium.Viewer('cesiumContainer', {
    geocoder: false, //隐藏查找控件
    homeButton: false, //隐藏视角返回初始位置按钮
    sceneModePicker: false, //隐藏视角模式3D 2D CV
    baseLayerPicker: false, //隐藏图层选择
    navigationHelpButton: false, //隐藏帮助
    animation: false, //隐藏动画控件
    timeline: false, //隐藏时间线控件
    fullscreenButton: false, //隐藏全屏
    terrainProvider: await Cesium.CesiumTerrainProvider.fromIonAssetId(2248627)
  })

  // 调整全局光源
  viewer.scene.light = new Cesium.DirectionalLight({
    color: new Cesium.Color(1.0, 1.0, 1.0, 1),
    direction: new Cesium.Cartesian3(0, -1, 1), // 将方向修改为斜向建筑物
    intensity: 10
  })
  // 加载建筑白膜
  const building = await Cesium.Cesium3DTileset.fromIonAssetId(2236714)
  viewer.scene.primitives.add(building)
  // building.show = false
  // 聚焦研究区域  调整研究区域视角
  viewer.zoomTo(building)

  // 清除默认鼠标左键点击事件
  viewer.screenSpaceEventHandler.removeInputAction(
    Cesium.ScreenSpaceEventType.LEFT_CLICK
  )
  viewer.screenSpaceEventHandler.removeInputAction(
    Cesium.ScreenSpaceEventType.LEFT_DOUBLE_CLICK
  )

  const PNGPosition = Cesium.Rectangle.fromDegrees(
    113.38126405683018,
    31.688171025895564,
    113.40541413682514,
    31.71745736808518
  )

  // 使用 ImageMaterialProperty 加载 PNG 图像
  // async function loadPNG(num, IsShow = true) {
  //   // 添加影像图层
  //   return viewer.entities.add({
  //     show: IsShow,
  //     rectangle: {
  //       coordinates: PNGPosition,
  //       material: new Cesium.ImageMaterialProperty({
  //         image: `/python/flood/${floodStore.years}/png/${num}/flood_interpolated.png`,
  //         transparent: true
  //       })
  //     }
  //   })
  // }
  // 使用 SingleTileImageryProvider 加载 PNG 图像
  async function loadPNG(num, IsShow = true) {
    const imageUrl = `/python/flood/${floodStore.years}/png/${num}/flood_interpolated.png`
    const provider = new Cesium.SingleTileImageryProvider({
      url: imageUrl,
      rectangle: PNGPosition,
      tileWidth: 256, // 单瓦片宽度 设置256就行，不用管图片真实大小
      tileHeight: 256
    })

    const layer = viewer.imageryLayers.addImageryProvider(provider)
    layer.show = IsShow // 默认不显示
    return layer
  }

  let floodPrimitivesPNG = []

  async function renderTilesetWithAnimationPNG(subcontents) {
    floodPrimitivesPNG = []
    await Promise.all(
      subcontents.map(async (item, index) => {
        try {
          const layer = await loadPNG(item, false) // 初始化时全部显示
          floodPrimitivesPNG[index] = layer
        } catch (error) {
          console.warn(`PNG 加载失败：${item}`, error)
        }
      })
    )
    // 在所有 tileset 加载完成后执行的代码
    floodPrimitivesPNG = Object.values(floodPrimitivesPNG)
    floodStore.initReady = true
    floodStore.index = 1 // 初始化索引为 1，同时会触发 watch 监听器，加载第一个洪水
  }

  renderTilesetWithAnimationPNG(floodStore.subcontents)

  watchEffect(async () => {
    if (building) {
      building.show = stateStore.showBuliding
    }
  })

  // 👇 监听 floodStore.index
  watch(
    [() => floodStore.index, () => stateStore.playInterval],
    ([newIndex, isPlaying]) => {
      // 清空所有图层
      floodPrimitivesPNG.forEach((layer) => {
        layer.show = false
      })

      // 显示当前帧
      if (floodPrimitivesPNG[newIndex - 1]) {
        floodPrimitivesPNG[newIndex - 1].show = true
      }

      // 如果正在播放，显示前一帧
      if (isPlaying && floodPrimitivesPNG[newIndex - 2]) {
        floodPrimitivesPNG[newIndex - 2].show = true
      }
    },
    { immediate: true }
  )

  // 新添加颜色pick模块（待更新完善）
  const scene = viewer.scene
  const context = scene.context

  let readColor = false
  let pickPosition = null // 定义 pickPosition 变量

  viewer.scene.camera.percentageChanged = 0.01 // 设置缩放触发阈值
  // 添加鼠标点击事件监听器
  viewer.canvas.addEventListener('contextmenu', function (event) {
    event.preventDefault() // 阻止右键菜单的默认行为
    readColor = true
    const canvas = viewer.canvas
    const rect = canvas.getBoundingClientRect()
    console.log(rect)
    pickPosition = new Cesium.Cartesian2(
      event.clientX - rect.left,
      event.clientY - rect.top
    )
    console.log(pickPosition)
    const pickRay = viewer.scene.camera.getPickRay(pickPosition)

    const cartesian = viewer.scene.globe.pick(pickRay, viewer.scene)
    if (Cesium.defined(cartesian)) {
      const cartographic = Cesium.Cartographic.fromCartesian(cartesian)
      const longitude = Cesium.Math.toDegrees(cartographic.longitude)
      const latitude = Cesium.Math.toDegrees(cartographic.latitude)
      console.log('点击位置的经纬度坐标：' + longitude + ', ' + latitude)
    }
  })

  scene.postRender.addEventListener(function () {
    if (readColor && pickPosition !== null) {
      const pixels = context.readPixels({
        x: pickPosition.x,
        y: pickPosition.y,
        width: 1,
        height: 1
      })
      // r = pixels[0]
      const rgbArray = Object.values(pixels).slice(0, 3)
      console.log(colorStore.gradientColors)
      let rgbRange = colorStore.findColorIndices(rgbArray, [
        [255, 255, 255],
        ...colorStore.gradientColors
      ])
      const min = Math.min(...Object.values(rgbRange))
      const sumOfDeviations = rgbRange.reduce((acc, val) => acc + val - min, 0)
      console.log('Sum of Absolute Deviations:', sumOfDeviations)

      console.log('Red Range:', rgbRange[0])
      console.log('Green Range:', rgbRange[1])
      console.log('Blue Range:', rgbRange[2])
      console.log('鼠标点击位置的颜色值:', pixels[0])
      console.log('鼠标点击位置的颜色值:', pixels[1])
      console.log('鼠标点击位置的颜色值:', pixels[2])
      console.log(min)
      const index = colorStore.length - min - 1
      console.log(index)
      ElMessage({
        message: `${colorStore?.legendItems[index]?.label} `,
        type: sumOfDeviations < 2.1 ? 'success' : 'warning'
      })

      readColor = false
      pickPosition = null // 重置 pickPosition
    }
  })
})
</script>

<style>
#cesiumContainer {
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
  overflow: hidden;
}

.cesium-widget-credits {
  display: none !important;
}
</style>
