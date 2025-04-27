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
        login: (email, password) => apiCall('/auth/login', 'POST', { email, password }),
        signup: (userData) => apiCall('/auth/signup', 'POST', userData),
        logout: () => apiCall('/auth/logout', 'POST'),
        getCurrentUser: () => apiCall('/auth/me'),
    },
    
    // Tour APIs
    tours: {
        getAll: () => apiCall('/turlar'),
        getById: (id) => apiCall(`/turlar/${id}`),
        create: (tourData) => apiCall('/turlar', 'POST', tourData),
        update: (id, tourData) => apiCall(`/turlar/${id}`, 'PUT', tourData),
        delete: (id) => apiCall(`/turlar/${id}`, 'DELETE'),
    },
    
    // Tour Package APIs - Yeni eklendi
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
        getAll: () => apiCall('/musteriler'),
        getById: (id) => apiCall(`/musteriler/${id}`),
        create: (customerData) => apiCall('/musteriler', 'POST', customerData),
        update: (id, customerData) => apiCall(`/musteriler/${id}`, 'PUT', customerData),
        delete: (id) => apiCall(`/musteriler/${id}`, 'DELETE'),
    },
    
    // Region APIs (now using destinasyon)
    regions: {
        getAll: () => apiCall('/destinasyonlar'),
        getById: (id) => apiCall(`/destinasyonlar/${id}`),
    },
    
    // Destination APIs
    destinations: {
        getAll: () => apiCall('/destinasyonlar'),
        getById: (id) => apiCall(`/destinasyonlar/${id}`),
        create: (destinationData) => apiCall('/destinasyonlar', 'POST', destinationData),
        update: (id, destinationData) => apiCall(`/destinasyonlar/${id}`, 'PUT', destinationData),
        delete: (id) => apiCall(`/destinasyonlar/${id}`, 'DELETE'),
    },
    
    // Resource APIs
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
        
        // Vehicle APIs
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
        getAll: () => apiCall('/degerlendirmeler'),
        getById: (id) => apiCall(`/degerlendirmeler/${id}`),
        create: (reviewData) => apiCall('/degerlendirmeler', 'POST', reviewData),
        update: (id, reviewData) => apiCall(`/degerlendirmeler/${id}`, 'PUT', reviewData),
        delete: (id) => apiCall(`/degerlendirmeler/${id}`, 'DELETE'),
    },
    
    // Dashboard Statistics APIs
    dashboard: {
        getStats: () => apiCall('/dashboard/stats'),
        getRecentBookings: () => apiCall('/dashboard/recent-bookings'),
        getUpcomingTours: () => apiCall('/dashboard/upcoming-tours'),
        getRevenueData: () => apiCall('/dashboard/revenue'),
    },
};

// Login User function - Used by login.js
window.loginUser = async function(credentials) {
    console.log('Login attempt with:', credentials);
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: credentials.email,
                password: credentials.password
            }),
            credentials: 'include'
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error(`Login error: HTTP ${response.status}`, errorText);
            throw new Error('E-posta veya şifre hatalı. Lütfen tekrar deneyin.');
        }
        
        const data = await response.json();
        console.log('Login API response:', data);
        return data;
    } catch (error) {
        console.error('Login error:', error);
        throw new Error(error.message || 'E-posta veya şifre hatalı. Lütfen tekrar deneyin.');
    }
};

// Signup User function - Used by login.js
window.signupUser = async function(userData) {
    console.log('Signup attempt with:', userData);
    try {
        const response = await fetch(`${API_BASE_URL}/auth/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
            credentials: 'include'
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error(`Signup error: HTTP ${response.status}`, errorText);
            throw new Error('Kayıt işlemi başarısız oldu. Lütfen tekrar deneyin.');
        }
        
        const data = await response.json();
        console.log('Signup API response:', data);
        return data;
    } catch (error) {
        console.error('Signup error:', error);
        throw new Error(error.message || 'Kayıt işlemi başarısız oldu. Lütfen tekrar deneyin.');
    }
};

// Get Tour By ID function - Used by package-details.js and booking.js
window.getTurById = async function(id) {
    console.log('Getting tour details for ID:', id);
    try {
        // Önce Tur Paketi olarak dene
        try {
            const response = await fetch(`${API_BASE_URL}/turpaketleri/${id}`);
            if (response.ok) {
                const data = await response.json();
                console.log("Tur paketi bulundu:", data);
                return data;
            }
        } catch (error) {
            console.log("Tur paketi bulunamadı, turlar endpoint'i deneniyor...");
        }
        
        // Tur paketi bulunamazsa, Tur olarak dene
        try {
            const response = await fetch(`${API_BASE_URL}/turlar/${id}`);
            if (response.ok) {
                const data = await response.json();
                console.log("Tur bulundu:", data);
                return data;
            } else {
                throw new Error(`Tur bulunamadı: ${response.status}`);
            }
        } catch (error) {
            console.error("Tur da bulunamadı:", error);
            throw new Error(`Tur bulunamadı: ${error.message}`);
        }
    } catch (error) {
        console.error("Tur verileri alınamadı:", error);
        throw error;
    }
};

// Create Rezervasyon function - Used by booking.js
window.createRezervasyon = async function(reservationData) {
    console.log('Creating reservation with data:', reservationData);
    try {
        const response = await fetch(`${API_BASE_URL}/rezervasyon`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(reservationData),
            credentials: 'include'
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error(`Reservation error: HTTP ${response.status}`, errorText);
            throw new Error('Rezervasyon oluşturulamadı.');
        }
        
        const data = await response.json();
        console.log('Reservation API response:', data);
        return data;
    } catch (error) {
        console.error('Reservation error:', error);
        throw new Error(error.message || 'Rezervasyon oluşturulamadı. Lütfen tekrar deneyin.');
    }
};

// Export the API Service
// This will make it available to other JavaScript files
window.ApiService = ApiService;