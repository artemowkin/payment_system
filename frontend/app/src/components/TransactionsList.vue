<script setup lang="ts">
import type { TransactionOut } from '@/api/transactions'
import TransactionsListItem from '@/components/TransactionsListItem.vue'

export interface Props {
    transactions: TransactionOut[]
}

export interface Emits {
    (e: 'click', transaction: TransactionOut): void
}

const props = defineProps<Props>()

const emits = defineEmits<Emits>()
</script>

<template>
    <div v-if="props.transactions.length" class="transactions_list">
        <div class="header_row">
            <div>Тип</div>
            <div>Статус</div>
            <div>Сумма</div>
            <div>Валюта</div>
            <div>Приложение</div>
            <div>Время</div>
        </div>
        <TransactionsListItem :transaction="transaction" @click="(transaction: TransactionOut) => emits('click', transaction)" v-for="transaction in props.transactions" :key="transaction.uuid" />
    </div>
    <div v-else class="no_transactions_message">У вас пока нет транзакций. Интегрируйте нашу систему на ваш сайт и увидете здесь транзакции</div>
</template>

<style lang="scss" scoped>
.transactions_list {
    display: grid;
    gap: 1rem;

    .header_row {
        padding: 0 .75rem .5rem;
        display: grid;
        grid-template-columns: repeat(6, 1fr);
    }
}

.no_transactions_message {
    text-align: center;
}
</style>