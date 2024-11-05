# ChatPDF

## Description
The ChatPDF is a web-based platform that allows users to upload documents for content extraction and querying. It utilizes FastAPI for the backend and React.js for the frontend, leveraging Unstructured.io for processing and the Gemini API for answering user queries based on document content.

## Tools Used
- **Backend**: FastAPI
- **Frontend**: React.js
- **Styling**: Bootstrap
- **API Requests**: Axios
- **Document Processing**: Unstructured.io
- **Query Processing**: Gemini API
- **Containerization**: Docker

## Setup Instructions

### Prerequisites
- Docker
- Docker Compose

### Getting Started

1. **Clone the Repository**
   ```bash
   git clone git@github.com:mrinshad/ChatPDF.git
   cd ChatPDF
   ```

2. **Create a .env File In the root directory, create a .env file and add the following variables:**

    ```bash
    UNSTRUCTUREDIO_API_KEY=your_unstructured_io_api_key
    GEMINI_API_KEY=your_gemini_api_key
    UNSTRUCTUREDIO_ENDPOINT=https://your_unstructured_io_url
    SUPABASE_URL=https://your_supabase_url
    SUPABASE_KEY=your_supabase_key
    ALLOWED_ORIGINS=http://localhost:3000
    ```

3. **Build and Run the Application Run the following command to build and start the application:**

    ```bash
    docker-compose up --build
    ```

4. **Access the Application**
    - Frontend: http://localhost:3000
    - Backend: http://localhost:8000

Now you should have the Document Processing Application running on your local machine!

Feel free to customize the repository link and any other details specific to your project!