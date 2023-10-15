<template>
  <div class="legend-container">
    <div class="legend" ref="legend">
      <div
        v-for="(item, index) in colorStore.legendItems"
        :key="index"
        class="legend-item"
      >
        <div class="color-box" :style="{ backgroundColor: item.color }"></div>
        <div class="label-text">{{ item.label }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useColorStore } from '@/stores/color'
const colorStore = useColorStore()
</script>

<style>
.legend-container {
  background-color: rgba(255, 255, 255, 0.7);
  padding: 20px;
  border: 1px solid #ccc;
  max-width: 180px;
}

.legend {
  color: #000;
  display: flex;
  flex-direction: column;
  font-size: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.color-box {
  width: 50px;
  height: 20px;
  border: 1px solid #000;
  margin-right: 10px;
}

.label-text {
  width: 80px;
  white-space: pre; /* 保留连续的空格 */
}
</style>
