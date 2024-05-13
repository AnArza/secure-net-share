import React from 'react';
import './FileList.css';
import downloadIcon from '../assets/download-icon.svg'; // Ensure the path to the icon is correct

const FileList = ({ files }) => {
  const handleDownload = (fileId, fileName) => {
    const token = localStorage.getItem('token');
    fetch(`/api/files/download/${fileId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    .then(response => {
      if (response.ok) {
        response.blob().then(blob => {
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          const safeFileName = fileName ? fileName.replace('.gz', '') : 'Downloaded_File';
          link.setAttribute('download', safeFileName);  // Use safe file name
          document.body.appendChild(link);
          link.click();
          link.parentNode.removeChild(link);
        });
      } else {
        console.error('Failed to download file');
      }
    })
    .catch(error => {
      console.error('Error downloading file:', error);
    });
  };

  return (
    <ul className="file-list-container">
      {files.map((file, index) => (
        <li key={index} className="file-item">
          <span className="file-name">{file.name ? file.name.replace('.gz', '') : 'Unnamed File'} {file.owner.username}</span>
          <button onClick={() => handleDownload(file.id, file.name)} className="download-button">
            <img src={downloadIcon} alt="Download" className="download-icon"/>
          </button>
        </li>
      ))}
    </ul>
  );
};

export default FileList;
