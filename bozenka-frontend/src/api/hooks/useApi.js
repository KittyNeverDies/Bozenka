// src/hooks/useApi.js
import {useCallback} from 'react';
import {useAuth} from '../context/AuthContext';
import BaseClientAPI from '../api/BaseClientAPI.js';

export const useApi = () => {
    const { accessToken, refreshToken, updateTokens, logout } = useAuth();
    const apiClient = new BaseClientAPI();

    const handleRequest = useCallback(async (requestFunc) => {
        try {
            // First attempt with current access token
            console.log("Trying to make request")
            return await requestFunc(accessToken);
        } catch (error) {
            console.log("log out")
            logout();
            if (error.message === 'Request failed with status 401' && refreshToken) {
                try {
                    // Try to refresh the token
                    const newTokens = await apiClient.refreshAuthToken(refreshToken);
                    updateTokens(newTokens.access_token, newTokens.refresh_token);

                    // Retry the request with new token
                    return await requestFunc(newTokens.access_token);
                } catch (refreshError) {
                    // If refresh fails, log out the user
                    logout();
                    throw new Error('Session expired. Please login again.');
                }
            }

            throw error;
        }
    }, [accessToken, refreshToken, updateTokens, logout]);

    const makeAuthenticatedRequest = useCallback(async (endpoint, options = {}) => {
        return handleRequest(token => (apiClient.makeRequest(endpoint, token, options))
        );
    }, [handleRequest]);

    // Wrap API methods with authentication
    const api = {
        login: apiClient.login.bind(apiClient),
        register: apiClient.register.bind(apiClient),
        getPrivateCommunities: () =>
            makeAuthenticatedRequest('/private/communities/'),
        getPrivateCommunity: (communityId) =>
            makeAuthenticatedRequest(`/private/communities/${communityId}/`),
        updateCommunityBaseInformation: (communityId, updatedData) =>
            makeAuthenticatedRequest(
                `/private/communities/${communityId}/update/base`,
                {
                    method: 'POST',
                    body: JSON.stringify({ updated_data: updatedData })
                }
            ),
        deleteCommunity: (communityId) =>
            makeAuthenticatedRequest(
                `/private/communities/${communityId}/delete_community/`,
                { method: 'GET' }
            ),
        getAccountInfo: () => makeAuthenticatedRequest(
            '/private/user/account/',
            { method: 'GET' }
        ),
        updateAccountInfo: (updatedData) =>
            makeAuthenticatedRequest(
                '/private/user/account/update',
                {
                    method: 'POST',
                    body: JSON.stringify({updatedData: updatedData})
                }
            )
        // Add other API methods as needed
    };

    return api;
};