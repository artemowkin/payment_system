<script setup lang="ts">
export interface Emits {
    (e: 'close'): void
}

const emits = defineEmits<Emits>()
</script>

<template>
    <div class="popup_container">
        <div class="popup_background_close" @click="emits('close')"></div>
        <slot></slot>
    </div>
</template>

<style lang="scss" scoped>
.popup_container {
    background-color: rgba(0, 0, 0, .5);
    position: fixed;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    display: grid;
    place-content: center;
    z-index: 10000;

    .popup_background_close {
        position: absolute;
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
        z-index: -1;
    }
}
</style>