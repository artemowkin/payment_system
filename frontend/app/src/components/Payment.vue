<script setup lang="ts">
import { computed } from 'vue'
import Form from '@/components/Form.vue'
import FormField from '@/components/FormField.vue'
import type { CardInfo, AnonymousTransaction } from '@/api/transactions'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/yup'
import * as yup from 'yup'

export interface Props {
    transaction: AnonymousTransaction
    formError: string | null
}

export interface Emits {
    (e: 'submit', card_info: CardInfo): void
}

const props = defineProps<Props>()

const emits = defineEmits<Emits>()

const submitTitle = computed(() => {
    return `Оплатить ${props.transaction.amount} ${props.transaction.currency}`
})

const { values, errors, defineInputBinds } = useForm({
    validationSchema: toTypedSchema(
        yup.object({
            card_code: yup.string().matches(/^\d{4} ?\d{4} ?\d{4} ?\d{4}$/g, 'Введите правильный номер карты').required('Введите номер карты'),
            date: yup.string().matches(/^\d{2}\/\d{2}$/g, 'Введите дату в формате MM/YY').required('Введите срок окончания действия карты'),
            cvv: yup.string().matches(/^\d{3,4}$/g, "Введите правильный cvv").required('Введите cvv')
        })
    )
})

const card_code = defineInputBinds('card_code')
const date = defineInputBinds('date')
const cvv = defineInputBinds('cvv')

const isFormValid = computed<boolean>(() => {
    return Object.values(values).length && !Object.values(errors.value).length
})

const onSubmit = () => {
    if (!isFormValid.value) return

    emits('submit', values as CardInfo)
}
</script>

<template>
    <div class="container">
        <Form :form-error="props.formError" :is-form-valid="isFormValid" :submit-title="submitTitle" @submit="onSubmit">
            <template v-slot:title>
                <h1>Оплата покупки</h1>
            </template>
            <template v-slot:fields>
                <FormField>
                    <input v-bind="card_code" type="text" placeholder="Номер карты" />
                    <div class="error">{{ errors.card_code }}</div>
                </FormField>
                <FormField>
                    <input v-bind="date" type="text" placeholder="Годна до" />
                    <div class="error">{{ errors.date }}</div>
                </FormField>
                <FormField>
                    <input v-bind="cvv" type="password" placeholder="CVV" />
                    <div class="error">{{ errors.cvv }}</div>
                </FormField>
            </template>
        </Form>
    </div>
</template>

<style lang="scss">
.container {
    width: 100%;
    height: 100vh;
    display: grid;
    place-content: center;

    h1 {
        text-align: center;
    }
}
</style>