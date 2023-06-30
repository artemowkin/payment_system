<script setup lang="ts">
interface Props {
    formError: string | null
    isFormValid: boolean
    submitTitle: string
}

interface Emits {
    (e: 'submit'): void
}

const props = defineProps<Props>()

const emits = defineEmits<Emits>()
</script>

<template>
    <form @submit.prevent="emits('submit')">
        <slot name="title"></slot>
        <slot name="fields"></slot>
        <div v-if="props.formError" class="form_error">{{ props.formError }}</div>
        <button type="submit" :class="isFormValid ? '' : 'invalid'">{{ props.submitTitle }}</button>
        <slot name="additional-links"></slot>
    </form>
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

    :slotted(h1) {
        margin: 0;
        padding: 1rem 0;
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

    :slotted(.additional_links) {
        display: grid;
        place-content: center;

        a {
            color: #6394ff;
        }
    }
}
</style>