import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import FileList from '../components/FileList';
import UploadButton from '../components/UploadButton';
import RecipientSelector from '../components/RecipientSelector';
import './Home.css';

const Home = ({ token, onLogout }) => {
    const [files, setFiles] = useState([]);
    const [currentUser, setCurrentUser] = useState({ username: '', id: null });
    const [selectedUsers, setSelectedUsers] = useState([]);
    const baseWebsocketUrl = 'ws://localhost:8002';

    useEffect(() => {
        if (token) {
            fetch('/api/current-user/', {
                headers: { 'Authorization': `Bearer ${token}` }
            })
            .then(response => response.json())
            .then(data => setCurrentUser(data.user))
            .catch(error => console.error('Error fetching current user:', error));
        }
    }, [token]);

    useEffect(() => {
        if (currentUser.username) {
            const ws = new WebSocket(`${baseWebsocketUrl}/ws/files/?username=${currentUser.username}`);
            ws.onmessage = event => {
                const data = JSON.parse(event.data);
                console.log('Received files:', data)
                switch (data.type) {
                    case 'files_list':
                        setFiles(data.files); break;
                    case 'file_uploaded':
                        setFiles(prev => [...prev, data.file]); break;
                    case 'file_deleted':
                        setFiles(prev => prev.filter(file => file.id !== data.file_id)); break;
                    case 'file_updated':
                        setFiles(prevFiles => {
                            const existingFileMap = new Map(prevFiles.map(file => [file.id, file]));

                            data.data.forEach(updatedFile => {
                                existingFileMap.set(updatedFile.id, updatedFile);
                            });

                            return Array.from(existingFileMap.values());
                        });
                        break;
                    default: break;
                }
            };
            return () => ws.close();
        }
    }, [currentUser.username]);


    const handleUpload = (formData, file) => {
      if (token) {
        fetch('/api/files/upload/', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
          body: formData
        })
        .then(response => {
          if (response.ok) {
            return response.json();
          }
          throw new Error('Failed to upload file');
        })
        .then(data => {
          console.log('File uploaded successfully:', data);
        })
        .catch(error => {
          console.error('Error uploading file:', error);
        });
      }
    };

    const handleSelectedUsersChange = (selectedIds) => {
        setSelectedUsers(selectedIds);
    };

    return (
        <div className="home">
            <Header user={currentUser.username} onLogout={onLogout} />
            <main className="home-content">
                <RecipientSelector token={token} user={currentUser.username} onSelect={handleSelectedUsersChange} />
                <UploadButton onUpload={handleUpload} />
                <FileList files={files} />
            </main>
        </div>
    );
};

export default Home;
