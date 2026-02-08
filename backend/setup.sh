#!/bin/bash

# Quick setup script for Linux/macOS
# Required: Python 3.11.9

echo ""
echo "==============================================="
echo "Expense Splitter - Backend Setup"
echo "Requires Python 3.11.9"
echo "==============================================="
echo ""

# Check Python version
python3 --version
echo ""
echo "If you don't have Python 3.11.9, install it from https://www.python.org/downloads/"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment with Python 3.11.9..."
    python3.11 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Python 3.11.9 not found."
        echo "Please install Python 3.11.9 from https://www.python.org/downloads/"
        exit 1
    fi
else
    echo "Virtual environment already exists."
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Creating .env file from template..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ".env file created. Please update it with your database settings."
else
    echo ".env file already exists."
fi

echo ""
echo "==============================================="
echo "Setup Complete!"
echo "==============================================="
echo ""
echo "To start the server, run:"
echo "   python main.py"
echo ""
echo "The API will be available at:"
echo "   http://localhost:8000"
echo ""
echo "Swagger Docs available at:"
echo "   http://localhost:8000/docs"
echo ""
