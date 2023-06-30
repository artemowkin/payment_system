<script setup lang="ts">
import Navigation from '@/components/Navigation.vue'
import Merchants from '@/components/Merchants.vue'
import MainContent from '@/components/MainContent.vue'
</script>

<template>
  <MainContent title="Активные приложения">
    <template v-slot:navigator>
      <Navigation current="merchants" />
    </template>
    <template v-slot:content>
      <Merchants />
    </template>
  </MainContent>
</template>

<style lang="scss" scoped>
</style>
