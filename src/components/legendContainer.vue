<template>
  <div class="legend">
    <div v-for="(item, index) in legendData" :key="index" class="legend-item">
      <span
        class="legend-color"
        :style="{ backgroundColor: item.color }"
      ></span>
      <span class="legend-text">{{ item.text }}</span>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      colorData: ['#ff7f50', '#87cefa', '#da70d6', '#32cd32', '#6495ed'],
      textData: ['文字1', '文字2', '文字3', '文字4', '文字5'],
      legendData: []
    }
  },
  mounted() {
    this.generateLegendData()
  },
  methods: {
    generateLegendData() {
      this.legendData = this.colorData.map((color, index) => ({
        color: color,
        text: this.textData[index]
      }))
    }
  }
}
</script>

<style scoped>
.legend {
  display: flex;
  flex-direction: column;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.legend-color {
  width: 20px;
  height: 10px;
  border-radius: 2px;
  margin-right: 5px;
}

.legend-text {
  font-size: 14px;
}
</style>
