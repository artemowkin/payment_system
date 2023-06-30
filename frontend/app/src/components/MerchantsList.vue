<script setup lang="ts">
import type { MerchantOut } from '@/api/merchants'
import MerchantsListItem from './MerchantsListItem.vue'

export interface Props {
    merchants: MerchantOut[]
}

export interface Emits {
    (e: 'click', merchant: MerchantOut): void
    (e: 'delete', merchant: MerchantOut): void
}

const props = defineProps<Props>()

const emits = defineEmits<Emits>()
</script>

<template>
    <div v-if="props.merchants.length" class="merchants_list">
        <MerchantsListItem
            @click="(merchant: MerchantOut) => emits('click', merchant)"
            @delete="(merchant: MerchantOut) => emits('delete', merchant)"
            :key="merchant.uuid"
            :merchant="merchant"
            v-for="merchant in props.merchants" />
    </div>
    <div v-else class="no_merchants_message">У вас еще нет приложений. Создайте ваше первое!</div>
</template>

<style lang="scss" scoped>
.merchants_list {
    display: grid;
    gap: 1rem;
}

.no_merchants_message {
    text-align: center;
}
</style>