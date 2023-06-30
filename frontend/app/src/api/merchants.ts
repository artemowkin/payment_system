export interface MerchantOut {
    slug: string
    uuid: string
    public_key: string
    private_key: string
}

export interface MerchantIn {
    slug: string
}

export const getMerchants = async (token: string): Promise<MerchantOut[]> => {
    const response = await fetch('/api/merchants/', {
        headers: { Authorization: `Bearer ${token}` }
    })

    if (response.ok) {
        const responseJson = await response.json()
        return responseJson as MerchantOut[]
    }

    return []
}

export const createMerchant = async (token: string, merchantData: MerchantIn): Promise<MerchantOut | { detail: string }> => {
    const response = await fetch('/api/merchants/', {
        body: JSON.stringify(merchantData),
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
        method: 'POST'
    })

    const responseJson = await response.json()

    if (response.ok) {
        return responseJson as MerchantOut
    }

    return responseJson as { detail: string }
}

export const deleteMerchant = async (token: string, merchantUUID: string): Promise<null | { detail: string }> => {
    const response = await fetch(`/api/merchants/${merchantUUID}/`, {
        headers: { Authorization: `Bearer ${token}` },
        method: 'DELETE'
    })

    if (response.ok) {
        return null
    }

    const responseJson = await response.json()

    return responseJson as { detail: string }
}