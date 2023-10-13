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
        uri: `@/../python/flood/30years/glb/${num}/triangle_mesh_0.05.glb`,
        // show: IsShow
        // preloadWhenHidden: preload
        // color: Cesium.Color.fromBytes(190,228,246,230),
        // color: Cesium.Color.fromBytes(255, 255, 255, 230),
        // colorBlendAmount:0.5,
        colorBlendMode: Cesium.Cesium3DTileColorBlendMode.HIGHLIGHT
        // showOutline:true,
        // silhouetteColor: Cesium.Color.RED
      }
    })
  }
  loadingGLB(21000)
  // // 预加载按钮模块
  // let currentTilesetGLB
  // let floodPrimitivesGLB = {} // 用于建立索引和 tileset 的关系
  // async function renderTilesetWithAnimationGLB(subcontent) {
  //   floodPrimitivesGLB = {}
  //   // 异步加载 tileset 并建立映射关系
  //   await Promise.all(
  //     subcontent.map(async (item, index) => {
  //       try {
  //         const tileset = await loadingGLB(item)

  //         // viewer.scene.primitives.add(tileset); // 添加到场景
  //         floodPrimitivesGLB[index] = tileset // 建立索引和 tileset 的映射关系

  //         inputNumberGLB.value = index + 1
  //       } catch (error) {
  //         console.log(error)
  //       }
  //     })
  //   )
  //   // 在所有 tileset 加载完成后执行的代码
  //   floodPrimitivesGLB = Object.values(floodPrimitivesGLB)
  //   console.log(floodPrimitivesGLB.forEach((item) => console.log(item.name)))
  //   console.log('全部加载完成 : ' + floodPrimitivesGLB.length)
  //   // floodPrimitivesGLB.forEach((primitive) =>primitive.show = false);
  // }

  // const subcontentFilePath = `@/../python/flood/30years/glb/subcontent.txt`
  // const response = await fetch(subcontentFilePath)
  // const data = await response.text()
  // const subcontent = data.split('\n').map(parseFloat)
  // renderTilesetWithAnimationGLB(subcontent)

  // const cesiumCanvas = await document.querySelector('#cesiumContainer canvas')
  // console.log(cesiumCanvas)
  // const ctx = await cesiumCanvas.getContext('2d')
  // cesiumCanvas.addEventListener('click', function (event) {
  //   const x = event.clientX
  //   const y = event.clientY

  //   const pixelData = ctx.getImageData(x, y, 1, 1).data

  //   const red = pixelData[0]
  //   const green = pixelData[1]
  //   const blue = pixelData[2]

  //   console.log(`点击位置的颜色为: RGB(${red}, ${green}, ${blue})`)
  // })
  // viewer.canvas.addEventListener('click', function (event) {
  //   const x = event.clientX
  //   const y = event.clientY

  //   const pickedObject = viewer.scene.pick(new Cesium.Cartesian2(x, y)) // 使用pick方法获取选中的对象

  //   if (Cesium.defined(pickedObject)) {
  //     const color = pickedObject.color
  //     const red = Cesium.Color.floatToByte(color.red)
  //     const green = Cesium.Color.floatToByte(color.green)
  //     const blue = Cesium.Color.floatToByte(color.blue)

  //     console.log(`点击位置的颜色为: RGB(${red}, ${green}, ${blue})`)
  //   }
  // })

  var scene = viewer.scene
  var context = scene.context

  var readColor = false
  var pickPosition = null // 定义 pickPosition 变量

  viewer.scene.camera.percentageChanged = 0.01 // 设置缩放触发阈值
  // 添加鼠标点击事件监听器
  viewer.canvas.addEventListener('click', function (event) {
    readColor = true
    var canvas = viewer.canvas
    var rect = canvas.getBoundingClientRect()
    console.log(rect)
    pickPosition = new Cesium.Cartesian2(
      event.clientX - rect.left,
      event.clientY - rect.top
    )
    console.log(pickPosition)
    var pickRay = viewer.scene.camera.getPickRay(pickPosition)

    var cartesian = viewer.scene.globe.pick(pickRay, viewer.scene)
    if (Cesium.defined(cartesian)) {
      var cartographic = Cesium.Cartographic.fromCartesian(cartesian)
      var longitude = Cesium.Math.toDegrees(cartographic.longitude)
      var latitude = Cesium.Math.toDegrees(cartographic.latitude)
      console.log('点击位置的经纬度坐标：' + longitude + ', ' + latitude)
    }
  })

  scene.postRender.addEventListener(function () {
    if (readColor && pickPosition !== null) {
      var pixels = context.readPixels({
        x: pickPosition.x,
        y: pickPosition.y,
        width: 1,
        height: 1
      })
      console.log('鼠标点击位置的颜色值:', pixels)
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
