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
    
    // User authentication APIs
    users: {
        login: (email, password) => apiCall('/users/login', 'POST', { email, password }),
        signup: (userData) => apiCall('/users/signup', 'POST', userData),
        getCurrentUser: () => apiCall('/users/me'),
    },
    
    // Tour APIs
    tours: {
        getAll: () => apiCall('/turlar'),        
        getById: (id) => apiCall(`/turlar/${id}`),
        create: (tourData) => {
            const apiData = {
                adi: tourData.ad,
                sure: tourData.sure,
                fiyat: parseFloat(tourData.fiyat),
                destinasyon_id: parseInt(tourData.destinasyon_id),
                aciklama: tourData.aciklama || "",
                aktif: tourData.durum === 'active' ? true : false
            };
            return apiCall('/turlar', 'POST', apiData);
        },
        update: (id, tourData) => apiCall(`/turlar/${id}`, 'PUT', tourData),
        delete: (id) => apiCall(`/turlar/${id}`, 'DELETE'),
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
        
        destinations: {
            getAll: () => apiCall('/destinasyonlar'),
            getById: (id) => apiCall(`/destinasyonlar/${id}`),
            create: (destinationData) => apiCall('/destinasyonlar', 'POST', destinationData),
            update: (id, destinationData) => apiCall(`/destinasyonlar/${id}`, 'PUT', destinationData),
            delete: (id) => apiCall(`/destinasyonlar/${id}`, 'DELETE'),
        },
        
        tours: {
            getAll: () => apiCall('/turlar'),        
            getById: (id) => apiCall(`/turlar/${id}`),
            create: (tourData) => {
                const apiData = {
                    adi: tourData.ad,
                    sure: tourData.sure,
                    fiyat: parseFloat(tourData.fiyat),
                    destinasyon_id: parseInt(tourData.destinasyon_id),
                    aciklama: tourData.aciklama || "",
                    aktif: tourData.durum === 'active' ? true : false
                };
                return apiCall('/turlar', 'POST', apiData);
            },
            update: (id, tourData) => apiCall(`/turlar/${id}`, 'PUT', tourData),
            delete: (id) => apiCall(`/turlar/${id}`, 'DELETE'),
        },
    },
    
    // Review APIs - Fixed to use degerlendirmeler instead of degerlendirme
    reviews: {
        getAll: () => apiCall('/degerlendirmeler'),
        getById: (id) => apiCall(`/degerlendirmeler/${id}`),
        create: (reviewData) => apiCall('/degerlendirmeler', 'POST', reviewData),
        update: (id, reviewData) => apiCall(`/degerlendirmeler/${id}`, 'PUT', reviewData),
        delete: (id) => apiCall(`/degerlendirmeler/${id}`, 'DELETE'),
        getTourReviews: (tourId) => apiCall(`/degerlendirmeler?tur_paketi_id=${tourId}`),
    },
    
    // Dashboard Statistics APIs
    dashboard: {
        getStats: () => apiCall('/dashboard/stats'),
        getRecentBookings: () => apiCall('/dashboard/recent-bookings'),
        getUpcomingTours: () => apiCall('/dashboard/upcoming-tours'),
        getRevenueData: () => apiCall('/dashboard/revenue'),
    },

    // Regions APIs
    regions: {
        getAll: () => apiCall('/destinasyonlar'),
        getById: (id) => apiCall(`/destinasyonlar/${id}`),
        create: (regionData) => apiCall('/destinasyonlar', 'POST', regionData),
        update: (id, regionData) => apiCall(`/destinasyonlar/${id}`, 'PUT', regionData),
        delete: (id) => apiCall(`/destinasyonlar/${id}`, 'DELETE'),
    },
};

// Update tours to correctly use turpaketleri endpoint
// This ensures the dashboard loads tour packages correctly
window.loadTourPackages = () => ApiService.tourPackages.getAll();
window.getTourPackageById = (id) => ApiService.tourPackages.getById(id);

// Enhanced helper function to load destination data for dropdowns
window.loadDestinationOptions = async (selectElementId) => {
    try {
        console.log(`Loading destinations for dropdown: ${selectElementId}`);
        const destinations = await ApiService.destinations.getAll();
        const selectElement = document.getElementById(selectElementId);
        
        if (selectElement && destinations && destinations.length > 0) {
            console.log(`Found ${destinations.length} destinations, populating dropdown ${selectElementId}`);
            selectElement.innerHTML = '<option value="">Select Destination</option>';
            destinations.forEach(destination => {
                const option = document.createElement('option');
                option.value = destination.id;
                option.textContent = destination.ad || destination.name;
                selectElement.appendChild(option);
            });
            return true;
        } else {
            console.warn(`Failed to populate destination dropdown: ${selectElementId}`);
            if (!selectElement) console.warn('Select element not found');
            if (!destinations || destinations.length === 0) console.warn('No destinations data received');
            return false;
        }
    } catch (error) {
        console.error('Failed to load destinations:', error);
        return false;
    }
};

// Helper function to load guides data for dropdowns
window.loadGuideOptions = async (selectElementId) => {
    try {
        const guides = await ApiService.resources.guides.getAll();
        const selectElement = document.getElementById(selectElementId);
        
        if (selectElement && guides && guides.length > 0) {
            selectElement.innerHTML = '<option value="">Select Guide</option>';
            guides.forEach(guide => {
                const option = document.createElement('option');
                option.value = guide.id;
                option.textContent = guide.ad || guide.name;
                selectElement.appendChild(option);
            });
            return true;
        }
        return false;
    } catch (error) {
        console.error('Failed to load guides:', error);
        return false;
    }
};

// Helper function to load drivers data for dropdowns
window.loadDriverOptions = async (selectElementId) => {
    try {
        const drivers = await ApiService.resources.drivers.getAll();
        const selectElement = document.getElementById(selectElementId);
        
        if (selectElement && drivers && drivers.length > 0) {
            selectElement.innerHTML = '<option value="">Select Driver</option>';
            drivers.forEach(driver => {
                const option = document.createElement('option');
                option.value = driver.id;
                option.textContent = driver.ad || driver.name;
                selectElement.appendChild(option);
            });
            return true;
        }
        return false;
    } catch (error) {
        console.error('Failed to load drivers:', error);
        return false;
    }
};

// Helper function to load vehicles data for dropdowns
window.loadVehicleOptions = async (selectElementId) => {
    try {
        const vehicles = await ApiService.resources.vehicles.getAll();
        const selectElement = document.getElementById(selectElementId);
        
        if (selectElement && vehicles && vehicles.length > 0) {
            selectElement.innerHTML = '<option value="">Select Vehicle</option>';
            vehicles.forEach(vehicle => {
                const option = document.createElement('option');
                option.value = vehicle.id;
                option.textContent = vehicle.ad || vehicle.name || `${vehicle.tip || vehicle.type} - ${vehicle.plaka || vehicle.licensePlate}`;
                selectElement.appendChild(option);
            });
            return true;
        }
        return false;
    } catch (error) {
        console.error('Failed to load vehicles:', error);
        return false;
    }
};

// Helper function to load tour references data for dropdowns
window.loadTourOptions = async (selectElementId) => {
    try {
        const tours = await ApiService.tours.getAll();
        const selectElement = document.getElementById(selectElementId);
        
        if (selectElement && tours && tours.length > 0) {
            selectElement.innerHTML = '<option value="">Select Tour</option>';
            tours.forEach(tour => {
                const option = document.createElement('option');
                option.value = tour.id;
                option.textContent = tour.adi || tour.ad || tour.name;
                selectElement.appendChild(option);
            });
            return true;
        }
        return false;
    } catch (error) {
        console.error('Failed to load tours:', error);
        return false;
    }
};

// Convenience function to load all tour form dropdowns at once
window.loadAllTourFormDropdowns = async () => {
    console.log('Loading all dropdown data for tour form');
    const results = await Promise.all([
        window.loadDestinationOptions('tourLocation'),
        window.loadGuideOptions('tourGuide'),
        window.loadDriverOptions('tourDriver'),
        window.loadVehicleOptions('tourVehicle'),
        window.loadTourOptions('tourReference')
    ]);
    
    return results.every(result => result === true);
};

// User Authentication Functions - These functions were missing
window.loginUser = async (userData) => {
    try {
        console.log('Attempting to log in user:', userData.email);
        const response = await apiCall('/users/login', 'POST', {
            email: userData.email,
            password: userData.password
        });
        console.log('Login response:', response);
        return response;
    } catch (error) {
        console.error('Login failed:', error);
        throw new Error('Login failed: ' + (error.message || 'Unknown error'));
    }
};

window.signupUser = async (userData) => {
    try {
        console.log('Attempting to register new user:', userData);
        const response = await apiCall('/users/signup', 'POST', userData);
        console.log('Signup response:', response);
        return response;
    } catch (error) {
        console.error('Signup failed:', error);
        throw new Error('Signup failed: ' + (error.message || 'Unknown error'));
    }
};

// Backward compatibility for existing functions
window.getDegerlendirmeler = (turId) => ApiService.reviews.getTourReviews(turId);
window.createDegerlendirme = (data) => ApiService.reviews.create(data);
window.getTurById = (id) => ApiService.tourPackages.getById(id);

// Export the API Service
// This will make it available to other JavaScript files
window.ApiService = ApiService;