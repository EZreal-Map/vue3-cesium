<template>
  <div id="cesiumContainer"></div>
</template>

<script setup>
import * as Cesium from 'cesium'
import { onMounted } from 'vue'
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
  // 调整研究区域视角
  viewer.camera.flyTo({
    destination: Cesium.Cartesian3.fromDegrees(113.39811, 31.699212, 4000.0), // 例如：1000
    orientation: {
      heading: Cesium.Math.toRadians(0.0), // 指定航向角度
      pitch: Cesium.Math.toRadians(-90.0), // 指定俯仰角度
      roll: 0.0 // 指定翻滚角度
    }
  })
  // 调整全局光源
  viewer.scene.light = new Cesium.DirectionalLight({
    color: new Cesium.Color(1.0, 1.0, 1.0, 1),
    direction: new Cesium.Cartesian3(0, -1, 1), // 将方向修改为斜向建筑物
    intensity: 10
  })
  // 加载建筑白膜
  const tileset = await Cesium.Cesium3DTileset.fromIonAssetId(2236714)
  viewer.scene.primitives.add(tileset)
})
</script>

<style>
#cesiumContainer {
  width: 100%;
  height: 100vh;
  padding: 0;
  margin: 0;
  overflow: hidden;
}

.cesium-widget-credits {
  display: none !important;
}
</style>
