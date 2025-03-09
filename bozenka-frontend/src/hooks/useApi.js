
// src/hooks/useApi.js
import { useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import CommunityApiClient from '../api/CommunityApiClient';

export const useApi = () => {
    const { accessToken, refreshToken, updateTokens, logout } = useAuth();
    const apiClient = new CommunityApiClient();

    const handleRequest = useCallback(async (requestFunc) => {
        try {
            // First attempt with current access token
            const response = await requestFunc(accessToken);
            return response;
        } catch (error) {
            if (error.message === 'Token expired' && refreshToken) {
                try {
                    // Try to refresh the token
                    const newTokens = await apiClient.refreshAuthToken(refreshToken);
                    updateTokens(newTokens.access_token, newTokens.refresh_token);

                    // Retry the request with new token
                    const response = await requestFunc(newTokens.access_token);
                    return response;
                } catch (refreshError) {
                    // If refresh fails, log out the user
                    logout();
                    throw new Error('Session expired. Please login again.');
                }
            }
            throw error;
        }
    }, [accessToken, refreshToken, updateTokens, logout, apiClient]);

    const makeAuthenticatedRequest = useCallback(async (endpoint, options = {}) => {
        return handleRequest(token => 
            apiClient.makeRequest(endpoint, token, options)
        );
    }, [handleRequest, apiClient]);

    // Wrap API methods with authentication
    const api = {
        login: apiClient.login.bind(apiClient),
        register: apiClient.register.bind(apiClient),
        getPrivateCommunities: () => 
            makeAuthenticatedRequest('/private/communities/'),
        updateCommunityBaseInformation: (communityId, updatedData) => 
            makeAuthenticatedRequest(
                `/private/communities/${communityId}/update_community_base_information/`,
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
        // Add other API methods as needed
    };

    return api;
};
