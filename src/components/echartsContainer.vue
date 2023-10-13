<template>
  <div id="echartsContainer"></div>
</template>

<script setup>
import * as echarts from 'echarts'
import { onMounted, watchEffect } from 'vue'
import { useFloodStore } from '../stores/flood'
const floodStore = useFloodStore()
onMounted(async () => {
  // 基于准备好的dom，初始化echarts实例
  const myChart = echarts.init(document.getElementById('echartsContainer'))
  // 绘制图表
  myChart.setOption({
    xAxis: {
      type: 'category'
      // data: ['A', 'B', 'C']
    },
    yAxis: {
      type: 'value',
      min: 60000, // 设置最小值
      max: 160000 // 设置最大值
    },
    grid: {
      left: '55px', // 调整左边距
      right: '20px', // 调整右边距
      top: '20px', // 调整上边距
      bottom: '25px' // 调整下边距
    },
    series: [
      {
        data: [
          81594, 81387, 80785, 80698, 80331, 80099, 80093, 80000, 79860, 79833,
          79703, 79568, 79478, 79306, 79218, 79189, 79096, 79077, 78862, 78814,
          78828, 78722, 78704, 78718, 78691, 78587, 78544, 78589, 78395, 78277,
          78135, 78052, 78014, 78039, 77895, 77865, 77779, 77781, 77775, 77691,
          77613, 77622, 77484, 77475, 77318, 77332, 77311, 77252, 77147, 77105,
          77097, 76995, 76986, 76963, 76908, 76925, 76899, 76842, 76798, 76757,
          76769, 77896, 78091, 78267, 78328, 78395, 78487, 78802, 78830, 79016,
          79607, 79702, 80217, 80500, 80794, 81127, 81324, 81611, 81977, 82174,
          82369, 82490, 82665, 82905, 83064, 83253, 83613, 84125, 84958, 85316,
          85737, 86619, 88723, 89183, 91196, 92367, 93683, 94984, 95656, 96379,
          97039, 99907, 102396, 103199, 104115, 106139, 109314, 110402, 112468,
          114708, 115853, 117195, 118232, 121387, 122472, 124689, 125762,
          128958, 131276, 132511, 133338, 134483, 135558, 135848, 136396,
          138751, 139432, 139788, 141031, 141434, 141916, 142139, 142298,
          143493, 143663, 143544, 143825, 144440, 144429, 144390, 144604,
          144602, 144687, 144818, 144888, 144974, 144821, 144886, 144746,
          144858, 144826, 144839, 144731, 144737, 144512, 144611, 144319,
          144212, 143951, 143841, 143738, 143567, 143261, 143172, 142975,
          142941, 142863, 142725, 142540, 142270, 141905, 141777, 141644,
          141574, 141419
        ],
        type: 'bar',
        smooth: true
      }
    ]
  })

  // 设置响应式
  window.addEventListener('resize', () => {
    myChart.resize()
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

  watchEffect(() => {
    // 修改柱状图颜色
    // const dataIndex = 0
    const seriesIndex = floodStore.index - 1
    // const option = myChart.getOption() // 获取当前图表配置
    // const series = option.series[0]
    // console.log(series)
    // 修改柱状图颜色
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
