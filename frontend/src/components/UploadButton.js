import React from 'react';
import './UploadButton.css';

const UploadButton = ({ onUpload }) => {
  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) {
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    onUpload(formData, file);
  };

  return (
    <label className="file-upload">
      <input type="file" onChange={handleFileChange} />
      Upload File
    </label>
  );
};

export default UploadButton;
