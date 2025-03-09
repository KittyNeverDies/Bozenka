
// src/utils/tokenManager.js
import { AES, enc } from 'crypto-js';

const STORAGE_KEY = 'auth_state';
const ENCRYPTION_KEY = process.env.REACT_APP_ENCRYPTION_KEY || 'default-key-change-in-prod';

export class TokenManager {
    static encryptData(data) {
        return AES.encrypt(JSON.stringify(data), ENCRYPTION_KEY).toString();
    }

    static decryptData(encryptedData) {
        try {
            const bytes = AES.decrypt(encryptedData, ENCRYPTION_KEY);
            return JSON.parse(bytes.toString(enc.Utf8));
        } catch {
            return null;
        }
    }

    static getTokens() {
        try {
            const encryptedData = localStorage.getItem(STORAGE_KEY);
            if (!encryptedData) return null;
            
            return this.decryptData(encryptedData);
        } catch {
            return null;
        }
    }

    static setTokens(accessToken, refreshToken) {
        const data = { accessToken, refreshToken, timestamp: Date.now() };
        const encryptedData = this.encryptData(data);
        localStorage.setItem(STORAGE_KEY, encryptedData);
    }

    static clearTokens() {
        localStorage.removeItem(STORAGE_KEY);
    }

    static isTokenExpired(token) {
        if (!token) return true;
        
        try {
            const payload = JSON.parse(atob(token.split(".")[1]));
            return payload.exp < Date.now() / 1000;
        } catch {
            return true;
        }
    }
}

// Example usage in AuthContext
export const useTokenManager = () => {
    const getStoredTokens = () => TokenManager.getTokens();
    const storeTokens = (accessToken, refreshToken) => TokenManager.setTokens(accessToken, refreshToken);
    const clearStoredTokens = () => TokenManager.clearTokens();
    const checkTokenExpiration = (token) => TokenManager.isTokenExpired(token);

    return {
        getStoredTokens,
        storeTokens,
        clearStoredTokens,
        checkTokenExpiration
    };
};
