<template>
  <div id="echartsContainer"></div>
</template>

<script setup>
import * as echarts from 'echarts'
import { ref, onMounted, watchEffect } from 'vue'
import { useFloodStore } from '../stores/flood'
import { useStateStore } from '../stores/state'
const floodStore = useFloodStore()
const stateStore = useStateStore()

const initFlag = ref(false)
const updateEchartFlag = ref(true) // 初始值为true 避免visibility持久化为false
onMounted(async () => {
  // 基于准备好的dom，初始化echarts实例
  const myChart = echarts.init(document.getElementById('echartsContainer'))
  // 绘制图表
  watchEffect(() => {
    if (stateStore.visibility && updateEchartFlag.value) {
      updateEchartFlag.value = false
      // 启动定时器，每0.1秒调用一次 resize()
      const ID = setInterval(() => myChart.resize(), 10)
      // 一秒钟后停止定时器
      setTimeout(() => {
        clearInterval(ID) // 停止定时器
      }, 1000)
    }

    if (floodStore.initReady && !initFlag.value) {
      initFlag.value = true
      myChart.setOption({
        xAxis: {
          type: 'category'
          // data: ['A', 'B', 'C']
        },
        yAxis: {
          type: 'value',
          min: 60000 // 设置最小值
          // max: 180000 // 设置最大值
        },
        grid: {
          left: '55px', // 调整左边距
          right: '20px', // 调整右边距
          top: '20px', // 调整上边距
          bottom: '25px' // 调整下边距
        },
        series: [
          {
            data: floodStore.echartSeries,
            type: 'bar',
            smooth: true
          }
        ]
      })
    }

    if (initFlag.value) {
      const seriesIndex = floodStore.index - 1
      myChart.setOption({
        series: [
          {
            itemStyle: {
              color: function (params) {
                if (params.dataIndex === seriesIndex) {
                  return '#FF6347' // 设置被点击柱状图的颜色
                } else {
                  return params.color // 保持其他柱状图的颜色不变
                }
              }
            }
          }
        ]
      })
    }
  })

  // 设置响应式
  window.addEventListener('resize', () => {
    if (stateStore.visibility) {
      myChart.resize()
    } else {
      if (!stateStore.updateEchart) {
        updateEchartFlag.value = true // 在隐藏的情况下，屏幕动了设置 需要更重新新echarts的标志
      }
    }
  })

  myChart.on('click', function (params) {
    // 获取被点击柱状图的系列索引和数据索引
    var seriesIndex = params.seriesIndex
    var dataIndex = params.dataIndex
    floodStore.setIndex(dataIndex + 1)
    // 修改柱状图颜色
    myChart.setOption({
      series: [
        {
          itemStyle: {
            color: function (params) {
              if (
                params.seriesIndex === seriesIndex &&
                params.dataIndex === dataIndex
              ) {
                return '#FF6347' // 设置被点击柱状图的颜色
              } else {
                return params.color // 保持其他柱状图的颜色不变
              }
            }
          }
        }
      ]
    })
  })
})
</script>

<style>
#echartsContainer {
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
  overflow: hidden;
}
</style>
