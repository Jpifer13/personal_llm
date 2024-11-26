 
# Text Generation with GPT-2

This project is a web application that uses FastAPI and React to generate text using GPT-2.

## Prerequisites

- Python 3.12^
- Node.js and npm
- Poetry

## Setup and Running

### Backend Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install the required Python packages using Poetry:**

   ```bash
   poetry install
   ```

3. **Activate the virtual environment:**

   ```bash
   poetry shell
   ```

4. **Start the FastAPI backend:**

   ```bash
   uvicorn app:app --reload
   ```

### Frontend Setup

1. **Navigate to the `ui` directory:**

   ```bash
   cd ui
   ```

2. **Install the required Node.js packages:**

   ```bash
   npm install
   ```

3. **Build the React app:**

   ```bash
   npm run build
   cd ..
   ```

### Running the Application

1. **Ensure the backend is running:**

   ```bash
   uvicorn app:app --reload
   ```

2. **Access the application:**

   Open your web browser and go to `http://127.0.0.1:8000/`.

## Notes

- The React app will be served from the FastAPI backend.
- Enter a prompt and see each new generated text response appear in a new text box under the previous responses, with the results container automatically scrolling to the latest response as it is being typed.
