// Function to check if user agent is iOS
function isiOS() {
    return /iPhone|iPad|iPod/i.test(navigator.userAgent);
}

// Function to check if user agent is Android
function isAndroid() {
    return /Android/i.test(navigator.userAgent);
}

function editStartUrlAndGenerateDataUrl(manifestUrl, newStartUrl) {
    // Fetch the manifest.json file
    return fetch(manifestUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Check if start_url exists in the manifest
        if (data.start_url) {
            originalStartUrl = data.start_url;
            // Edit the start_url
            data.start_url = newStartUrl;

            // Convert the updated data back to JSON
            const updatedManifest = JSON.stringify(data);

            // Generate Data URL from updated JSON content
            const dataUrl = 'data:application/manifest+json;charset=utf-8,' + encodeURIComponent(updatedManifest);
            // Log the generated Data URL
            console.log('Generated Data URL:', dataUrl);
            return dataUrl;
        } else {
            console.error('start_url not found in manifest.json');
            throw new Error('start_url not found in manifest.json');
        }
    })
    .catch(error => {
        console.error('Error fetching or updating manifest.json:', error);
        return Promise.reject(error);
    });
}

// Example usage
if (isiOS()) {
    // Perform iOS-specific action
    console.log("User is using iOS");
    editStartUrlAndGenerateDataUrl("./assets/manifest.json", "")
        .then(dataUrlOrStartUrl => {
            document.querySelector("head > link").href = dataUrlOrStartUrl;
            console.log('Generated Data URL:', dataUrlOrStartUrl);
        })
        .catch(error => {
            console.error('Error:', error);
        });
} else if (isAndroid()) {
    // Perform Android-specific action
    console.log("User is using Android");
    // Your Android specific code here
} else {
    // Perform action for other user agents
    console.log("User is using some other platform");
    // Your generic code here
    editStartUrlAndGenerateDataUrl("./assets/manifest.json", "")
        .then(dataUrlOrStartUrl => {
            document.querySelector("head > link").href = dataUrlOrStartUrl;
            console.log('Generated Data URL:', dataUrlOrStartUrl);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}