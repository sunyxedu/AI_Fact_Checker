function sendWebsiteURLToPython() {
    const websiteURL = window.location.href;
    
    fetch('http://localhost:5000/check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: websiteURL })
    })
    .then(response => response.json())
    .then(data => console.log('Response from Python:', data))
    .catch(error => console.error('Error:', error));
}

sendWebsiteURLToPython();
