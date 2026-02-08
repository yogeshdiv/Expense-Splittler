# 💰 Expense Splitter

A full-stack web application for tracking shared expenses among friends. Built with **FastAPI** (backend) and **React** (frontend).

**Live demo:** https://split-up-1.onrender.com/

## Features

✅ **Add User** - Easily add friends to your group
✅ **Add Expenses** - Track shared expenses with amount, description, payer, and split details
✅ **View Expenses** - See a comprehensive list of all expenses
✅ **Settlement Summary** - Automatic debt calculation and simplification to minimize transactions


## Project Structure

```
assignment/
├── backend/
│   ├── main.py                 # FastAPI application with SQLAlchemy ORM
│   ├── validation_model         # Pydantic models
│   ├── routes                   # user and expense routes
│   ├── db                       # folder containing connection and different models
│   ├── services                 # services for settlement and expense
│   ├── requirements.txt         # Python dependencies
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

5. Run the server:
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


## Database Schema

**User Table**:
- `id`: Primary key
- `name`: Unique name of the person
- `balance`: Balance 

**Expenses Table**:
- `id`: Primary key
- `description`: Expense description
- `amount`: Amount paid
- `paid_by_id`: Foreign key to people
- `date`: Expense date

**Expense Split Table** (Many-to-Many):
- `expense_id`: Foreign key to expenses
- `person_id`: Foreign key to people (split among)


## Future Enhancements

- Pagination for displaying expenses
- migartion to postgres for scaling
- User authentication & authorization
- Export/Download reports (PDF, CSV)
- Email notifications
- Settlement confirmation tracking

---