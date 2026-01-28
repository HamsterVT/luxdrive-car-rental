// Load cars on page load
document.addEventListener('DOMContentLoaded', function () {
    loadCars();
});

// Load all cars from API
async function loadCars() {
    try {
        const response = await fetch('http://localhost:8001/api/cars/');
        const cars = await response.json();
        displayCars(cars);
    } catch (error) {
        console.error('Error loading cars:', error);
    }
}

// Display cars in grid
function displayCars(cars) {
    const grid = document.getElementById('carsGrid');
    grid.innerHTML = '';

    cars.forEach(car => {
        const carCard = createCarCard(car);
        grid.appendChild(carCard);
    });
}

// Create car card element
function createCarCard(car) {
    const card = document.createElement('div');
    card.className = 'car-card';
    card.dataset.type = car.car_type;

    // Map car IDs to image files
    const imageMap = {
        'M5F90': 'bmw_m5_f90_1769585537447.png',
        'E63S': 'mercedes_e63s_1769585692589.png',
        'REVUELTO': 'lamborghini_revuelto_1769585801494.png',
        'SF90': 'ferrari_sf90_1769586005810.png',
        'PHANTOM': 'rolls_royce_phantom_1769586067724.png',
        'G63AMG': 'mercedes_g63_1769586376400.png',
        'M8COMP': 'bmw_m8_competition_1769588008746.png',
        'M3G80': 'bmw_m3_g80_1769587817963.png',
        'G6X6': 'mercedes_g63_6x6_1769588309525.png',
        'GHOST': 'rolls_royce_ghost_1769588635498.png',
        '812COMP': 'ferrari_812_competizione_1769588222950.png',
        'M5LOW': 'bmw_m5_f90_1769585537447.png'
    };

    const imagePath = imageMap[car.car_id] || 'default.png';

    card.innerHTML = `
        <img src="/static/images/${imagePath}" alt="${car.brand} ${car.model}" class="car-image">
        <div class="car-info">
            <div class="car-brand">${car.brand}</div>
            <div class="car-model">${car.model}</div>
            <div class="car-details">
                <div class="detail-item">
                    <strong>${car.year}</strong>
                    Year
                </div>
                <div class="detail-item">
                    <strong>${car.color}</strong>
                    Color
                </div>
                <div class="detail-item">
                    <strong>${car.fuel_level}%</strong>
                    Fuel
                </div>
                <div class="detail-item">
                    <strong>${car.location}</strong>
                    Location
                </div>
            </div>
            <div class="car-price">
                <div>
                    <div class="price">$${car.hourly_rate}</div>
                    <div class="price-label">per hour</div>
                </div>
                <button class="btn-book" onclick="openBookingModal('${car.car_id}', '${car.brand} ${car.model}', '${car.location}')">
                    Book Now
                </button>
            </div>
        </div>
    `;

    return card;
}

// Filter cars by type
function filterCars(type) {
    const cards = document.querySelectorAll('.car-card');
    const buttons = document.querySelectorAll('.filter-btn');

    // Update active button
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    // Filter cards
    cards.forEach(card => {
        if (type === 'all' || card.dataset.type === type) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Open booking modal
function openBookingModal(carId, carName, location) {
    const modal = document.getElementById('bookingModal');
    document.getElementById('car_id').value = carId;

    // Pre-fill location if available
    const locationSelect = document.querySelector('select[name="pickup_location"]');
    if (locationSelect && location) {
        locationSelect.value = location;
    }

    modal.style.display = 'block';
}

// Close modal
function closeModal() {
    const modal = document.getElementById('bookingModal');
    modal.style.display = 'none';
    document.getElementById('bookingForm').reset();
    document.getElementById('bookingResult').innerHTML = '';
}

// Close modal when clicking outside
window.onclick = function (event) {
    const modal = document.getElementById('bookingModal');
    if (event.target == modal) {
        closeModal();
    }
}

// Handle booking form submission
document.addEventListener('DOMContentLoaded', function () {
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            const formData = new FormData(bookingForm);
            const data = {
                car_id: formData.get('car_id'),
                user_name: formData.get('user_name'),
                user_email: formData.get('user_email'),
                user_phone: formData.get('user_phone'),
                pickup_location: formData.get('pickup_location'),
                start_datetime: formData.get('start_datetime'),
                end_datetime: formData.get('end_datetime'),
                rental_type: formData.get('rental_type')
            };

            try {
                const response = await fetch('/api/rentals/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                const resultDiv = document.getElementById('bookingResult');

                if (response.ok && result.status === 'success') {
                    resultDiv.className = 'success';
                    resultDiv.innerHTML = `
                        <h3>Booking Request Submitted!</h3>
                        <p>Your request is being processed.</p>
                        <p>Booking ID: ${result.rental.id}</p>
                        <p>Estimated Price: $${result.total_price}</p>
                        <p><strong>Track your booking status in <a href="/my-bookings/" style="color: #000; text-decoration: underline;">My Rentals</a></strong></p>
                    `;
                    bookingForm.reset();
                } else {
                    resultDiv.className = 'error';
                    resultDiv.innerHTML = `
                        <h3>Booking Failed</h3>
                        <p>${result.message || 'Unable to complete booking'}</p>
                        <p>${result.reason || ''}</p>
                    `;
                }
            } catch (error) {
                const resultDiv = document.getElementById('bookingResult');
                resultDiv.className = 'error';
                resultDiv.innerHTML = `
                    <h3>Error</h3>
                    <p>Unable to connect to server. Please try again.</p>
                `;
            }
        });
    }
});

// Search cars function
function searchCars() {
    const form = document.getElementById('searchForm');
    const location = form.querySelector('select[name="location"]').value;
    const startDate = form.querySelector('input[name="start_datetime"]').value;
    const endDate = form.querySelector('input[name="end_datetime"]').value;

    if (!location || !startDate || !endDate) {
        alert('Please fill in all search fields');
        return;
    }

    // Scroll to cars section
    document.getElementById('cars').scrollIntoView({ behavior: 'smooth' });

    // Filter cars by location
    const cards = document.querySelectorAll('.car-card');
    cards.forEach(card => {
        const cardLocation = card.querySelector('.detail-item:nth-child(4) strong').textContent;
        if (cardLocation === location) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}
