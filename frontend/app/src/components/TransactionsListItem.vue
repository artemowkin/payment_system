<script setup lang="ts">
import { computed } from 'vue'
import type { TransactionOut } from '@/api/transactions'

export interface Props {
    transaction: TransactionOut
}

export interface Emits {
    (e: 'click', transaction: TransactionOut): void
}

const props = defineProps<Props>()

const emits = defineEmits<Emits>()

const transactionStatusColor = computed<string>(() => {
    const statusesColors = {
        completed: 'green',
        failed: 'red',
        pending: 'orange',
        created: 'black'
    }

    return statusesColors[props.transaction.status]
})
</script>

<template>
    <div class="transaction" @click="emits('click', props.transaction)">
        <div class="transaction_type">{{ props.transaction.type }}</div>
        <div class="transaction_status" :style="{ color: transactionStatusColor }">{{ props.transaction.status }}</div>
        <div class="transaction_amount">{{ props.transaction.amount }}</div>
        <div class="transaction_currency">{{ props.transaction.currency }}</div>
        <div class="transaction_merchant">{{ props.transaction.merchant.slug }}</div>
        <div class="transaction_datetime" :title="new Date(props.transaction.datetime).toLocaleString('ru')">
            {{ new Date(props.transaction.datetime).toLocaleTimeString('ru') }}
        </div>
    </div>
</template>

<style lang="scss" scoped>
.transaction {
    cursor: pointer;
    padding: 1rem;
    border-radius: .5rem;
    box-shadow: 0px 0px 10px 2px rgba(34, 60, 80, 0.05);
    display: grid;
    grid-template-columns: repeat(6, 1fr);
}
</style>