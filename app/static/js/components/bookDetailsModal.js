/**
 * Book Details Modal Component
 * Displays full book information in a modal when a book card is clicked
 */

import { deleteBook, updateBook } from '../api.js';

let currentModal = null;
let currentModalState = null;
let currentEscapeHandler = null;

// Helper functions for unified score handling
function getVectorSimilarity(book) {
    if (book.$similarity !== undefined && book.$similarity !== null) {
        return book.$similarity;
    }
    if (book.scores && book.scores.$vector !== undefined && book.scores.$vector !== null) {
        return book.scores.$vector;
    }
    return null;
}

function formatSimilarityPercent(similarity) {
    if (similarity === null || similarity === undefined) return null;
    return Math.round(similarity * 100);
}

function escapeHtml(value) {
    return String(value ?? '')
        .replace(/&/g, '&')
        .replace(/</g, '<')
        .replace(/>/g, '>')
        .replace(/"/g, '"')
        .replace(/'/g, '&#x27;');
}

function mergeBookState(existingBook, updatedBook) {
    return {
        ...existingBook,
        ...updatedBook,
        scores: updatedBook.scores ?? existingBook.scores,
        $similarity: updatedBook.$similarity ?? existingBook.$similarity,
    };
}

function renderStarRating(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);

    let stars = '★'.repeat(fullStars);
    if (hasHalfStar) stars += '⯨';
    stars += '☆'.repeat(emptyStars);

    return `<span class="book-rating-large" title="${rating.toFixed(1)} out of 5">${stars} ${rating.toFixed(1)}</span>`;
}

function renderGenres(genres) {
    if (!genres || genres.length === 0) return '<p class="detail-empty">No genres specified</p>';

    return genres
        .map((genre) => `<span class="genre-badge-large">${escapeHtml(genre)}</span>`)
        .join('');
}

function renderCheckoutStatus(book) {
    const metadataHtml = [];

    if (book.metadata?.isbn) {
        metadataHtml.push(`<p><strong>ISBN:</strong> ${escapeHtml(book.metadata.isbn)}</p>`);
    }
    if (book.metadata?.language) {
        metadataHtml.push(`<p><strong>Language:</strong> ${escapeHtml(book.metadata.language)}</p>`);
    }
    if (book.metadata?.edition) {
        metadataHtml.push(`<p><strong>Edition:</strong> ${escapeHtml(book.metadata.edition)}</p>`);
    }

    if (book.is_checked_out) {
        const dueDate = book.due_date ? new Date(book.due_date).toLocaleDateString() : 'Unknown';
        const borrower = book.borrower || 'Unknown';
        return `
            <div class="checkout-info checked-out">
                <div class="checkout-status">
                    <span class="status-icon">⊗</span>
                    <span class="status-text">Checked Out</span>
                </div>
                <div class="checkout-details">
                    <p><strong>Borrower:</strong> ${escapeHtml(borrower)}</p>
                    <p><strong>Due Date:</strong> ${escapeHtml(dueDate)}</p>
                    ${metadataHtml.join('')}
                </div>
            </div>
        `;
    }

    return `
        <div class="checkout-info available">
            <div class="checkout-status">
                <span class="status-icon">✓</span>
                <span class="status-text">Available</span>
            </div>
            ${metadataHtml.length > 0 ? `
                <div class="checkout-details">
                    ${metadataHtml.join('')}
                </div>
            ` : ''}
        </div>
    `;
}

function renderSearchRelevance(book) {
    const similarity = getVectorSimilarity(book);
    const scores = book.scores;

    if (!similarity && !scores) return '';

    let html = '<div class="detail-section"><h3>Search Relevance</h3>';

    if (similarity !== null && !scores) {
        const percent = formatSimilarityPercent(similarity);
        html += `
            <div class="score-detail">
                <div class="score-label">Vector Similarity</div>
                <div class="similarity-bar">
                    <div class="similarity-fill" style="width: ${percent}%"></div>
                </div>
                <p class="similarity-text">${percent}% match</p>
            </div>
        `;
    }

    if (scores && scores.$rerank !== undefined && scores.$rerank !== null) {
        html += `
            <div class="score-detail">
                <div class="score-label">Rerank Score</div>
                <div class="score-value" title="Final relevance adjustment">${scores.$rerank.toFixed(4)}</div>
                <p class="score-description">Final relevance adjustment (lower is better)</p>
            </div>
        `;
    }

    if (scores && scores.$rrf !== undefined && scores.$rrf !== null) {
        html += `
            <div class="score-detail">
                <div class="score-label">RRF Score <span class="info-icon" title="Reciprocal Rank Fusion combines multiple ranking signals">ⓘ</span></div>
                <div class="score-value">${scores.$rrf.toFixed(6)}</div>
                <p class="score-description">Reciprocal Rank Fusion score (lower is better)</p>
            </div>
        `;
    }

    html += '</div>';
    return html;
}

function renderSummarySection(book, isEditMode, formData) {
    if (!isEditMode) {
        return `
            <div class="detail-section">
                <h3>Summary</h3>
                <p class="detail-summary">${escapeHtml(book.summary || 'No summary available')}</p>
            </div>
        `;
    }

    return `
        <div class="detail-section">
            <h3>Summary</h3>
            <label class="detail-form-label" for="book-summary-input">Edit summary</label>
            <textarea id="book-summary-input" name="summary" class="detail-form-control detail-form-textarea" rows="8">${escapeHtml(formData.summary)}</textarea>
        </div>
    `;
}

function renderPublicationSection(book, isEditMode, formData) {
    if (!isEditMode) {
        return `
            <div class="detail-section">
                <h3>Publication Info</h3>
                <div class="detail-info-grid">
                    <div class="info-item">
                        <span class="info-label">Year:</span>
                        <span class="info-value">${escapeHtml(book.publication_year)}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Pages:</span>
                        <span class="info-value">${escapeHtml(book.number_of_pages)}</span>
                    </div>
                </div>
            </div>
        `;
    }

    return `
        <div class="detail-section">
            <h3>Edit Publication Info</h3>
            <div class="detail-edit-grid">
                <div class="detail-edit-field">
                    <label class="detail-form-label" for="book-year-input">Year</label>
                    <input id="book-year-input" name="publication_year" class="detail-form-control" type="number" min="0" step="1" value="${escapeHtml(formData.publication_year)}">
                </div>
                <div class="detail-edit-field">
                    <label class="detail-form-label" for="book-pages-input">Pages</label>
                    <input id="book-pages-input" name="number_of_pages" class="detail-form-control" type="number" min="1" step="1" value="${escapeHtml(formData.number_of_pages)}">
                </div>
            </div>
        </div>
    `;
}

function renderActionBar(state) {
    if (!state.book.id) return '';

    if (state.isEditMode) {
        return `
            <div class="book-details-actions">
                <button type="button" class="detail-action-button secondary" data-action="cancel-edit" ${state.isSaving ? 'disabled' : ''}>Cancel</button>
                <button type="button" class="detail-action-button primary" data-action="save" ${state.isSaving ? 'disabled' : ''}>
                    ${state.isSaving ? 'Saving...' : 'Save Changes'}
                </button>
            </div>
        `;
    }

    return `
        <div class="book-details-actions">
            <button type="button" class="detail-action-button secondary" data-action="edit">Update</button>
            <button type="button" class="detail-action-button danger" data-action="confirm-delete">Delete</button>
        </div>
    `;
}

function renderDeleteConfirm(state) {
    if (!state.showDeleteConfirm) return '';

    return `
        <div class="detail-confirm-overlay" role="dialog" aria-modal="true" aria-labelledby="delete-confirm-title">
            <div class="detail-confirm-modal">
                <h3 id="delete-confirm-title">Delete book?</h3>
                <p>This action will permanently remove <strong>${escapeHtml(state.book.title)}</strong> from the library.</p>
                <div class="detail-confirm-actions">
                    <button type="button" class="detail-action-button secondary" data-action="cancel-delete" ${state.isDeleting ? 'disabled' : ''}>Cancel</button>
                    <button type="button" class="detail-action-button danger" data-action="delete" ${state.isDeleting ? 'disabled' : ''}>
                        ${state.isDeleting ? 'Deleting...' : 'Delete'}
                    </button>
                </div>
            </div>
        </div>
    `;
}

function createBookDetailsModal(state) {
    const { book, isEditMode, feedback, error, formData } = state;
    const modal = document.createElement('div');
    modal.className = 'book-details-modal';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-labelledby', 'book-details-title');
    modal.setAttribute('aria-modal', 'true');

    modal.innerHTML = `
        <div class="book-details-backdrop"></div>
        <div class="book-details-container">
            <div class="book-details-header">
                <div>
                    <h2 id="book-details-title" class="book-details-title">${escapeHtml(book.title)}</h2>
                    ${isEditMode ? '<p class="book-details-subtitle">Edit selected fields for this book</p>' : ''}
                </div>
                <button class="book-details-close" aria-label="Close book details">
                    <span>✕</span>
                </button>
            </div>

            ${feedback ? `<div class="detail-status-message success">${escapeHtml(feedback)}</div>` : ''}
            ${error ? `<div class="detail-status-message error">${escapeHtml(error)}</div>` : ''}
            ${renderActionBar(state)}

            <div class="book-details-content">
                <div class="book-details-main">
                    <div class="detail-section">
                        <h3>Author</h3>
                        <p class="detail-author">${escapeHtml(book.author)}</p>
                    </div>

                    ${renderSummarySection(book, isEditMode, formData)}

                    <div class="detail-section">
                        <h3>Genres</h3>
                        <div class="detail-genres">
                            ${renderGenres(book.genres)}
                        </div>
                    </div>

                    <div class="detail-section">
                        <h3>Availability</h3>
                        ${renderCheckoutStatus(book)}
                    </div>
                </div>

                <div class="book-details-sidebar">
                    <div class="detail-section">
                        <h3>Rating</h3>
                        ${renderStarRating(book.rating)}
                    </div>

                    ${renderPublicationSection(book, isEditMode, formData)}

                    ${renderSearchRelevance(book)}

                    ${book.id ? `
                        <div class="detail-section">
                            <h3>Book ID</h3>
                            <p class="detail-id">${escapeHtml(book.id)}</p>
                        </div>
                    ` : ''}
                </div>
            </div>
            ${renderDeleteConfirm(state)}
        </div>
    `;

    return modal;
}

function getInitialState(book, options = {}) {
    return {
        book,
        options,
        isEditMode: false,
        isSaving: false,
        isDeleting: false,
        showDeleteConfirm: false,
        feedback: '',
        error: '',
        formData: {
            summary: book.summary || '',
            publication_year: book.publication_year ?? '',
            number_of_pages: book.number_of_pages ?? '',
        },
    };
}

function rerenderModal() {
    if (!currentModalState || !currentModal) return;

    const isActive = currentModal.classList.contains('active');
    const newModal = createBookDetailsModal(currentModalState);

    if (isActive) {
        newModal.classList.add('active');
    }

    currentModal.replaceWith(newModal);
    currentModal = newModal;
    attachModalEventListeners();
}

function attachModalEventListeners() {
    if (!currentModal || !currentModalState) return;

    const closeBtn = currentModal.querySelector('.book-details-close');
    const backdrop = currentModal.querySelector('.book-details-backdrop');

    closeBtn?.addEventListener('click', closeBookDetails);
    backdrop?.addEventListener('click', () => {
        if (!currentModalState.showDeleteConfirm) {
            closeBookDetails();
        }
    });

    currentModal.querySelector('[data-action="edit"]')?.addEventListener('click', () => {
        currentModalState.isEditMode = true;
        currentModalState.feedback = '';
        currentModalState.error = '';
        rerenderModal();
        currentModal.querySelector('#book-summary-input')?.focus();
    });

    currentModal.querySelector('[data-action="cancel-edit"]')?.addEventListener('click', () => {
        currentModalState.isEditMode = false;
        currentModalState.error = '';
        currentModalState.formData = {
            summary: currentModalState.book.summary || '',
            publication_year: currentModalState.book.publication_year ?? '',
            number_of_pages: currentModalState.book.number_of_pages ?? '',
        };
        rerenderModal();
    });

    currentModal.querySelector('[data-action="save"]')?.addEventListener('click', handleSave);
    currentModal.querySelector('[data-action="confirm-delete"]')?.addEventListener('click', () => {
        currentModalState.showDeleteConfirm = true;
        currentModalState.error = '';
        rerenderModal();
    });
    currentModal.querySelector('[data-action="cancel-delete"]')?.addEventListener('click', () => {
        currentModalState.showDeleteConfirm = false;
        rerenderModal();
    });
    currentModal.querySelector('[data-action="delete"]')?.addEventListener('click', handleDelete);
}

function validateFormData(formData) {
    const publicationYear = Number(formData.publication_year);
    const numberOfPages = Number(formData.number_of_pages);

    if (!Number.isInteger(publicationYear) || publicationYear < 0) {
        return 'Publication year must be a valid non-negative number.';
    }

    if (!Number.isInteger(numberOfPages) || numberOfPages < 1) {
        return 'Pages must be a valid positive whole number.';
    }

    return '';
}

async function handleSave() {
    if (!currentModalState?.book?.id || currentModalState.isSaving) return;

    const summaryInput = currentModal.querySelector('#book-summary-input');
    const yearInput = currentModal.querySelector('#book-year-input');
    const pagesInput = currentModal.querySelector('#book-pages-input');

    const formData = {
        summary: summaryInput?.value.trim() ?? '',
        publication_year: yearInput?.value ?? '',
        number_of_pages: pagesInput?.value ?? '',
    };

    const validationError = validateFormData(formData);
    if (validationError) {
        currentModalState.error = validationError;
        currentModalState.feedback = '';
        currentModalState.formData = formData;
        rerenderModal();
        return;
    }

    currentModalState.isSaving = true;
    currentModalState.error = '';
    currentModalState.feedback = '';
    currentModalState.formData = formData;
    rerenderModal();

    try {
        const updatedBook = await updateBook(currentModalState.book.id, {
            summary: formData.summary,
            publication_year: Number(formData.publication_year),
            number_of_pages: Number(formData.number_of_pages),
        });

        currentModalState.book = mergeBookState(currentModalState.book, updatedBook);
        currentModalState.isEditMode = false;
        currentModalState.isSaving = false;
        currentModalState.feedback = 'Book updated successfully.';
        currentModalState.formData = {
            summary: currentModalState.book.summary || '',
            publication_year: currentModalState.book.publication_year ?? '',
            number_of_pages: currentModalState.book.number_of_pages ?? '',
        };

        if (typeof currentModalState.options?.onBookUpdated === 'function') {
            currentModalState.options.onBookUpdated(currentModalState.book);
        }

        rerenderModal();
    } catch (error) {
        currentModalState.isSaving = false;
        currentModalState.error = error.message || 'Failed to update book.';
        rerenderModal();
    }
}

async function handleDelete() {
    if (!currentModalState?.book?.id || currentModalState.isDeleting) return;

    currentModalState.isDeleting = true;
    currentModalState.error = '';
    rerenderModal();

    try {
        await deleteBook(currentModalState.book.id);

        if (typeof currentModalState.options?.onBookDeleted === 'function') {
            currentModalState.options.onBookDeleted(currentModalState.book.id);
        }

        closeBookDetails();
    } catch (error) {
        currentModalState.isDeleting = false;
        currentModalState.error = error.message || 'Failed to delete book.';
        rerenderModal();
    }
}

export function showBookDetails(book, options = {}) {
    closeBookDetails();

    currentModalState = getInitialState(book, options);

    const modal = createBookDetailsModal(currentModalState);
    document.body.appendChild(modal);
    currentModal = modal;

    document.body.style.overflow = 'hidden';

    attachModalEventListeners();

    currentEscapeHandler = (e) => {
        if (e.key !== 'Escape') return;

        if (currentModalState?.showDeleteConfirm) {
            currentModalState.showDeleteConfirm = false;
            rerenderModal();
            return;
        }

        closeBookDetails();
    };

    document.addEventListener('keydown', currentEscapeHandler);

    requestAnimationFrame(() => {
        modal.classList.add('active');
    });

    modal.querySelector('.book-details-close')?.focus();
}

export function closeBookDetails() {
    if (!currentModal) return;

    if (currentEscapeHandler) {
        document.removeEventListener('keydown', currentEscapeHandler);
        currentEscapeHandler = null;
    }

    const modalToClose = currentModal;
    currentModal.classList.remove('active');

    setTimeout(() => {
        if (modalToClose && modalToClose.parentNode) {
            modalToClose.parentNode.removeChild(modalToClose);
        }
    }, 300);

    currentModal = null;
    currentModalState = null;
    document.body.style.overflow = '';
}

export function init() {
    console.log('Book Details Modal component initialized');
}

// Made with Bob
