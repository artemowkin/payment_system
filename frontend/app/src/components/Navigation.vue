<script setup lang="ts">
import { RouterLink, useRouter } from 'vue-router';

export interface Props {
    current: 'merchants' | 'transactions'
}

const props = defineProps<Props>()

const router = useRouter()

const logout = () => {
    localStorage.clear()
    router.push({ name: 'login' })
}
</script>

<template>
    <nav>
        <RouterLink :class="props.current == 'merchants' ? 'active' : ''" :to="{ name: 'merchants' }">Приложения</RouterLink>
        <RouterLink :class="props.current == 'transactions' ? 'active': ''" :to="{ name: 'transactions' }">Транзакции</RouterLink>
        <button class="logout_button" @click="logout">Выйти</button>
    </nav>
</template>

<style scoped lang="scss">
nav {
    padding: 1rem;
    background-color: white;
    border-radius: 1rem;
    width: 100%;
    height: fit-content;
    display: grid;
    gap: .5rem;
    padding: .5rem;
    position: sticky;
    top: 2rem;

    a, .logout_button {
        padding: .75rem;
        border-radius: 1rem;
        border: 3px solid transparent;

        &:hover {
            background-color: #9db9fc28;
        }

        &.active {
            background-color: #9db9fc28;
            border: 3px solid #9db9fc;
            pointer-events: none;
            color: #9db9fc;
        }
    }

    .logout_button {
        background-color: transparent;
        cursor: pointer;

        &:hover {
            background-color: rgba(255, 0, 0, 0.104);
            color: red;
        }
    }
}
</style>