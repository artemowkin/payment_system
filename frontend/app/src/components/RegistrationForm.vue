<script setup lang="ts">
import { computed } from 'vue'
import { useForm } from 'vee-validate'
import type { UserIn } from '@/api/auth'
import FormField from './FormField.vue'
import Form from './Form.vue'
import { toTypedSchema } from '@vee-validate/yup'
import * as yup from 'yup'
import { RouterLink } from 'vue-router'

export interface Props {
    formError: string | null
}

export interface Emits {
    (e: 'submit', values: UserIn): void
}

const props = defineProps<Props>()

const emits = defineEmits<Emits>()

const { values, errors, defineInputBinds } = useForm({
    validationSchema: toTypedSchema(
        yup.object({
            email: yup.string().email('Введите правильный email').required('Введите email'),
            first_name: yup.string().required('Введите имя'),
            last_name: yup.string().required('Введите фамилию'),
            middle_name: yup.string(),
            password1: yup.string().matches(/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/g, "Пароль должен быть длиной больше 8 символов и содержать латинские буквы разных регистров и цифры").required('Введите пароль'),
            password2: yup.string().required('Повторите пароль').oneOf([yup.ref('password1'), null], "Пароли не совпадают")
        })
    )
})

const email = defineInputBinds('email')
const firstName = defineInputBinds('first_name')
const lastName = defineInputBinds('last_name')
const middleName = defineInputBinds('middle_name')
const password1 = defineInputBinds('password1')
const password2 = defineInputBinds('password2')

const isFormValid = computed<boolean>(() => {
    return Object.values(values).length && !Object.values(errors.value).length
})

const onSubmit = () => {
    if (!isFormValid.value) return

    emits('submit', values as UserIn)
}
</script>

<template>
    <Form submit-title="Зарегистрироваться" :form-error="formError" :is-form-valid="isFormValid" @submit="onSubmit">
        <template v-slot:title>
            <h1>Регистрация</h1>
        </template>
        <template v-slot:fields>
            <FormField>
                <input v-bind="email" placeholder="Email" />
                <div class="error">{{ errors.email }}</div>
            </FormField>
            <FormField>
                <input v-bind="firstName" placeholder="Имя" />
                <div class="error">{{ errors.first_name }}</div>
            </FormField>
            <FormField>
                <input v-bind="lastName" placeholder="Фамилия" />
                <div class="error">{{ errors.last_name }}</div>
            </FormField>
            <FormField>
                <input v-bind="middleName" placeholder="Отчество (не обязательно)" />
                <div class="error">{{ errors.middle_name }}</div>
            </FormField>
            <FormField>
                <input v-bind="password1" type="password" placeholder="Пароль" />
                <div class="error">{{ errors.password1 }}</div>
            </FormField>
            <FormField>
                <input v-bind="password2" type="password" placeholder="Повторите пароль" />
                <div class="error">{{ errors.password2 }}</div>
            </FormField>
        </template>
        <template v-slot:additional-links>
            <div class="additional_links">
                <RouterLink :to="{ name: 'login' }">Вход</RouterLink>
            </div>
        </template>
    </Form>
</template>

<style lang="scss" scoped>
form {
    display: grid;
    background: white;
    padding: 2rem;
    border-radius: .5rem;
    gap: 1rem;
    width: 30rem;

    .form_error {
        color: rgba(251, 92, 92, 0.632);
        padding-left: .5rem;
    }

    h1 {
        margin: 0;
        padding: 1rem 0;
    }

    .field {
        input {
            width: 100%;
            background-color: #89898915;
            border: 0;
            padding: .75rem;
            border-radius: .5rem;
        }

        .error {
            color: rgba(251, 92, 92, 0.632);
            padding: .5rem .5rem 0;
        }
    }

    button {
        width: fit-content;
        place-self: center;
        border: 0;
        padding: 1rem;
        border-radius: .5rem;
        cursor: pointer;
        color: white;
        background-color: #407bff;

        &.invalid {
            background-color: #6394ff;
        }
    }
}
</style>