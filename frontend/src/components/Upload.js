import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import Spinner from 'react-bootstrap/Spinner'; // Import Spinner from react-bootstrap

axios.defaults.baseURL = 'http://localhost:8000'; // Set base URL for API requests

const Upload = () => {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false); // State to manage loading
    const navigate = useNavigate(); // Initialize useNavigate

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', file);
        setLoading(true); // Set loading to true

        try {
            const response = await axios.post('/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            // Navigate to the chat page with the document_id after successful upload
            navigate(`/chat/${response.data.document_id}`);
        } catch (error) {
            console.error('Error uploading file:', error);
        } finally {
            setLoading(false); // Reset loading state
        }
    };

    return (
        <div className="container mt-5">
            <h2>Upload Document</h2>
            {loading ? ( // Show loading spinner when loading
                <div className="text-center">
                    <Spinner animation="border" role="status">
                        <span className="visually-hidden">Processing your document...</span>
                    </Spinner>
                    <p>Processing your document...</p>
                </div>
            ) : (
                <form onSubmit={handleUpload}>
                    <div className="mb-3">
                        <input type="file" onChange={handleFileChange} className="form-control" required />
                    </div>
                    <button type="submit" className="btn btn-success">Upload</button>
                </form>
            )}
        </div>
    );
};

export default Upload;
