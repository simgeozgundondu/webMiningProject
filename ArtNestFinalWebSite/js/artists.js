
async function fetchArtists() {
    try {
        const response = await fetch('./json/artists.json');
        const artists = await response.json();
        return artists;
    } catch (error) {
        console.error('Error fetching artists:', error);
        return [];
    }
}

async function populateArtists() {
    const artistsData = await fetchArtists();
    const categoriesContainer = document.getElementById('categories-container');

    try {
        // Create artist buttons for the category
        const artistButtonsContainer = document.createElement('div');
        artistButtonsContainer.classList.add('artist-buttons-container');
        artistsData.forEach(artistItem => {
            const artistButton = document.createElement('button');
            artistButton.setAttribute('type', 'button');
            artistButton.classList.add('btn', 'btn-dark');

            // Create and add image element
            const artistImage = document.createElement('img');
            artistImage.classList.add("artistImg")
            artistImage.src = artistItem.artist_img;
            artistImage.alt = 'Loading...';
            artistImage.style.width = '300px';
            artistImage.style.height = '380px';
            artistImage.style.marginBottom='10px';
            artistButton.appendChild(artistImage);// Append the image to the button

            // Create a paragraph element for artist name
            const artistNameParagraph = document.createElement('h5');
            artistNameParagraph.textContent = artistItem.ArtistName;
            artistButton.appendChild(artistNameParagraph);



            artistButton.addEventListener('click', async () => {

                // Sanatçı bilgilerini sanatçı adına göre bul
                const artistInfo = artistsData.find(artist => artist.ArtistName === artistButton.textContent);

                if (artistInfo) {
                    const params = new URLSearchParams({
                        artistName: artistInfo.ArtistName,
                        date: artistInfo.Date,
                        nationality: artistInfo.Nationality,
                        bio: artistInfo.Bio,
                        artworks: JSON.stringify(artistInfo.Artworks),
                        artistImage: artistInfo.artist_img
                    });

                    window.location.href = `./artistDetail.html?${params.toString()}`;
                } else {
                    console.error(`Artist '${artistName}' not found in the database.`);
                }
            });


            artistButtonsContainer.appendChild(artistButton);
        });

        categoriesContainer.appendChild(artistButtonsContainer);

    } catch (error) {
        console.error('Error populating artists:', error);
    }
}


document.addEventListener('DOMContentLoaded', async function () {


    const urlParams = new URLSearchParams(window.location.search);
    const artistName = urlParams.get('artistName');
    const date = urlParams.get('date');
    const nationality = urlParams.get('nationality');
    const bio = urlParams.get('bio');
    const artworks = urlParams.get('artworks');
    const artistImage = urlParams.get('artistImage');

    if (artistName) {
        // Update HTML content with artist information
        const artistNameElement = document.getElementById('artistName');
        artistNameElement.textContent = `${artistName}`;

        const dateElement = document.getElementById('date');
        if (date) {
            dateElement.textContent = `Date: ${date}`;
        }

        const nationalityElement = document.getElementById('nationality');
        if (nationality) {
            nationalityElement.textContent = `Nationality: ${nationality}`;
        }

        const bioElement = document.getElementById('bio');
        if (bio) {
            bioElement.textContent = `${bio}`;
        }
        const artistImageElement = document.getElementById('artistImage');
        if (artistImage) {
            artistImageElement.src = artistImage;
        }

        if (artworks) {
            // Convert artworks (which is a JSON string) back to an array
            const artworksArray = JSON.parse(artworks);
            // Display artwork names side by side
            const artworkNamesContainer = document.getElementById('artworkNamesContainer');
            artworkNamesContainer.textContent = "Artworks:";
            artworksArray.forEach(artwork => {
                const artworkNameElement = document.createElement('span');
                artworkNameElement.textContent = artwork;
                artworkNameElement.classList.add('artwork-name');
                artworkNamesContainer.appendChild(artworkNameElement);
            });
        }

    }

    // Add event listener to search input for real-time filtering
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', filterArtists);
});
// Function to filter artist buttons based on search input
function filterArtists() {
    const searchInput = document.getElementById('searchInput');
    const searchText = searchInput.value.trim().toLowerCase();
    const artistButtons = document.querySelectorAll('.artist-buttons-container button');

    // Loop through each artist button to check for match
    artistButtons.forEach(button => {
        const artistName = button.textContent.toLowerCase();
        const categorySection = button.closest('.category-section');

        // Toggle visibility based on search match
        if (artistName.includes(searchText)) {
            button.style.display = 'block';
            categorySection.style.display = 'block'; 
        } else {
            button.style.display = 'none';
            const visibleButtons = categorySection.querySelectorAll('.artist-buttons-container button[style="display: block;"]');
            if (visibleButtons.length === 0) {
                categorySection.style.display = 'none'; // Hide category section if no buttons are visible
            }
        }
    });
}


// Call the function to populate the gallery
populateArtists();
