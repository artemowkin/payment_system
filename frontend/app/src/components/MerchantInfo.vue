<script setup lang="ts">
import type { MerchantOut } from '@/api/merchants'

export interface Props {
    merchant: MerchantOut
}

const props = defineProps<Props>()

const copyToClipboard = (value: string) => {
    navigator.clipboard.writeText(value)
}
</script>

<template>
    <content>
        <h2>{{ props.merchant.slug }}</h2>
        <div class="key_container">
            <div class="key_label">Merchant GUID:</div>
            <div class="key_value_container">
                <div class="key">{{ props.merchant.uuid }}</div>
                <div class="copy_button" @click="copyToClipboard(props.merchant.uuid)">copy</div>
            </div>
        </div>
        <div class="key_container">
            <div class="key_label">Public key:</div>
            <div class="key_value_container">
                <div class="key">{{ props.merchant.public_key.slice(0, 25) }}...</div>
                <div class="copy_button" @click="copyToClipboard(props.merchant.public_key)">copy</div>
            </div>
        </div>
        <div class="key_container">
            <div class="key_label">Private key:</div>
            <div class="key_value_container">
                <div class="key">{{ props.merchant.private_key.slice(0, 25) }}...</div>
                <div class="copy_button" @click="copyToClipboard(props.merchant.private_key)">copy</div>
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