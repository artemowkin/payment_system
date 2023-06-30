<script setup lang="ts">
import Navigation from './Navigation.vue'

export interface Props {
    title: string
}

const props = defineProps<Props>()
</script>

<template>
    <div class="wrapper">
        <slot name="navigator"></slot>
        <content>
            <h1>{{ props.title }}</h1>
            <slot name="content"></slot>
        </content>
    </div>
</template>

<style lang="scss" scoped>
.wrapper {
  display: grid;
  grid-template-columns: minmax(min-content, max-content) 4fr;
  padding: 2rem;
  gap: 2rem;

  content {
    background: white;
    border-radius: 1rem;
    padding: 2rem;
    height: fit-content;
    display: grid;
    gap: 3rem;

    h1 {
        margin: 0;
        padding: 0;
    }
  }
}
</style>