/**
 * API Service for TourJett Dashboard
 * Handles all interactions with the backend API
 */

// API ayarları
const API_BASE_URL = 'http://localhost:5000/api';
const MOCK_MODE = false; // Mock mod kapalı (gerçek API kullan)

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
        getAll: () => apiCall('/tur'),
        getById: (id) => apiCall(`/tur/${id}`),
        create: (tourData) => apiCall('/tur', 'POST', tourData),
        update: (id, tourData) => apiCall(`/tur/${id}`, 'PUT', tourData),
        delete: (id) => apiCall(`/tur/${id}`, 'DELETE'),
    },
    
    // Tour Package APIs
    tourPackages: {
        getAll: () => apiCall('/turpaketleri'),
        getById: (id) => apiCall(`/turpaketleri/${id}`),
        create: (packageData) => apiCall('/turpaketleri', 'POST', packageData),
        update: (id, packageData) => apiCall(`/turpaketleri/${id}`, 'PUT', packageData),
        delete: (id) => apiCall(`/turpaketleri/${id}`, 'DELETE'),
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
    
    // Destination APIs
    destinations: {
        getAll: () => apiCall('/destinasyonlar'),
        getById: (id) => apiCall(`/destinasyonlar/${id}`),
        create: (destinationData) => apiCall('/destinasyonlar', 'POST', destinationData),
        update: (id, destinationData) => apiCall(`/destinasyonlar/${id}`, 'PUT', destinationData),
        delete: (id) => apiCall(`/destinasyonlar/${id}`, 'DELETE'),
    },
    
    // Resources APIs
    resources: {
        // Guide APIs
        guides: {
            getAll: () => apiCall('/rehber'),
            getById: (id) => apiCall(`/rehber/${id}`),
            create: (guideData) => apiCall('/rehber', 'POST', guideData),
            update: (id, guideData) => apiCall(`/rehber/${id}`, 'PUT', guideData),
            delete: (id) => apiCall(`/rehber/${id}`, 'DELETE'),
        },
        
        // Driver APIs
        drivers: {
            getAll: () => apiCall('/surucu'),
            getById: (id) => apiCall(`/surucu/${id}`),
            create: (driverData) => apiCall('/surucu', 'POST', driverData),
            update: (id, driverData) => apiCall(`/surucu/${id}`, 'PUT', driverData),
            delete: (id) => apiCall(`/surucu/${id}`, 'DELETE'),
        },
        
        // Vehicle APIs - Fixed path to match backend route
        vehicles: {
            getAll: () => apiCall('/vehicles'),
            getById: (id) => apiCall(`/vehicles/${id}`),
            create: (vehicleData) => apiCall('/vehicles', 'POST', vehicleData),
            update: (id, vehicleData) => apiCall(`/vehicles/${id}`, 'PUT', vehicleData),
            delete: (id) => apiCall(`/vehicles/${id}`, 'DELETE'),
        },
    },
    
    // Review APIs
    reviews: {
        getAll: () => apiCall('/degerlendirme'),
        getById: (id) => apiCall(`/degerlendirme/${id}`),
        create: (reviewData) => apiCall('/degerlendirme', 'POST', reviewData),
        update: (id, reviewData) => apiCall(`/degerlendirme/${id}`, 'PUT', reviewData),
        delete: (id) => apiCall(`/degerlendirme/${id}`, 'DELETE'),
        getTourReviews: (tourId) => apiCall(`/degerlendirme?tur_paketi_id=${tourId}`),
    },
    
    // Dashboard Statistics APIs
    dashboard: {
        getStats: () => apiCall('/dashboard/stats'),
        getRecentBookings: () => apiCall('/dashboard/recent-bookings'),
        getUpcomingTours: () => apiCall('/dashboard/upcoming-tours'),
        getRevenueData: () => apiCall('/dashboard/revenue'),
    },
};

// Backward compatibility for existing functions
window.getDegerlendirmeler = (turId) => ApiService.reviews.getTourReviews(turId);
window.createDegerlendirme = (data) => ApiService.reviews.create(data);
window.getTurById = (id) => ApiService.tourPackages.getById(id);

// Export the API Service
// This will make it available to other JavaScript files
window.ApiService = ApiService;