<script setup lang="ts">
import { computed } from 'vue'
import { useForm } from 'vee-validate'
import type { UserLogin } from '@/api/auth'
import FormField from './FormField.vue'
import Form from './Form.vue'
import { toTypedSchema } from '@vee-validate/yup'
import * as yup from 'yup'
import { RouterLink } from 'vue-router'

export interface Props {
    formError: string | null
}

export interface Emits {
    (e: 'submit', values: UserLogin): void
}

const props = defineProps<Props>()

const emits = defineEmits<Emits>()

const { values, errors, defineInputBinds } = useForm({
    validationSchema: toTypedSchema(
        yup.object({
            email: yup.string().email('Введите правильный email').required('Введите email'),
            password: yup.string().required('Введите пароль')
        })
    )
})

const email = defineInputBinds('email')
const password = defineInputBinds('password')

const isFormValid = computed<boolean>(() => {
    return Object.values(values).length && !Object.values(errors.value).length
})

const onSubmit = () => {
    if (!isFormValid.value) return

    emits('submit', values as UserLogin)
}
</script>

<template>
    <Form submit-title="Войти" :form-error="formError" :is-form-valid="isFormValid" @submit="onSubmit">
        <template v-slot:title>
            <h1>Вход</h1>
        </template>
        <template v-slot:fields>
            <FormField>
                <input v-bind="email" placeholder="Email" />
                <div class="error">{{ errors.email }}</div>
            </FormField>
            <FormField>
                <input v-bind="password" type="password" placeholder="Повторите пароль" />
                <div class="error">{{ errors.password }}</div>
            </FormField>
        </template>
        <template v-slot:additional-links>
            <div class="additional_links">
                <RouterLink :to="{ name: 'registration' }">Регистрация</RouterLink>
            </div>
        </template>
    </Form>
</template>

<style lang="scss" scoped>
</style>