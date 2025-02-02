chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "checkYouTubeVideo") {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            let url = tabs[0].url;
            let videoId = new URL(url).searchParams.get("v");

            if (videoId) {
                fetch(`http://127.0.0.1:5000/fact-check/${videoId}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.is_misinformation) {
                            alert("Misinformation found! Details are in the terminal.");
                        } else {
                            chrome.storage.local.set({ factCheckResult: "Checked: Correct" });
                        }
                    });
            }
        });
    }
});
