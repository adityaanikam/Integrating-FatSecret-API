



# FastAPI FatSecret API Integration

A FastAPI application that integrates with the FatSecret API to search for food information and nutritional data.

## Project Structure
```
fastapi_project/
├── .env                    # Environment variables
├── auth.py                 # Authentication module
├── docker-compose.yml      # Docker compose configuration
├── dockerfile             # Docker configuration
├── main.py                # Main application file
└── requirements.txt       # Python dependencies
```

## Setup

1. Clone the repository:
```bash
git clone 
https://github.com/adityaanikam/Integrating-FatSecret-API
cd fastapi_project
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  
# On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your FatSecret API credentials:
```env
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```

## Running the Application

### Using Python directly:
```bash
uvicorn main:app --reload
```

### Using Docker:
```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`

## API Endpoints

- `GET /`: Welcome message and API status
- `GET /search_food/{query}`: Search for foods matching the query
- `GET /food/{food_id}`: Get detailed information about a specific food

## Dependencies

- FastAPI
- uvicorn
- httpx
- python-dotenv
- Docker (optional)

## Environment Variables

| Variable | Description |
|----------|-------------|
| CLIENT_ID | Your FatSecret API Client ID |
| CLIENT_SECRET | Your FatSecret API Client Secret |

## Development

1. Make sure you have Python 3.9+ installed
2. Install development dependencies
3. Run tests before submitting pull requests
4. Follow PEP 8 style guidelines

## Troubleshooting

If you encounter IP validation errors:
1. Ensure your IP is authorized in the FatSecret Platform
2. Check your `.env` file has correct credentials
3. Verify network connectivity

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```
