/**
 * API Service for TourJett Dashboard
 * Handles all interactions with the backend API
 */

// Base API URL - updated to work with Docker container
const API_BASE_URL = 'http://localhost:5000/api';

// API Error Handler
const handleApiError = (error) => {
    console.error('API Error:', error);
    // More detailed error logging for debugging
    if (error.response) {
        console.error('Response status:', error.response.status);
        console.error('Response data:', error.response.data);
    } else if (error.request) {
        console.error('No response received:', error.request);
    }
    
    // User-friendly error message
    alert('An error occurred while communicating with the server. Please try again.');
    return Promise.reject(error);
};

// Generic function to make API calls with better error handling
const apiCall = async (endpoint, method = 'GET', data = null) => {
    const url = `${API_BASE_URL}${endpoint}`;
    
    console.log(`Making API call to: ${url}`);
    
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include', // To include cookies for authentication
    };
    
    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }
    
    try {
        console.log('API request options:', options);
        const response = await fetch(url, options);
        
        if (!response.ok) {
            // Get more details about the error
            const errorText = await response.text();
            console.error(`HTTP error! Status: ${response.status}`, errorText);
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        // Try to parse as JSON, fallback to text if not JSON
        if (response.headers.get('content-type')?.includes('application/json')) {
            const data = await response.json();
            console.log('API response data:', data);
            return data;
        } else {
            const text = await response.text();
            console.log('API response text:', text);
            return text;
        }
    } catch (error) {
        return handleApiError(error);
    }
};

// API Service object with methods for each entity type
const ApiService = {
    // Authentication APIs
    auth: {
        login: (username, password) => apiCall('/auth/login', 'POST', { username, password }),
        logout: () => apiCall('/auth/logout', 'POST'),
        getCurrentUser: () => apiCall('/auth/me'),
    },
    
    // Tour APIs
    tours: {
        getAll: () => apiCall('/turlar'),
        getById: (id) => apiCall(`/turlar/${id}`),
        create: (tourData) => apiCall('/tur', 'POST', tourData),
        update: (id, tourData) => apiCall(`/tur/${id}`, 'PUT', tourData),
        delete: (id) => apiCall(`/tur/${id}`, 'DELETE'),
    },
    
    // Reservation APIs
    reservations: {
        getAll: () => apiCall('/rezervasyon'),
        getById: (id) => apiCall(`/rezervasyon/${id}`),
        create: (reservationData) => apiCall('/rezervasyon', 'POST', reservationData),
        update: (id, reservationData) => apiCall(`/rezervasyon/${id}`, 'PUT', reservationData),
        delete: (id) => apiCall(`/rezervasyon/${id}`, 'DELETE'),
    },
    
    // Customer APIs
    customers: {
        getAll: () => apiCall('/musteri'),
        getById: (id) => apiCall(`/musteri/${id}`),
        create: (customerData) => apiCall('/musteri', 'POST', customerData),
        update: (id, customerData) => apiCall(`/musteri/${id}`, 'PUT', customerData),
        delete: (id) => apiCall(`/musteri/${id}`, 'DELETE'),
    },
    
    // Region APIs
    regions: {
        getAll: () => apiCall('/bolge'),
        getById: (id) => apiCall(`/bolge/${id}`),
    },
    
    // Destination APIs
    destinations: {
        getAll: () => apiCall('/destinasyon'),
        getById: (id) => apiCall(`/destinasyon/${id}`),
        create: (destinationData) => apiCall('/destinasyon', 'POST', destinationData),
        update: (id, destinationData) => apiCall(`/destinasyon/${id}`, 'PUT', destinationData),
        delete: (id) => apiCall(`/destinasyon/${id}`, 'DELETE'),
    },
    
    // Resource APIs
    resources: {
        // Guide APIs
        guides: {
            getAll: () => apiCall('/kaynak/rehber'),
            getById: (id) => apiCall(`/kaynak/rehber/${id}`),
            create: (guideData) => apiCall('/kaynak/rehber', 'POST', guideData),
            update: (id, guideData) => apiCall(`/kaynak/rehber/${id}`, 'PUT', guideData),
            delete: (id) => apiCall(`/kaynak/rehber/${id}`, 'DELETE'),
        },
        
        // Driver APIs
        drivers: {
            getAll: () => apiCall('/kaynak/sofor'),
            getById: (id) => apiCall(`/kaynak/sofor/${id}`),
            create: (driverData) => apiCall('/kaynak/sofor', 'POST', driverData),
            update: (id, driverData) => apiCall(`/kaynak/sofor/${id}`, 'PUT', driverData),
            delete: (id) => apiCall(`/kaynak/sofor/${id}`, 'DELETE'),
        },
        
        // Vehicle APIs
        vehicles: {
            getAll: () => apiCall('/kaynak/arac'),
            getById: (id) => apiCall(`/kaynak/arac/${id}`),
            create: (vehicleData) => apiCall('/kaynak/arac', 'POST', vehicleData),
            update: (id, vehicleData) => apiCall(`/kaynak/arac/${id}`, 'PUT', vehicleData),
            delete: (id) => apiCall(`/kaynak/arac/${id}`, 'DELETE'),
        },
    },
    
    // Review APIs
    reviews: {
        getAll: () => apiCall('/degerlendirme'),
        getById: (id) => apiCall(`/degerlendirme/${id}`),
        create: (reviewData) => apiCall('/degerlendirme', 'POST', reviewData),
        update: (id, reviewData) => apiCall(`/degerlendirme/${id}`, 'PUT', reviewData),
        delete: (id) => apiCall(`/degerlendirme/${id}`, 'DELETE'),
    },
    
    // Dashboard Statistics APIs
    dashboard: {
        getStats: () => apiCall('/dashboard/stats'),
        getRecentBookings: () => apiCall('/dashboard/recent-bookings'),
        getUpcomingTours: () => apiCall('/dashboard/upcoming-tours'),
        getRevenueData: () => apiCall('/dashboard/revenue'),
    },
};

// Export the API Service
// This will make it available to other JavaScript files
window.ApiService = ApiService;