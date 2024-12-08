// Event Listener for Icon Button Click
document.getElementById('iconBtn').addEventListener('click', uploadImage);

function uploadImage() {
    const input = document.getElementById('imageUpload');
    const file = input.files[0];

    if (!file) {
        alert("Please select an image first.");
        return;
    }

    // Display image preview
    const imagePreview = document.getElementById('imagePreview');
    const imagePreviewContainer = document.getElementById('imagePreviewContainer');
    const reader = new FileReader();

    reader.onload = function(e) {
        imagePreview.src = e.target.result;
        imagePreview.style.display = 'block';
        imagePreviewContainer.style.display = 'flex';  // Show image container
    };

    reader.readAsDataURL(file); // Read the image file as a data URL

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => displayColors(data.colors, data.image_url))
    .catch(error => console.error('Error:', error));
}

function displayColors(colors, imageUrl) {
    const colorResultsDiv = document.getElementById('colorResults');
    const imagePreview = document.getElementById('imagePreview');

    // Show the uploaded image preview
    imagePreview.src = imageUrl;

    // Clear previous results
    colorResultsDiv.innerHTML = '';

    colors.forEach(color => {
        const colorSwatch = document.createElement('div');
        colorSwatch.style.backgroundColor = color;
        colorSwatch.classList.add('color-swatch');

        const colorText = document.createElement('p');
        colorText.textContent = color;

        colorSwatch.appendChild(colorText);
        colorResultsDiv.appendChild(colorSwatch);
    });
}
