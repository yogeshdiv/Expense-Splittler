# 💰 Expense Splitter

A full-stack web application for tracking shared expenses among friends. Built with **FastAPI** (backend) and **React** (frontend).

## Features

✅ **Add User** - Easily add friends to your group
✅ **Add Expenses** - Track shared expenses with amount, description, payer, and split details
✅ **View Expenses** - See a comprehensive list of all expenses
✅ **Settlement Summary** - Automatic debt calculation and simplification to minimize transactions

## Tech Stack

- **Backend**: FastAPI, Python
- **Frontend**: React 18, Axios
- **Architecture**: REST API

## Project Structure

```
assignment/
├── backend/
│   ├── main.py                 # FastAPI application with SQLAlchemy ORM
│   ├── config.py               # Database configuration
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example            # Database config template
│   ├── .gitignore
│   ├── setup.bat               # Windows setup script
│   └── setup.sh                # macOS/Linux setup script
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── UserSection.js
│   │   │   ├── ExpenseSection.js
│   │   │   ├── ExpensesList.js
│   │   │   └── SettlementSummary.js
│   │   ├── api.js              # API client (Axios)
│   │   ├── App.js              # Main React component
│   │   ├── App.css             # Styling
│   │   └── index.js
│   ├── package.json
│   ├── .gitignore
│   └── node_modules/
│
└── README.md
```

## Setup & Installation

### Quick Start (Automated)

**Windows**:
```bash
cd backend
setup.bat
```

**macOS/Linux**:
```bash
cd backend
chmod +x setup.sh
./setup.sh
```

### Manual Setup

#### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- **Windows**:
```bash
venv\Scripts\activate
```
- **macOS/Linux**:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Configure Database:
Copy `.env.example` to `.env` and choose your database:
```bash
```

**SQLite**: No additional setup needed. Database file will be created automatically.

```bash
createdb expense_splitter
```

6. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`
Swagger Docs: `http://localhost:8000/docs`

#### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The app will open at `http://localhost:3000`

## API Endpoints

### People Management
- `GET /users` - Get all people
- `POST /users` - Add a new user
- `DELETE /users/{name}` - Remove a user

### Expenses Management
- `GET /expenses` - Get all expenses
- `POST /expenses` - Create a new expense
- `DELETE /expenses/{expense_id}` - Delete an expense

### Settlement
- `GET /settlement` - Get simplified settlement summary

## How to Use

1. **Add Friends**: Enter names and click "Add Person"
2. **Create Expense**: 
   - Fill in description (e.g., "Dinner")
   - Enter amount
   - Select who paid
   - Choose who the expense should be split between
   - Click "Add Expense"
3. **View Expenses**: All expenses are listed with details
4. **Settlement**: Check who owes whom automatically calculated and simplified

## Example

**Scenario**: Alice, Bob, and Charlie go out together

1. Alice pays Rs 1200 for dinner split between all three
   - Alice is owed Rs 400 by Bob and Charlie
   
2. Bob pays Rs 600 lunch for himself and Charlie
   - Bob is owed Rs 300 by Charlie

**Settlement Summary**:
- Charlie owes Alice Rs 400
- Charlie owes Bob Rs 300
(Simplified to: Charlie owes Alice Rs 400 + Bob Rs 300, or further simplified if there are reverse transactions)

## Notes

- **Data Persistence**: All data is stored in PostgreSQL or SQLite database (configured via .env)
- **Database**: Supports both PostgreSQL (production) and SQLite (development)
- **Auto Schema Creation**: Database tables are automatically created on first run
- Frontend auto-refreshes every 2 seconds to stay synchronized with the backend
- The debt settlement algorithm automatically simplifies transactions to minimize the number of payments needed

## Database Schema

**People Table**:
- `id`: Primary key
- `name`: Unique name of the person

**Expenses Table**:
- `id`: Primary key
- `description`: Expense description
- `amount`: Amount paid
- `paid_by_id`: Foreign key to people
- `date`: Expense date

**Expense Split Table** (Many-to-Many):
- `expense_id`: Foreign key to expenses
- `person_id`: Foreign key to people (split among)

## Troubleshooting

### Database Connection Error
**Problem**: `psycopg2.OperationalError: could not translate host name "localhost"`

**Solution**: 
- Make sure PostgreSQL is installed and running
- Or switch to SQLite in `.env`: `DATABASE_TYPE=sqlite`

### Port Already in Use
**Problem**: `OSError: [Errno 48] Address already in use`

**Solution**: Kill the existing process or change port:
```bash
# On Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# On macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Module Not Found
**Problem**: `ModuleNotFoundError: No module named 'sqlalchemy'`

**Solution**: Make sure virtual environment is activated and dependencies are installed:
```bash
# Activate venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Won't Connect to Backend
**Problem**: `Error: Network Error` or `CORS error`

**Solution**: 
- Make sure backend is running on `http://localhost:8000`
- API will auto-refresh every 2 seconds
- Check browser console for detailed errors

## Future Enhancements

- User authentication & authorization
- Payment history tracking
- Export/Download reports (PDF, CSV)
- Mobile app (React Native/Flutter)
- Real-time updates using WebSockets
- Email notifications
- Database migrations (Alembic)
- Advanced settlement algorithms
- Group management
- Settlement confirmation tracking

---

Made with ❤️ for easy expense management
