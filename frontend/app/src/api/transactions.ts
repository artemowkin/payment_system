import type { MerchantOut } from "./merchants"

export interface TransactionOut {
    type: string
    amount: number
    currency: string
    redirect_url: string
    uuid: string
    status: string
    merchant: MerchantOut
    card_info: string | null
}

export interface AnonymousTransaction {
    type: string
    amount: number
    currency: string
}

export interface CardInfo {
    card_code: string
    date: string
    cvv: string
}

export interface RedirectResponse {
    redirect_url: string
}

export const getTransactions = async (token: string): Promise<TransactionOut[]> => {
    const response = await fetch('/api/transactions/', {
        headers: { Authorization: `Bearer ${token}` }
    })

    if (!response.ok) return []

    const responseJson = await response.json()

    return responseJson as TransactionOut[]
}

export const getAnonymous = async (key: string): Promise<AnonymousTransaction | { detail: string }> => {
    const response = await fetch(`/api/transactions/anonymous/${key}`)

    const responseJson = await response.json()

    if (!response.ok) {
        return responseJson as { detail: string }
    }

    return responseJson as AnonymousTransaction
}

export const applyAnonymous = async (key: string, cardInfo: CardInfo): Promise<RedirectResponse | { detail: string }> => {
    const response = await fetch(`/api/transactions/apply/${key}`, {
        body: JSON.stringify(cardInfo),
        headers: { 'Content-Type': 'application/json' },
        method: 'POST'
    })

    const responseJson = await response.json()

    if (!response.ok) {
        return responseJson as { detail: string }
    }

    return responseJson as RedirectResponse
}