<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import RegistrationForm from '@/components/RegistrationForm.vue'
import type { UserIn } from '@/api/auth'
import { registration } from '@/api/auth'

const formError = ref<string | null>(null)

const router = useRouter()

const onSubmit = async (userData: UserIn) => {
    const user = await registration(userData)

    if ('detail' in user) {
        formError.value = user.detail
    } else {
        localStorage.setItem('accessToken', user.access_token)
        localStorage.setItem('refreshToken', user.refresh_token)
        router.push({ name: 'merchants' })
    }
}
</script>

<template>
    <div class="background">
        <RegistrationForm :formError="formError" @submit="onSubmit" />
    </div>
</template>

<style lang="scss" scoped>
.background {
    background-image: url('@/assets/auth_background.svg');
    background-color: #f3f5fc;
    background-position: center right;
    background-size: 50%;
    background-repeat: no-repeat;
    position: fixed;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
    z-index: -1;

    display: grid;
    place-content: center start;
    padding-left: 4rem;
}
</style>