# Task Manager

A full-featured Django-based Task Manager with REST API, weather integration, analytics dashboard, and a modern frontend.

## Features
- **Task CRUD**: Create, read, update, and delete tasks with priorities, statuses, due dates, and locations.
- **Weather Integration**: Fetches and displays real-time weather info for tasks with a location using OpenWeatherMap.
- **Analytics Dashboard**: Visualizes task statistics, completion rates, and trends using Chart.js.
- **Recent Activities**: Tracks and displays task activity history.
- **REST API**: Built with Django REST Framework for easy integration.
- **Admin Panel**: Manage tasks and activities via Django admin.
- **CORS Support**: Ready for frontend-backend separation.

## Tech Stack
- Django 4.2.7
- Django REST Framework 3.14.0
- PostgreSQL (default, can be changed)
- OpenWeatherMap API (for weather info)
- Chart.js (frontend dashboard)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone 
cd task_manager
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv task_env
# Windows:
task_env\Scripts\activate
# macOS/Linux:
source task_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```
SECRET_KEY=your-django-secret-key
DEBUG=True
DB_NAME=task_manager
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
WEATHER_API_KEY=your_openweathermap_api_key
```

### 5. Apply Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser (for admin access)
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

Visit [http://localhost:8000/](http://localhost:8000/) for the dashboard.

## API Endpoints

All API endpoints are prefixed with `/api/`.

### Task Endpoints
- `GET /api/tasks/` — List tasks (paginated)
- `POST /api/tasks/` — Create a new task
- `GET /api/tasks/{id}/` — Retrieve a task
- `PUT /api/tasks/{id}/` — Update a task
- `DELETE /api/tasks/{id}/` — Delete a task

### Custom Actions
- `GET /api/tasks/statistics/` — Task statistics for analytics
- `GET /api/tasks/weather_summary/` — Weather info for tasks with location
- `POST /api/tasks/{id}/refresh_weather/` — Refresh weather info for a task
- `GET /api/tasks/dashboard/` — Combined dashboard data (stats, weather, activities)

## Data Models

### Task
- `title`: string
- `description`: text
- `priority`: low | medium | high
- `status`: pending | in_progress | completed
- `created_at`, `updated_at`: datetime
- `due_date`: datetime (optional)
- `location`: string (optional)
- `weather_info`: JSON (auto-fetched)

### TaskActivity
- `task`: FK to Task
- `action`: string (e.g., created, status_changed, weather_updated)
- `description`: text
- `timestamp`: datetime

## Admin Panel
- Visit `/admin/` to manage tasks and activities.
- Filter, search, and view weather info directly in the admin.

## Frontend Dashboard
- Modern, responsive dashboard at `/` (root URL)
- Visualizes stats, recent tasks, activities, and weather
- Add/edit tasks via modal forms
- Charts powered by Chart.js

## Weather Integration
- Set a location on a task to fetch weather info from OpenWeatherMap.
- Requires a valid `WEATHER_API_KEY` in your `.env`.

## CORS
- CORS is enabled for local development (`localhost:8000`, `localhost:3000`, etc.)
- Ready for integration with React, Vue, or other frontends.