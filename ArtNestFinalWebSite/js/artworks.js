// Function to fetch JSON data from a URL
async function fetchArtworks() {
    try {
        const response = await fetch('./json/artworks.json');
        const artworks = await response.json();
        return artworks;
    } catch (error) {
        console.error('Error fetching artworks:', error);
        return [];
    }
}

// Function to create a card for each artwork
function createCard(artwork) {
    // Create a card element
    const card = document.createElement('div');
    card.classList.add('card', 'card-hover', 'h-100');

    // Create the card body
    const cardBody = document.createElement('div');
    cardBody.classList.add('card-body');

    // Create the image element
    const img = document.createElement('img');
    img.classList.add('card-img-top');
    img.src = artwork.image_url;
    img.alt = artwork.artwork;

    // Create the reveal div with artwork information
    const revealDiv = document.createElement('div');
    revealDiv.classList.add('reveal', 'h-100', 'p-2', 'd-flex');
    revealDiv.innerHTML = `<div class="w-100 align-self-center"><p>${artwork.artwork + " - " + artwork.artist}</p></div>`;

    // Add click event listener to each card
    card.addEventListener('click', () => {
        // Redirect to about copy.html with artwork information as query parameter
        const artworkInfo = {
            artwork: artwork.artwork,
            artist: artwork.artist,
            price: artwork.price,
            place: artwork.place,
            artworkDate: artwork.artwork_date,
            artworkImage: artwork.image_url
        };
        const params = new URLSearchParams(artworkInfo);
        window.location.href = `artworkDetail.html?${params.toString()}`;
    });

    // Append elements to the card body
    cardBody.appendChild(img);
    cardBody.appendChild(revealDiv);

    // Append card body to the card
    card.appendChild(cardBody);

    return card;
}

// Function to populate the gallery with artworks
async function populateGallery(filter = '') {
    const galleryContainer = document.getElementById('gallery');
    galleryContainer.innerHTML = ''; // Clear existing gallery

    // Fetch artworks data
    const artworks = await fetchArtworks();

    // Filter artworks based on the search input
    const filteredArtworks = artworks.filter(artwork =>
        artwork.artwork.toLowerCase().includes(filter.toLowerCase())
    );

    // Loop through each filtered artwork and create gallery cards
    filteredArtworks.forEach(artwork => {
        const card = createCard(artwork);
        galleryContainer.appendChild(card);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const artwork = urlParams.get('artwork');
    const artist = urlParams.get('artist');
    const price = urlParams.get('price');
    const place = urlParams.get('place');
    const artworkDate = urlParams.get('artworkDate');
    const artworkImage = urlParams.get('artworkImage');

    if (artwork && artist) {
        // Update HTML content with artwork and artist information
        const artworkTitleElement = document.getElementById('artworkTitle');
        const artistNameElement = document.getElementById('artistName');
        const priceElement = document.getElementById('price');
        const placeElement = document.getElementById('place');
        const artworkDateElement = document.getElementById('artworkDate');
        const artworkImageElement = document.getElementById('artworkImage');

        artworkTitleElement.textContent = artwork;
        artistNameElement.textContent = `Artist: ${artist}`;
        artworkImageElement.src = artworkImage;

        if (price) {
            priceElement.textContent = `Price: ${price}`;
        }
        if (place) {
            placeElement.textContent = `Place: ${place}`;
        }
        if (artworkDate) {
            artworkDateElement.textContent = `Artwork Date: ${artworkDate}`;
        }
    }

    // Initialize gallery with all artworks
    populateGallery();

    // Add event listener to the search box
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', () => {
        const filter = searchInput.value;
        populateGallery(filter);
    });
});

// Call the function to populate the gallery
populateGallery();

