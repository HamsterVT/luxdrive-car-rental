# 🔧 Fleet Service - Car Availability Microservice

Manages luxury car fleet and validates rental availability.

## 🎯 Features

- Luxury car fleet management
- Real-time availability checking
- Fuel/battery level monitoring
- Location verification
- Time conflict detection
- Maintenance status tracking

## 🚀 Quick Start

### Installation

```bash
cd fleet_service
pip3 install -r requirements.txt
```

### Run Migrations

```bash
python3 manage.py migrate
```

### Load Luxury Cars

```bash
python3 manage.py load_cars
```

This loads 12 premium vehicles:
- BMW M5 F90
- Mercedes E63S AMG
- BMW M8 Competition
- BMW M3 G80
- Mercedes G63 AMG
- Lamborghini Revuelto
- Ferrari SF90 Stradale
- Ferrari 812 Competizione
- Mercedes G-Class 6x6
- Rolls-Royce Phantom
- Rolls-Royce Ghost

### Start Server

```bash
python3 manage.py runserver 8001
```

Server will run at: `http://localhost:8001`

## 📡 API Endpoints

### Base URL
```
http://localhost:8001/api/
```

### 1. Check Availability

**POST** `/api/check-availability/`

**Request Body:**
```json
{
  "car_id": "M5F90",
  "start_datetime": "2026-02-01T10:00:00",
  "end_datetime": "2026-02-01T18:00:00",
  "pickup_location": "Downtown Station"
}
```

**Available Response (200):**
```json
{
  "available": true,
  "message": "Car is available",
  "car_details": {
    "brand": "BMW",
    "model": "M5 F90",
    "year": 2023,
    "color": "Marina Bay Blue",
    "fuel_level": 85,
    "location": "Downtown Station",
    "hourly_rate": "150.00",
    "daily_rate": "1200.00"
  }
}
```

**Not Available Responses:**

**Low Fuel:**
```json
{
  "available": false,
  "message": "Car is not available",
  "reason": "Low fuel level (15%). Car needs refueling"
}
```

**Time Conflict:**
```json
{
  "available": false,
  "message": "Car is not available",
  "reason": "Time conflict with existing booking",
  "conflict_details": {
    "existing_booking_start": "2026-02-01T14:00:00",
    "existing_booking_end": "2026-02-01T16:00:00"
  }
}
```

**Wrong Location:**
```json
{
  "available": false,
  "message": "Car is not available",
  "reason": "Car is located at Airport Terminal, not Downtown Station"
}
```

**Under Maintenance:**
```json
{
  "available": false,
  "message": "Car is not available",
  "reason": "Car is currently under maintenance"
}
```

### 2. Register Rental

**POST** `/api/rentals/register/`

**Request Body:**
```json
{
  "car_id": "M5F90",
  "start_datetime": "2026-02-01T10:00:00",
  "end_datetime": "2026-02-01T18:00:00"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Rental registered successfully"
}
```

### 3. List All Cars

**GET** `/api/cars/`

**Response:**
```json
[
  {
    "car_id": "M5F90",
    "brand": "BMW",
    "model": "M5 F90",
    "year": 2023,
    "color": "Marina Bay Blue",
    "car_type": "sedan",
    "fuel_level": 85,
    "location": "Downtown Station",
    "hourly_rate": "150.00",
    "is_available": true
  }
]
```

### 4. Get Car Details

**GET** `/api/cars/{car_id}/`

## 🧪 Testing

### Test with cURL

```bash
# Check availability
curl -X POST http://localhost:8001/api/check-availability/ \
  -H "Content-Type: application/json" \
  -d '{
    "car_id": "M5F90",
    "start_datetime": "2026-02-01T10:00:00",
    "end_datetime": "2026-02-01T18:00:00",
    "pickup_location": "Downtown Station"
  }'

# List all cars
curl http://localhost:8001/api/cars/

# Get car details
curl http://localhost:8001/api/cars/M5F90/
```

## 🚗 Available Locations

- Downtown Station
- Airport Terminal
- Shopping Mall
- University Campus
- Business District

## ✅ Validation Rules

1. **Car Exists**: Car must be in database
2. **Not Under Maintenance**: `is_under_maintenance = False`
3. **Sufficient Fuel**: Fuel/battery level ≥ 20%
4. **Correct Location**: Car location matches pickup location
5. **No Time Conflicts**: No overlapping bookings

## 📦 Dependencies

- Django 4.2.27
- Django REST Framework 3.14.0
- django-cors-headers 4.3.1

## 🌐 Deployment (Render)

1. Push code to GitHub
2. Create new Web Service on Render
3. Deploy!

## 🏗️ Architecture

```
Rental Service Request
        ↓
Check Availability Endpoint
        ↓
Validate:
  - Car exists
  - Not under maintenance
  - Fuel level ≥ 20%
  - Correct location
  - No time conflicts
        ↓
Return available/not available
```

## 📝 License

MIT License
