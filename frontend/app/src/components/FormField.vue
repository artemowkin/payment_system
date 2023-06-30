<script setup lang="ts">
</script>

<template>
    <div class="field">
        <slot></slot>
    </div>
</template>

<style lang="scss" scoped>
.field {
    :slotted(input) {
        width: 100%;
        background-color: #89898915;
        border: 0;
        padding: .75rem;
        border-radius: .5rem;
    }

    :slotted(.error) {
        color: rgba(251, 92, 92, 0.632);
        padding: .5rem .5rem 0;
    }
}
</style>