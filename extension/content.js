// Get the video ID from the YouTube URL
const videoId = window.location.search.split('v=')[1].split('&')[0];

// Fetch the transcript data from the YouTube API
async function fetchTranscript(videoId) {
    const response = await fetch(`https://www.youtube.com/api/timedtext?lang=en&v=${videoId}`);
    const transcript = await response.text();
    
    // Process the transcript to extract sentences and timestamps
    const data = [];
    const regex = /<body>(.*?)<\/body>/g;
    const matches = transcript.match(regex);

    if (matches) {
        matches.forEach(match => {
            const timestamp = match.match(/t="(\d+)"/)[1];
            const text = match.match(/>(.*?)</)[1];
            const time = `${Math.floor(timestamp / 60)}:${timestamp % 60}`;
            data.push({ time, text });
        });
    }

    return data;
}

// Fetch transcript and store it in local storage
fetchTranscript(videoId).then(data => {
    chrome.storage.local.set({ transcriptData: data });
});
