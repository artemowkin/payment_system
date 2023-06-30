<script setup lang="ts">
import type { MerchantOut } from '@/api/merchants'

export interface Props {
    merchant: MerchantOut
}

export interface Emits {
    (e: 'click', merchant: MerchantOut): void
    (e: 'delete', merchant: MerchantOut): void
}

const props = defineProps<Props>()

const emits = defineEmits<Emits>()
</script>

<template>
    <div class="merchant">
        <div class="merchant_title" @click="emits('click', props.merchant)">{{ props.merchant.slug }}</div>
        <div class="delete_button" @click="emits('delete', props.merchant)">Удалить</div>
    </div>
</template>

<style lang="scss" scoped>
.merchant {
    padding: 1rem;
    border-radius: .5rem;
    box-shadow: 0px 0px 10px 2px rgba(34, 60, 80, 0.05);
    display: flex;
    justify-content: space-between;
    align-items: center;

    .merchant_title {
        color: #6394ff;
        cursor: pointer;
    }

    .delete_button {
        color: red;
        font-size: .75rem;
        cursor: pointer;
        padding: .5rem;
        border-radius: .5rem;

        &:hover {
            background-color: rgba(255, 0, 0, .05);
        }
    }
}
</style>