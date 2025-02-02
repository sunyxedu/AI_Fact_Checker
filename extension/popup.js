async function fetchFactCheckData() {
    try {
        const response = await fetch('http://localhost:5000/factcheck');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        const imageElement = document.getElementById('warningImage');
        
        if (!imageElement) {
            console.error("Error: Image element with ID 'resultImage' not found in the DOM.");
            return;
        }

        if (data.is_misinformation) {  
            imageElement.src = 'WARNING.png';
            imageElement.style.display = 'block';
        } else {
            document.body.innerText = 'Checked: Correct';
        }

    } catch (error) {
        console.error('Error fetching fact-check data:', error);
    }
}

fetchFactCheckData();
