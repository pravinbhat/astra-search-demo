function renderStarRating(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
    
    let stars = '★'.repeat(fullStars);
    if (hasHalfStar) stars += '⯨';
    stars += '☆'.repeat(emptyStars);
    
    return `<span class="book-rating" title="${rating.toFixed(1)} out of 5">${stars} ${rating.toFixed(1)}</span>`;
}

function renderGenres(genres) {
    if (!genres || genres.length === 0) return '';
    
    return genres
        .slice(0, 3) // Show max 3 genres
        .map(genre => `<span class="genre-badge">${genre}</span>`)
        .join('');
}

function truncateText(text, maxLength = 150) {
    if (!text || text.length <= maxLength) return text;
    return text.substring(0, maxLength).trim() + '...';
}

function renderCheckoutStatus(book) {
    if (book.is_checked_out) {
        const dueDate = book.due_date ? new Date(book.due_date).toLocaleDateString() : 'Unknown';
        return `
            <span class="book-status checked-out" title="Due: ${dueDate}">
                ⊗ Checked Out
            </span>
        `;
    }
    return '<span class="book-status available">✓ Available</span>';
}

function renderSimilarity(similarity) {
    if (similarity === undefined || similarity === null) return '';
    return `<span class="book-similarity">Similarity: ${(similarity * 100).toFixed(0)}%</span>`;
}

export function createBookCard(book, onClickHandler) {
    const card = document.createElement('div');
    card.className = 'book-card';
    card.dataset.bookId = book._id;
    card.setAttribute('role', 'button');
    card.setAttribute('tabindex', '0');
    card.setAttribute('aria-label', `View details for ${book.title} by ${book.author}`);
    const similarity = book.$similarity;
    
    card.innerHTML = `
        <h3 class="book-title">${book.title}</h3>
        <p class="book-author">by ${book.author}</p>
        
        <div class="book-meta">
            ${renderStarRating(book.rating)}
            <span>${book.publication_year}</span>
            <span>${book.number_of_pages} pages</span>
        </div>
        
        <div class="book-genres">
            ${renderGenres(book.genres)}
        </div>
        
        <p class="book-summary">${truncateText(book.summary, 200)}</p>
        
        <div class="book-footer">
            ${renderCheckoutStatus(book)}
            ${renderSimilarity(similarity)}
        </div>
    `;
    
    // Add click handler
    if (onClickHandler) {
        card.addEventListener('click', () => onClickHandler(book));
        card.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                onClickHandler(book);
            }
        });
    }
    
    return card;
}

export function renderResults(container, books, total, responseTime, onBookClick) {
    container.innerHTML = '';
    
    if (!books || books.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">📭</span>
                <h3>No Results Found</h3>
                <p>Try adjusting your search criteria or filters</p>
            </div>
        `;
        return;
    }
    
    const resultsTitle = document.getElementById('results-title');
    const resultsCount = document.getElementById('results-count');
    const resultsTimeEl = document.getElementById('results-time');
    
    if (resultsTitle) {
        resultsTitle.textContent = 'Search Results';
    }
    
    if (resultsCount) {
        resultsCount.textContent = `${books.length} of ${total} results`;
    }
    
    if (resultsTimeEl && responseTime !== undefined) {
        resultsTimeEl.textContent = `${responseTime}ms`;
    }
    
    books.forEach(book => {
        container.appendChild(createBookCard(book, onBookClick));
    });
}

export function showLoading() {
    const loadingState = document.getElementById('loading-state');
    const emptyState = document.getElementById('empty-state');
    const errorState = document.getElementById('error-state');
    const resultsContainer = document.getElementById('results-container');
    
    if (loadingState) loadingState.classList.remove('hidden');
    if (emptyState) emptyState.classList.add('hidden');
    if (errorState) errorState.classList.add('hidden');
    if (resultsContainer) resultsContainer.classList.add('hidden');
}

export function hideLoading() {
    const loadingState = document.getElementById('loading-state');
    if (loadingState) loadingState.classList.add('hidden');
}

export function showError(message) {
    const errorState = document.getElementById('error-state');
    const errorMessage = document.getElementById('error-message');
    const emptyState = document.getElementById('empty-state');
    const resultsContainer = document.getElementById('results-container');
    
    if (errorMessage) errorMessage.textContent = message;
    if (errorState) errorState.classList.remove('hidden');
    if (emptyState) emptyState.classList.add('hidden');
    if (resultsContainer) resultsContainer.classList.add('hidden');
}

export function showResults() {
    const resultsContainer = document.getElementById('results-container');
    const emptyState = document.getElementById('empty-state');
    const errorState = document.getElementById('error-state');
    const singleResults = document.getElementById('single-results');
    const comparisonResults = document.getElementById('comparison-results');
    
    if (resultsContainer) resultsContainer.classList.remove('hidden');
    if (emptyState) emptyState.classList.add('hidden');
    if (errorState) errorState.classList.add('hidden');
    
    if (singleResults) singleResults.classList.remove('hidden');
    if (comparisonResults) comparisonResults.classList.add('hidden');
}

export function showComparisonResults() {
    const resultsContainer = document.getElementById('results-container');
    const emptyState = document.getElementById('empty-state');
    const errorState = document.getElementById('error-state');
    const singleResults = document.getElementById('single-results');
    const comparisonResults = document.getElementById('comparison-results');
    
    if (resultsContainer) resultsContainer.classList.remove('hidden');
    if (emptyState) emptyState.classList.add('hidden');
    if (errorState) errorState.classList.add('hidden');
    
    if (singleResults) singleResults.classList.add('hidden');
    if (comparisonResults) comparisonResults.classList.remove('hidden');
}

export function showEmptyState() {
    const emptyState = document.getElementById('empty-state');
    const errorState = document.getElementById('error-state');
    const resultsContainer = document.getElementById('results-container');
    
    if (emptyState) emptyState.classList.remove('hidden');
    if (errorState) errorState.classList.add('hidden');
    if (resultsContainer) resultsContainer.classList.add('hidden');
}

export function clearResults() {
    const resultsGrid = document.getElementById('results-grid');
    if (resultsGrid) {
        resultsGrid.innerHTML = '';
    }
    showEmptyState();
}

export function scrollToResults() {
    const resultsSection = document.getElementById('results-section');
    if (resultsSection) {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}
