<script setup lang="ts">
interface Emits {
    (e: 'click'): void
}

const emits = defineEmits<Emits>()
</script>

<template>
    <button @click="emits('click')">+ Добавить</button>
</template>

<style lang="scss" scoped>
button {
    background-color: #407bff;
    padding: 1rem;
    border-radius: 1rem;
    color: white;
    border: 0;
    cursor: pointer;
    width: fit-content;

    &:hover {
        background-color: #6394ff;
    }
}
</style>