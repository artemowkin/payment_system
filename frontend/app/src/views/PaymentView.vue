<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import type { AnonymousTransaction, CardInfo } from '@/api/transactions'
import { getAnonymous, applyAnonymous } from '@/api/transactions'
import Payment from '@/components/Payment.vue'

const route = useRoute()

const currentTransaction = ref<AnonymousTransaction | null>(null)

const errorMessage = ref<string | null>(null)

const formError = ref<string | null>(null)

const onSubmit = async (cardInfo: CardInfo) => {
    const result = await applyAnonymous(route.params.key, cardInfo)

    if ('detail' in result) {
        formError.value = result.detail
        return
    }

    location.replace(result.redirect_url)
}

onMounted(async () => {
    const transaction = await getAnonymous(route.params.key)

    if ('detail' in transaction) {
        errorMessage.value = transaction.detail
        return
    }

    currentTransaction.value = transaction
})
</script>

<template>
    <Payment v-if="currentTransaction" :transaction="currentTransaction" :form-error="formError" @submit="onSubmit" />
    <div v-else-if="errorMessage" class="error_message_container">
        <div class="error_message">{{ errorMessage }}</div>
    </div>
</template>

<style lang="scss" scoped>
.error_message_container {
    width: 100%;
    height: 100vh;
    display: grid;
    place-content: center;

    .error_message {
        color: red;
        background-color: rgba(255, 0, 0, 0.075);
        border: 2px solid red;
        padding: 2rem;
        border-radius: 1rem;
    }
}
</style>