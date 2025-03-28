/**
 * Class representing a Community API client.
 */
class BaseClientAPI {
    /**
     * Create a CommunityApiClient.
     * @param {string} [baseUrl='http://localhost:8000'] - The base URL for the API.
     * @param {boolean} [useMockData=false] - Whether to use mock data for testing.
     */
    constructor(baseUrl = import.meta.env.REACT_APP_API_URL || 'http://localhost:8000',
                useMockData = false) {
        this.baseUrl = baseUrl;
        this.useMockData = useMockData;

        // Rate limiting
        this.requestCount = 0;
        this.requestLimit = 100;
        this.requestResetTime = Date.now() + 60000;
    }

    /**
     * Log in to the API.
     * @param {string} username - The username.
     * @param {string} password - The password.
     * @returns {Promise<Object>} - A promise that resolves to an object with a success property.
     */
    async login(username, password) {
        if (this.useMockData) {
            return { success: true };
        }

        try {
            const response = await fetch(`${this.baseUrl}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });

            if (!response.ok) {
                throw new Error('Login failed');
            }

            const data = await response.json();
            return {
                success: true,
                message: data.message,
                access_token: data.access_token,
                refresh_token: data.refresh_token
            };
        } catch (error) {
            console.error('Login failed:', error);
            return { error: error.message };
        }
    }

    /**
     * Register a new user.
     * @param {string} username - The username.
     * @param {string} email - The email.
     * @param {string} password - The password.
     * @returns {Promise<Object>} - A promise that resolves to an object with a success property.
     */
    async register(username, email, password) {
        if (this.useMockData) {
            return { success: true };
        }

        try {
            const response = await fetch(`${this.baseUrl}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, email, password })
            });

            if (!response.ok) {
                throw new Error('Registration failed');
            }

            const data = await response.json();
            return {
                success: true,
                message: data.message,
                access_token: data.access_token,
                refresh_token: data.refresh_token
            };
        } catch (error) {
            console.error('Registration failed:', error);
            return { error: error.message };
        }
    }

    /**
     * Refresh the authentication token.
     */
    async refreshAuthToken(refreshToken) {
        if (this.useMockData) {
            return {};
        }

        try {
            const response = await fetch(`${this.baseUrl}/api/token/refresh/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ refresh: refreshToken })
            });

            return await response.json();
        } catch (error) {
            console.error('Token refresh failed:', error);
            return { error: error.message };
        }
    }

    /**
     * Check if the rate limit has been exceeded.
     */
    checkRateLimit() {
        const now = Date.now();
        if (now > this.requestResetTime) {
            this.requestCount = 0;
            this.requestResetTime = now + 60000;
        }

        if (this.requestCount >= this.requestLimit) {
            throw new Error('Rate limit exceeded');
        }

        this.requestCount++;
    }

    /**
     * Make a request to the API.
     * @param {string} endpoint - The API endpoint.
     * @param {string} [authToken=null] - Authorization token
     * @param {Object} [options={}] - The request options.
     * @returns {Promise<Object>} - A promise that resolves to the response data.
     */
    async makeRequest(endpoint, authToken = null, options = {}) {
        if (this.useMockData) {
            return this.getMockResponse(endpoint);
        }

        try {
            this.checkRateLimit();

            const headers = {
                'Content-Type': 'application/json',
                ...(authToken && { 'Authorization': `Bearer ${authToken}` }),
                ...options.headers
            };

            const response = await fetch(`${this.baseUrl}${endpoint}`, {
                ...options,
                headers
            });

            if (!response.ok) {
                throw new Error(`Request failed with status ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Request failed:', error);
            return { error: error.message };
        }
    }

    /**
     * Get a list of communities.
     * @returns {Promise<Object>} - A promise that resolves to the response data.
     */
    async getCommunities() {
        return this.makeRequest('/communities/');
    }

    /**
     * Get a community by ID.
     * @param {number} communityId - The ID of the community.
     * @returns {Promise<Object>} - A promise that resolves to the response data.
     */
    async getCommunity(communityId) {
        if (!communityId) {
            return { error: 'Community ID is required' };
        }
        return this.makeRequest(`/communities/${communityId}/`);
    }

    /**
     * Get a list of tags.
     * @returns {Promise<Object>} - A promise that resolves to the response data.
     */
    async getTags() {
        return this.makeRequest('/tags/');
    }

    /**
     * Get a list of private communities.
     * @param {string} authToken - Token for authorization
     * @returns {Promise<Object>} - A promise that resolves to the response data.
     */
    async getPrivateCommunities(authToken) {
        return this.makeRequest('/private/communities/', authToken, {
            method: 'GET'
        });
    }

    /**
     * Update the base information of a community.
     * @param {number} communityId - The ID of the community.
     * @param {Object} updatedData - The updated data.
     * @param {string} authToken - Token for authorization
     * @returns {Promise<Object>} - A promise that resolves to the response data.
     */
    async updateCommunityBaseInformation(communityId, updatedData, authToken) {
        return this.makeRequest(
            `/private/communities/${communityId}/update_community_base_information/`,
            authToken,
            {
                method: 'POST',
                body: JSON.stringify({ updated_data: updatedData })
            }
        );
    }

    /**
     * Delete a community.
     * @param {number} communityId - The ID of the community.
     * @param {string} authToken - Token for authorization
     * @returns {Promise<Object>} - A promise that resolves to the response data.
     */
    async deleteCommunity(communityId, authToken) {
        return this.makeRequest(
            `/private/communities/${communityId}/delete_community/`,
            authToken,
            { method: 'GET' }
        );
    }
}

export default BaseClientAPI;