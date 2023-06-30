export interface BaseUser {
    email: string
    first_name: string
    last_name: string
    middle_name: string | null
}

export interface User extends BaseUser {
    uuid: string
}

export interface UserIn extends BaseUser {
    password1: string
    password2: string
}

export interface UserLogin {
    email: string
    password: string
}

export interface TokenPair {
    access_token: string
    refresh_token: string
}

export const getMe = async (token: string): Promise<User | null> => {
    const response = await fetch('/api/auth/me/', {
        headers: { Authorization: `Bearer ${token}` }
    })

    if (!response.ok) {
        return null
    } else {
        const responseJson = await response.json()
        return responseJson as User
    }
}

export const refresh = async (token: string | null): Promise<TokenPair | null> => {
    const response = await fetch('/api/auth/refresh/', {
        headers: { Authorization: `Bearer ${token}` },
        method: 'POST'
    })

    if (!response.ok) {
        return null
    } else {
        const responseJson = await response.json()
        return responseJson as TokenPair
    }
}

export const registration = async (data: UserIn): Promise<TokenPair | { detail: string }> => {
    const response = await fetch('/api/auth/registration/', {
        body: JSON.stringify(data),
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })

    const responseJson = await response.json()

    if (!response.ok) {
        return responseJson as { detail: string }
    } else {
        return responseJson as TokenPair
    }
}

export const login = async (data: UserLogin): Promise<TokenPair | { detail: string }> => {
    const response = await fetch('/api/auth/login/', {
        body: JSON.stringify(data),
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })

    const responseJson = await response.json()

    if (!response.ok) {
        return responseJson as { detail: string }
    } else {
        return responseJson as TokenPair
    }
}