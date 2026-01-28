# 🚗 Rental Service - Car Sharing Microservice

Premium car rental service with real-time availability checking.

## 🎯 Features

- Create car rentals
- Real-time availability validation via Fleet Service
- Automatic price calculation
- Rental management (view, complete, cancel)
- RESTful API

## 🚀 Quick Start

### Installation

```bash
cd rental_service
pip3 install -r requirements.txt
```

### Run Migrations

```bash
python3 manage.py migrate
```

### Start Server

```bash
python3 manage.py runserver 8000
```

Server will run at: `http://localhost:8000`

## 📡 API Endpoints

### Base URL
```
http://localhost:8000/api/
```

### 1. Create Rental

**POST** `/api/rentals/`

**Request Body:**
```json
{
  "car_id": "M5F90",
  "user_email": "user@example.com",
  "user_name": "John Doe",
  "user_phone": "+1234567890",
  "start_datetime": "2026-02-01T10:00:00",
  "end_datetime": "2026-02-01T18:00:00",
  "pickup_location": "Downtown Station",
  "rental_type": "hourly"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Car rented successfully",
  "rental": {
    "id": 1,
    "car_id": "M5F90",
    "status": "active",
    "total_price": "1200.00"
  },
  "car_details": {
    "brand": "BMW",
    "model": "M5 F90",
    "fuel_level": 85
  }
}
```

**Rejection Response (400):**
```json
{
  "status": "rejected",
  "message": "Car is not available",
  "reason": "Low fuel level (15%). Car needs refueling"
}
```

### 2. List All Rentals

**GET** `/api/rentals/`

**Response:**
```json
[
  {
    "id": 1,
    "car_id": "M5F90",
    "user_name": "John Doe",
    "status": "active",
    "total_price": "1200.00"
  }
]
```

### 3. Get Rental Details

**GET** `/api/rentals/{id}/`

### 4. Complete Rental

**POST** `/api/rentals/{id}/complete/`

**Response:**
```json
{
  "status": "success",
  "message": "Rental completed successfully"
}
```

### 5. Cancel Rental

**DELETE** `/api/rentals/{id}/`

## 🔧 Configuration

### Fleet Service URL

Edit `rental_service/settings.py`:

```python
FLEET_SERVICE_URL = 'http://localhost:8001'  # Local
# FLEET_SERVICE_URL = 'https://fleet-service.onrender.com'  # Production
```

## 🧪 Testing

### Test with cURL

```bash
# Create rental
curl -X POST http://localhost:8000/api/rentals/ \
  -H "Content-Type: application/json" \
  -d '{
    "car_id": "M5F90",
    "user_email": "test@mail.com",
    "user_name": "Test User",
    "user_phone": "+1234567890",
    "start_datetime": "2026-02-01T10:00:00",
    "end_datetime": "2026-02-01T18:00:00",
    "pickup_location": "Downtown Station",
    "rental_type": "hourly"
  }'

# List rentals
curl http://localhost:8000/api/rentals/
```

## 📦 Dependencies

- Django 4.2.27
- Django REST Framework 3.14.0
- django-cors-headers 4.3.1
- requests 2.31.0

## 🌐 Deployment (Render)

1. Push code to GitHub
2. Create new Web Service on Render
3. Set environment variables:
   - `FLEET_SERVICE_URL`: URL of deployed Fleet Service
4. Deploy!

## 🏗️ Architecture

```
User Request → Rental Service
                    ↓
            HTTP POST to Fleet Service
                    ↓
            Availability Check
                    ↓
            Response (available/not available)
                    ↓
            Create Rental or Reject
                    ↓
            Return to User
```

## 📝 License

MIT License
