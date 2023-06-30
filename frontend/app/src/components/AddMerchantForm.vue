<script setup lang="ts">
import { computed } from 'vue'
import { useForm } from 'vee-validate'
import FormField from './FormField.vue'
import Form from './Form.vue'
import type { MerchantIn } from '@/api/merchants'
import { toTypedSchema } from '@vee-validate/yup'
import * as yup from 'yup'

export interface Emits {
    (e: 'submit', values: MerchantIn): void
}

export interface Props {
    formError: string | null
}

const emits = defineEmits<Emits>()

const props = defineProps<Props>()

const { values, errors, defineInputBinds } = useForm({
    validationSchema: toTypedSchema(
        yup.object({
            slug: yup.string().matches(/^[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*$/, 'Может содержать только латинские буквы, цифры и символ "-"').required('Введите название приложения')
        })
    )
})

const slug = defineInputBinds('slug')

const isFormValid = computed<boolean>(() => {
    return Object.values(values).length && !Object.values(errors.value).length
})

const onSubmit = () => {
    if (!isFormValid.value) return

    emits('submit', values as MerchantIn)
}
</script>

<template>
    <Form submit-title="Создать" :form-error="props.formError" :is-form-valid="isFormValid" @submit="onSubmit">
        <template v-slot:title>
            <h1>Создание приложения</h1>
        </template>
        <template v-slot:fields>
            <FormField>
                <input v-bind="slug" placeholder="Название приложения" />
                <div class="error">{{ errors.slug }}</div>
            </FormField>
        </template>
    </form>
</template>

<style lang="scss" scoped>
</style>