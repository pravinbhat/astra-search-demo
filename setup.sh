#!/bin/bash
# Setup script for astra-search-demo

set -e

echo "🚀 Setting up Astra Search Demo..."

# Function to check if a Python version is compatible
check_python_version() {
    local python_cmd=$1
    if ! command -v "$python_cmd" &> /dev/null; then
        return 1
    fi
    
    local version=$($python_cmd --version 2>&1 | awk '{print $2}')
    local major=$(echo $version | cut -d. -f1)
    local minor=$(echo $version | cut -d. -f2)
    
    # Check if version is 3.11, 3.12, or 3.13
    if [ "$major" -eq 3 ] && [ "$minor" -ge 11 ] && [ "$minor" -lt 14 ]; then
        echo "$python_cmd"
        return 0
    fi
    return 1
}

# Try to find a compatible Python version
PYTHON_CMD=""
echo "🔍 Looking for compatible Python version (3.11, 3.12, or 3.13)..."

# Try specific versions first
for version in python3.13 python3.12 python3.11; do
    if PYTHON_CMD=$(check_python_version "$version"); then
        PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
        echo "✅ Found compatible Python: $PYTHON_CMD ($PYTHON_VERSION)"
        break
    fi
done

# If no specific version found, try python3
if [ -z "$PYTHON_CMD" ]; then
    if PYTHON_CMD=$(check_python_version "python3"); then
        PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
        echo "✅ Found compatible Python: $PYTHON_CMD ($PYTHON_VERSION)"
    fi
fi

# If still no compatible version found, exit with error
if [ -z "$PYTHON_CMD" ]; then
    echo "❌ Error: No compatible Python version found!"
    echo ""
    echo "This project requires Python 3.11, 3.12, or 3.13"
    echo "Python 3.14+ is not supported due to pydantic-core compatibility issues"
    echo ""
    echo "Please install a compatible Python version:"
    echo ""
    echo "On macOS with Homebrew:"
    echo "  brew install python@3.13"
    echo ""
    echo "On Ubuntu/Debian:"
    echo "  sudo apt install python3.13"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Remove old venv if exists
if [ -d "venv" ]; then
    echo "🗑️  Removing old virtual environment..."
    rm -rf venv
fi

# Create new virtual environment with the compatible Python version
echo "📦 Creating virtual environment with $PYTHON_CMD..."
$PYTHON_CMD -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your AstraDB credentials"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate        # bash/zsh"
echo "   source venv/bin/activate.fish   # fish"
echo ""
echo "2. Edit .env file with your AstraDB credentials"
echo ""
echo "3. Run the application:"
echo "   uvicorn app.main:app --reload"
echo ""
echo "4. Access API docs at http://localhost:8000/docs"

# Made with Bob
