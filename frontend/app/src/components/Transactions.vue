<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getTransactions } from '@/api/transactions'
import type { TransactionOut } from '@/api/transactions'
import TransactionsList from '@/components/TransactionsList.vue'
import TransactionInfo from './TransactionInfo.vue'
import PopUp from './PopUp.vue'

const transactions = ref<TransactionOut[]>([])

const currentTransaction = ref<TransactionOut | null>(null)

const showTransactionInfo = ref<boolean>(false)

const onTransactionClick = (transaction: TransactionOut) => {
    currentTransaction.value = transaction
    showTransactionInfo.value = true
}

onMounted(async () => {
    const token = localStorage.getItem('accessToken')

    transactions.value = await getTransactions(token as string)
})
</script>

<template>
    <div>
        <PopUp v-if="showTransactionInfo" @close="showTransactionInfo = false">
            <TransactionInfo :transaction="(currentTransaction as TransactionOut)" />
        </PopUp>
        <TransactionsList @click="onTransactionClick" :transactions="transactions" />
    </div>
</template>

<style lang="ts" scoped>
</style>