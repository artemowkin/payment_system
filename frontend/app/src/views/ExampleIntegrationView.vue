<script setup lang="ts">
const buy = async () => {
    const data = {
        "type": 'deposit',
        "amount": 69990,
        "currency": 'RUB',
        "redirect_url": 'http://localhost:8080/example_integration',
        "merchant_id": 'ed30802e-4bf9-4a80-8c38-61ea8ac0432d',
        "public_key": 'fcfa5c728ee45fdcc794c9ce4b5dae8f47761910',
    }

    data['signature'] = '7a31930a07d3fca29761e48c702b783f0a791fd1e2cca15cfb92bed338e78b78'

    const response = await fetch('/api/transactions/', {
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
        method: 'POST'
    })

    const responseJson = await response.json()

    location.replace(responseJson.payment_url)
}
</script>

<template>
    <div class="container">
        <div class="item">
            <img src="https://prostoreshop.ru/wp-content/uploads/2022/05/smartfon-apple-iphone-11-64gb-global-chernyj-7.jpg" />
            <div class="title">IPhone 11</div>
            <div class="price">69990 ₽</div>
        </div>
        <button @click="buy" class="buy_button">Купить</button>
    </div>
</template>

<style lang="scss" scoped>
.container {
    width: 100%;
    height: 100vh;
    display: grid;
    place-content: center;
    gap: 2rem;

    .item {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        place-items: center;
        background-color: white;
        overflow: hidden;
        border-radius: 2rem;
        padding: 1rem;

        img {
            width: 100px;
        }
    }

    button {
        background-color: #407bff;
        color: white;
        border: 0;
        width: fit-content;
        padding: 1rem;
        border-radius: 1rem;
        place-self: center;
        cursor: pointer;
    }
}
</style>