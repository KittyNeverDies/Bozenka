/**
 * Class representing a Community API client.
 */
class CommunityApiClient {
    /**
     * Create a CommunityApiClient.
     * @param {string} [baseUrl='http://localhost:8000'] - The base URL for the API.
     * @param {boolean} [useMockData=false] - Whether to use mock data for testing.
     */
    constructor(baseUrl = 'http://localhost:8000', useMockData = false) {
        // Basic data
        this.baseUrl = baseUrl;
        this.useMockData = useMockData;
        this.refreshToken = null;

        // Rate limiting
        this.requestCount = 0;
        this.requestLimit = 100;
        this.requestResetTime = Date.now() + 60000; // 1 minute window
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
            throw error;
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
            throw error;
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
                body: JSON.stringify({
                    refresh: refreshToken
                })
            });


            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Token refresh failed:', error);
            throw error;
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
     * @param {Object} [options={}] - The request options.
     * @param {number} [retryCount=3] - The number of times to retry the request.
     * @returns {Promise<Object>} - A promise that resolves to the response data.
     */
    async makeRequest(endpoint,  authToken = null, options = {}, retryCount = 3) {
        if (this.useMockData) {
            return this.getMockResponse(endpoint);
        }

        this.checkRateLimit();

        try {
            // Add authorization header if token exists
            const headers = {
                'Content-Type': 'application/json',
                ...(authToken && { 'Authorization': `Bearer ${authToken}` }),
                ...options.headers
            };

            const response = await fetch(`${this.baseUrl}${endpoint}`, {
                ...options,
                headers
            });

            // Handle 401 Unauthorized - Token expired
            if (response.status === 401 && retryCount > 0) {
                await this.refreshAuthToken();
                return this.makeRequest(endpoint, options, retryCount - 1);
            }

            if (!response.ok) {
                throw new Error(`Request failed with status ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            if (retryCount > 0) {
                return this.makeRequest(endpoint, options, retryCount - 1);
            }
            throw error;
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
            throw new Error('Community ID is required');
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
        return this.makeRequest(`/private/communities/${communityId}/update_community_base_information/`, authToken, {
            method: 'POST',
            body: JSON.stringify({ updated_data: updatedData })
        });
    }

    /**
     * Delete a community.
     * @param {number} communityId - The ID of the community.
     * @param {string} authToken - Token for authorization
     * @returns {Promise<Object>} - A promise that resolves to the response data.
     */
    async deleteCommunity(communityId, authToken) {
        return this.makeRequest(`/private/communities/${communityId}/delete_community/`, authToken, {
            method: 'GET'
        });
    }
}

export default CommunityApiClient;
