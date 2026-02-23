async function getRecommendations() {
    const input = document.getElementById('userInput').value;
    const resultsDiv = document.getElementById('results');
    const loader = document.getElementById('loader');

    if (!input) return alert("Tell me something about your mood!");

    loader.classList.remove('hidden');
    resultsDiv.innerHTML = '';

    try {
        const response = await fetch('/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ preferences: input })
        });

        const data = await response.json();
        loader.classList.add('hidden');

        // NEW: Check if the backend sent an error message
        if (!response.ok) {
            resultsDiv.innerHTML = `<p style="color: #ff6b6b;"><strong>Backend Error:</strong> ${data.error}</p>`;
            return;
        }

        // If no error, render the movies!
        data.forEach(movie => {
            resultsDiv.innerHTML += `
                <div class="movie-card">
                    <h3>${movie.title} (${movie.year})</h3>
                    <p><strong>Genre:</strong> ${movie.genre}</p>
                    <p><em>${movie.reason}</em></p>
                </div>
            `;
        });
    } catch (e) {
        loader.classList.add('hidden');
        resultsDiv.innerHTML = `<p style="color: #ff6b6b;">A frontend error occurred: ${e.message}</p>`;
    }
}