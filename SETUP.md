# Setup

## Quick setup

```bash
chmod +x setup.sh
./setup.sh
```

The setup script will:

- check Python compatibility
- create a virtual environment
- install dependencies
- create a local `.env` file from the template

## Manual setup

### 1. Clone the repository

```bash
git clone https://github.com/pravinbhat/astra-rag-demo.git
cd astra-rag-demo
```

### 2. Use Python 3.13

```bash
python3.13 --version
```

If needed, create a virtual environment:

```bash
python3.13 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Update `.env` with your AstraDB values:

```env
ASTRA_DB_API_ENDPOINT=https://your-database-id-your-region.apps.astra.datastax.com
ASTRA_DB_APPLICATION_TOKEN=AstraCS:your-token-here
ASTRA_DB_KEYSPACE=default_keyspace
COLLECTION_NAME=movie_reviews
```

## Getting AstraDB credentials

1. Open [AstraDB Console](https://astra.datastax.com/)
2. Select your database
3. Copy the API endpoint
4. Create or use an application token

## Run the app

```bash
uvicorn app.main:app --reload
```

Once running:

- API base URL: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`