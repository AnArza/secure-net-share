import React, { useState, useEffect } from 'react';
import './RecipientSelector.css';

const RecipientSelector = ({ user, onSelect, token }) => {
    const [recipients, setRecipients] = useState([]);
    const [selectedRecipients, setSelectedRecipients] = useState([]);
    const baseWebsocketUrl = 'ws://localhost:8002';

    useEffect(() => {
        if (user) {
            const ws = new WebSocket(`${baseWebsocketUrl}/ws/status/?username=${user}`);
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                console.log('Received data:', data);
                if (data.type === 'active_users') {
                    setRecipients(data.users);
                }
            };
            return () => ws.close();
        }
    }, [user]);

      const handleShare = () => {
        fetch('/api/files/share/', {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ shared_with: selectedRecipients })
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Failed to update share settings');
        })
        .then(data => {
            console.log('Share update successful:', data);
            // what to do here?
        })
        .catch(error => {
            console.error('Error sharing file:', error);
            alert('Failed to share file: ' + error.message);
        });
      };

    const handleSelect = (event) => {
        const selectedOptions = Array.from(event.target.selectedOptions, option => option.value);
        setSelectedRecipients(selectedOptions);
        onSelect(selectedOptions);
    };

    return (
        <div className="recipient-selector-container">
            <label htmlFor="recipient-selector">Available recipients:</label>
            <select multiple id="recipient-selector" onChange={handleSelect} value={selectedRecipients} className="recipient-selector">
                {recipients.map(recipient => (
                    <option key={recipient.user.username} value={recipient.user.username}>
                        {recipient.user.username}
                    </option>
                ))}
            </select>
            <button onClick={handleShare} className="share-button">Share</button>
        </div>
    );
};

export default RecipientSelector;
