# SmartCare - Smart Hospital System

SmartCare is a Django-based smart hospital system designed to improve the experience for both patients and doctors.  
The project provides a modern web platform where patients can explore doctors, book appointments, use an AI assistant for doctor suggestions, and track their appointment history, while doctors can manage appointments, patients, and availability from their own dashboard.

---

## Features

### Patient Side
- Browse doctors by **section**, **clinic**, and **search**
- Book appointments through a clean modal interface
- View personal appointments with status tracking:
  - Pending
  - Confirmed
  - Cancelled
- Use an **AI Symptom Checker** that asks follow-up questions and helps suggest the most suitable doctor
- Responsive and simple user-friendly design

### Doctor Side
- Doctor dashboard with quick stats:
  - Today's appointments
  - Total patients
  - Pending appointments
- View and manage appointments
- View patients list
- Manage availability
- Confirm or cancel appointments

### AI Assistant
- Multi-step patient chat
- Collects patient symptoms through conversation
- Suggests a suitable doctor based on patient answers and available doctor data
- Built to support smarter booking decisions

---

## Tech Stack

- **Backend:** Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** MySQL
- **Authentication:** Django auth system
- **Deployment:** AWS EC2 + Gunicorn + Nginx
- **AI Integration:** OpenAI API

---

## Project Screens

### Patient Features
- Doctors page with filtering and booking
- AI assistant page
- Patient appointments dashboard

### Doctor Features
- Doctor dashboard
- Appointments management
- Patient records view
- Availability section

---

## Main Modules

### 1. Authentication
- Login
- Logout
- User-based access for patients and doctors

### 2. Doctors Management
- Doctors linked to clinics and sections
- Detailed doctor cards
- Search and filtering support

### 3. Appointment System
- Book appointments by date and time
- Appointment notes
- Appointment status handling
- Patient and doctor appointment views

### 4. AI Assistant
- Chat-based symptom collection
- Smart recommendation flow
- Suggests doctors based on conversation data

### 5. Doctor Dashboard
- Dashboard statistics
- Appointment actions
- Patients list
- Availability management

---

## Database Models

Main models used in the project include:

- `Patient`
- `Doctor`
- `Clinic`
- `Section`
- `Appointment`
- `MedicalRecord`
- `AIChatSession`
- `AIChatMessage`

These models are connected to support appointment booking, doctor discovery, medical records, and AI-based recommendations.

---

## Installation

### 1. Clone the repository
```bash
git clone YOUR_REPO_URL
cd YOUR_PROJECT_FOLDER
