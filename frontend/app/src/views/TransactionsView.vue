<script setup lang="ts">
import Transactions from '@/components/Transactions.vue'
import Navigation from '@/components/Navigation.vue'
import MainContent from '@/components/MainContent.vue'
</script>

<template>
    <MainContent title="Список транзакций">
        <template v-slot:navigator>
            <Navigation current="transactions" />
        </template>
        <template v-slot:content>
            <Transactions />
        </template>
    </MainContent>
</template>

<style lang="scss" scoped>
</style>