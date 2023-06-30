<script setup lang="ts">
import type { TransactionOut } from '@/api/transactions'

export interface Props {
    transaction: TransactionOut
}

const props = defineProps<Props>()
</script>

<template>
    <content>
        <h2>{{ props.transaction.uuid }}</h2>
        <div class="key_container">
            <div class="key_label">Type:</div>
            <div class="key_value_container">
                <div class="key">{{ props.transaction.type }}</div>
            </div>
        </div>
        <div class="key_container">
            <div class="key_label">Amount:</div>
            <div class="key_value_container">
                <div class="key">{{ props.transaction.amount }}</div>
            </div>
        </div>
        <div class="key_container">
            <div class="key_label">Currency:</div>
            <div class="key_value_container">
                <div class="key">{{ props.transaction.currency }}</div>
            </div>
        </div>
        <div class="key_container">
            <div class="key_label">Redirect URL:</div>
            <div class="key_value_container">
                <div class="key">{{ props.transaction.redirect_url }}</div>
            </div>
        </div>
        <div class="key_container">
            <div class="key_label">Status:</div>
            <div class="key_value_container">
                <div class="key">{{ props.transaction.status }}</div>
            </div>
        </div>
        <div class="key_container">
            <div class="key_label">Merchant GUID:</div>
            <div class="key_value_container">
                <div class="key">{{ props.transaction.merchant.uuid }}</div>
            </div>
        </div>
        <div class="key_container">
            <div class="key_label">Merchant title:</div>
            <div class="key_value_container">
                <div class="key">{{ props.transaction.merchant.slug }}</div>
            </div>
        </div>
        <div v-if="props.transaction.card_info" class="key_container">
            <div class="key_label">Card number:</div>
            <div class="key_value_container">
                <div class="key">****{{ props.transaction.card_info }}</div>
            </div>
        </div>
        <div v-if="props.transaction.card_info" class="key_container">
            <div class="key_label">Creation datetime:</div>
            <div class="key_value_container">
                <div class="key">{{ new Date(props.transaction.datetime).toLocaleString('ru') }}</div>
            </div>
        </div>
    </content>
</template>

<style lang="scss" scoped>
content {
    padding: 2rem;
    border-radius: 1rem;
    background: white;
    display: grid;
    gap: 1rem;
    width: 100vw;
    max-width: max-content;

    h2 {
        margin: 0;
        padding: 0;
    }

    .key_container {
        display: grid;
        justify-content: flex-start;
        align-items: center;
        gap: 1rem;
        grid-template-columns: 1fr 3fr;

        .key_value_container {
            background-color: #6394ff25;
            border-radius: .5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;

            .key {
                padding: .5rem;
            }

            .copy_button {
                background-color: #407bff;
                padding: .5rem;
                border-radius: .5rem;
                color: white;
                cursor: pointer;
                margin-left: .5rem;
            }
        }
    }
}
</style>
