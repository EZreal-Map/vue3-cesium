<template>
  <div id="cesiumContainer"></div>
</template>

<script setup>
import * as Cesium from 'cesium'
import { onMounted, watchEffect } from 'vue'
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
  // viewer.camera.flyTo({
  //   destination: Cesium.Cartesian3.fromDegrees(113.39811, 31.699212, 4000.0), // 例如：1000
  //   orientation: {
  //     heading: Cesium.Math.toRadians(0.0), // 指定航向角度
  //     pitch: Cesium.Math.toRadians(-90.0), // 指定俯仰角度
  //     roll: 0.0 // 指定翻滚角度
  //   }
  // })
  // 清除默认鼠标左键点击事件
  viewer.screenSpaceEventHandler.removeInputAction(
    Cesium.ScreenSpaceEventType.LEFT_CLICK
  )
  viewer.screenSpaceEventHandler.removeInputAction(
    Cesium.ScreenSpaceEventType.LEFT_DOUBLE_CLICK
  )
  // 加载单个GLB方法
  async function loadingGLB(num, IsShow = true) {
    const position = Cesium.Cartesian3.fromDegrees(
      113.39592268502284,
      31.704985763068212,
      61.0309417
    )
    return viewer.entities.add({
      name: num,
      show: IsShow,
      position: position,
      orientation: Cesium.Transforms.headingPitchRollQuaternion(
        position,
        new Cesium.HeadingPitchRoll(
          Cesium.Math.toRadians(0),
          Cesium.Math.toRadians(90),
          Cesium.Math.toRadians(-90)
        )
      ),
      model: {
        uri: `/python/flood/${floodStore.years}/glb/${num}/triangle_mesh_0.05.glb`,
        // show: IsShow
        // preloadWhenHidden: preload
        // color: Cesium.Color.fromBytes(190,228,246,230),
        // color: Cesium.Color.fromBytes(255, 255, 255, 230),
        // colorBlendAmount:0.5,
        colorBlendMode: Cesium.Cesium3DTileColorBlendMode.HIGHLIGHT,
        // showOutline:true,
        // silhouetteColor: Cesium.Color.RED
        allowPicking: false
      }
    })
  }
  // 预加载按钮模块
  // 用于建立索引和 tileset 的关系 ***重要变量***
  let floodPrimitivesGLB = {}
  async function renderTilesetWithAnimationGLB(subcontents) {
    floodPrimitivesGLB = {}
    // 异步加载 tileset 并建立映射关系
    await Promise.all(
      subcontents.map(async (item, index) => {
        try {
          const tileset = await loadingGLB(item)
          // viewer.scene.primitives.add(tileset); // 添加到场景
          floodPrimitivesGLB[index] = tileset // 建立索引和 tileset 的映射关系
        } catch (error) {
          console.log(error)
        }
      })
    )
    // 在所有 tileset 加载完成后执行的代码
    floodPrimitivesGLB = Object.values(floodPrimitivesGLB)
    floodStore.initReady = true
    // console.log(floodPrimitivesGLB.forEach((item) => console.log(item.name)))
    // console.log('全部加载完成 : ' + floodPrimitivesGLB.length)
    // floodPrimitivesGLB.forEach((primitive) =>primitive.show = false);
  }
  renderTilesetWithAnimationGLB(floodStore.subcontents)

  // 加载播放动画模块
  function showFloodPrimitivesGLB(index) {
    // 隐藏
    if (Array.isArray(floodPrimitivesGLB)) {
      floodPrimitivesGLB.forEach((primitive) => (primitive.show = false))
      // 显示
      floodPrimitivesGLB[index - 1].show = true
    }
  }
  watchEffect(() => {
    if (building) {
      // console.log(building)
      // console.log(stateStore.showBuliding)
      building.show = stateStore.showBuliding
    }

    if (floodPrimitivesGLB && floodStore.index != 0) {
      showFloodPrimitivesGLB(floodStore.index)
    }
  })

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
