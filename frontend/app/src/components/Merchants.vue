<script setup lang="ts">
import { onMounted, ref } from 'vue'
import AddButton from './AddButton.vue'
import MerchantsList from './MerchantsList.vue'
import type { MerchantOut, MerchantIn } from '@/api/merchants'
import { getMerchants, createMerchant, deleteMerchant } from '@/api/merchants'
import PopUp from './PopUp.vue'
import AddMerchantForm from './AddMerchantForm.vue'
import MerchantInfo from './MerchantInfo.vue'

const merchants = ref<MerchantOut[]>([])

const showCreatePopUp = ref<boolean>(false)

const showMerchantPopUp = ref<boolean>(false)

const currentMerchant = ref<MerchantOut | null>(null)

const formError = ref<string | null>(null)

const onMerchantClick = (merchant: MerchantOut) => {
    currentMerchant.value = merchant
    showMerchantPopUp.value = true
}

const onSubmit = async (merchantData: MerchantIn) => {
    const token = localStorage.getItem('accessToken')

    const merchant = await createMerchant(token as string, merchantData)

    if ('detail' in merchant) {
        formError.value = merchant.detail
        return
    }

    showCreatePopUp.value = false

    const newMerchants = await getMerchants(token as string)

    merchants.value = newMerchants
}

const onMerchantDelete = async (merchant: MerchantOut) => {
    const token = localStorage.getItem('accessToken')

    await deleteMerchant(token as string, merchant.uuid)

    if ('detail' in merchant) {
        return
    }

    const newMerchants = await getMerchants(token as string)

    merchants.value = newMerchants
}

onMounted(async () => {
    const token = localStorage.getItem('accessToken')

    merchants.value = await getMerchants(token as string)
})
</script>

<template>
    <div class="merchants">
        <PopUp v-if="showCreatePopUp" @close="showCreatePopUp = false">
            <AddMerchantForm :form-error="formError" @submit="onSubmit" />
        </PopUp>
        <PopUp v-if="showMerchantPopUp" @close="showMerchantPopUp = false">
            <MerchantInfo :merchant="(currentMerchant as MerchantOut)" />
        </PopUp>
        <AddButton @click="showCreatePopUp = true" />
        <MerchantsList @click="onMerchantClick" @delete="onMerchantDelete" :merchants="merchants" />
    </div>
</template>

<style lang="scss" scoped>
.merchants {
    display: grid;
    gap: 2rem;
}
</style>