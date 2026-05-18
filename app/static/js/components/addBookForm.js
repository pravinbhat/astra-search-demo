/**
 * Add Book Form Component
 * Handles the modal, form validation, and book creation
 */

import * as API from '../api.js';

class AddBookForm {
    constructor() {
        this.modal = document.getElementById('add-book-modal');
        this.form = document.getElementById('add-book-form');
        this.fab = document.getElementById('add-book-fab');
        this.closeBtn = document.getElementById('modal-close-btn');
        this.cancelBtn = document.getElementById('form-cancel-btn');
        this.checkoutCheckbox = document.getElementById('book-checked-out');
        this.checkoutFields = document.getElementById('checkout-fields');
        this.formStatus = document.getElementById('form-status');
        
        this.init();
    }

    init() {
        // FAB click to open modal
        this.fab?.addEventListener('click', () => this.openModal());
        
        // Close modal handlers
        this.closeBtn?.addEventListener('click', () => this.closeModal());
        this.cancelBtn?.addEventListener('click', () => this.closeModal());
        
        // Close on backdrop click
        this.modal?.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.closeModal();
            }
        });
        
        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !this.modal?.classList.contains('hidden')) {
                this.closeModal();
            }
        });
        
        // Toggle checkout fields
        this.checkoutCheckbox?.addEventListener('change', (e) => {
            this.toggleCheckoutFields(e.target.checked);
        });
        
        // Form submission
        this.form?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });
        
        // Real-time validation
        this.setupValidation();
    }

    openModal() {
        this.modal?.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
        
        // Focus first input
        const firstInput = this.form?.querySelector('input');
        setTimeout(() => firstInput?.focus(), 100);
    }

    closeModal() {
        this.modal?.classList.add('hidden');
        document.body.style.overflow = '';
        this.resetForm();
    }

    toggleCheckoutFields(show) {
        if (show) {
            this.checkoutFields?.classList.remove('hidden');
        } else {
            this.checkoutFields?.classList.add('hidden');
            // Clear checkout fields
            document.getElementById('book-borrower').value = '';
            document.getElementById('book-due-date').value = '';
        }
    }

    setupValidation() {
        const inputs = this.form?.querySelectorAll('input, textarea, select');
        
        inputs?.forEach(input => {
            input.addEventListener('blur', () => {
                this.validateField(input);
            });
            
            input.addEventListener('input', () => {
                // Clear error on input
                const errorId = `${input.id.replace('book-', '')}-error`;
                const errorElement = document.getElementById(errorId);
                if (errorElement) {
                    errorElement.textContent = '';
                }
            });
        });
    }

    validateField(field) {
        const errorId = `${field.id.replace('book-', '')}-error`;
        const errorElement = document.getElementById(errorId);
        
        if (!errorElement) return true;
        
        let errorMessage = '';
        
        // Required field validation
        if (field.hasAttribute('required') && !field.value.trim()) {
            errorMessage = 'This field is required';
        }
        
        // Specific field validations
        if (field.value.trim()) {
            switch (field.id) {
                case 'book-year':
                    const year = parseInt(field.value);
                    if (year < 1000 || year > 9999) {
                        errorMessage = 'Please enter a valid year (1000-9999)';
                    }
                    break;
                    
                case 'book-pages':
                    if (parseInt(field.value) < 1) {
                        errorMessage = 'Pages must be greater than 0';
                    }
                    break;
                    
                case 'book-rating':
                    const rating = parseFloat(field.value);
                    if (rating < 0 || rating > 5) {
                        errorMessage = 'Rating must be between 0 and 5';
                    }
                    break;
                    
                case 'book-title':
                    if (field.value.length > 500) {
                        errorMessage = 'Title must be 500 characters or less';
                    }
                    break;
                    
                case 'book-author':
                    if (field.value.length > 300) {
                        errorMessage = 'Author must be 300 characters or less';
                    }
                    break;
            }
        }
        
        errorElement.textContent = errorMessage;
        return !errorMessage;
    }

    validateForm() {
        const inputs = this.form?.querySelectorAll('input[required], textarea[required], select[required]');
        let isValid = true;
        
        inputs?.forEach(input => {
            if (!this.validateField(input)) {
                isValid = false;
            }
        });
        
        return isValid;
    }

    getFormData() {
        const formData = new FormData(this.form);
        
        // Parse genres from comma-separated string
        const genresString = formData.get('genres');
        const genres = genresString
            .split(',')
            .map(g => g.trim())
            .filter(g => g.length > 0);
        
        // Build metadata object only when at least one value is provided
        const metadataEntries = {
            isbn: formData.get('isbn')?.trim(),
            language: formData.get('language')?.trim(),
            edition: formData.get('edition')?.trim()
        };
        const metadata = Object.fromEntries(
            Object.entries(metadataEntries).filter(([, value]) => value)
        );
        
        // Build book object
        const bookData = {
            title: formData.get('title'),
            author: formData.get('author'),
            number_of_pages: parseInt(formData.get('number_of_pages')),
            rating: parseFloat(formData.get('rating')),
            publication_year: parseInt(formData.get('publication_year')),
            summary: formData.get('summary'),
            genres: genres,
            metadata: Object.keys(metadata).length > 0 ? metadata : null,
            is_checked_out: formData.get('is_checked_out') === 'on',
            borrower: formData.get('borrower') || null,
            due_date: formData.get('due_date') || null
        };
        
        // Generate vectorize text (summary + genres)
        bookData['$vectorize'] = `${bookData.summary} ${genres.join(' ')}`;
        
        return bookData;
    }

    showStatus(message, type) {
        this.formStatus.textContent = message;
        this.formStatus.className = `form-status ${type}`;
        this.formStatus.classList.remove('hidden');
        
        // Auto-hide success messages after 3 seconds
        if (type === 'success') {
            setTimeout(() => {
                this.formStatus.classList.add('hidden');
            }, 3000);
        }
    }

    hideStatus() {
        this.formStatus.classList.add('hidden');
    }

    async handleSubmit() {
        // Validate form
        if (!this.validateForm()) {
            this.showStatus('Please fix the errors before submitting', 'error');
            return;
        }
        
        try {
            // Show loading state
            this.showStatus('Adding book...', 'loading');
            const submitBtn = document.getElementById('form-submit-btn');
            submitBtn.disabled = true;
            
            // Get form data
            const bookData = this.getFormData();
            
            // Call API
            const response = await API.createBook(bookData);
            
            // Show success message
            this.showStatus('Book added successfully!', 'success');
            
            // Reset form and close modal after a short delay
            setTimeout(() => {
                this.closeModal();
                
                // Optionally trigger a refresh of search results
                window.dispatchEvent(new CustomEvent('bookAdded', { detail: response }));
            }, 1500);
            
        } catch (error) {
            console.error('Error adding book:', error);
            this.showStatus(
                error.message || 'Failed to add book. Please try again.',
                'error'
            );
        } finally {
            const submitBtn = document.getElementById('form-submit-btn');
            submitBtn.disabled = false;
        }
    }

    resetForm() {
        this.form?.reset();
        this.hideStatus();
        this.toggleCheckoutFields(false);
        
        // Clear all error messages
        const errorElements = this.form?.querySelectorAll('.form-error');
        errorElements?.forEach(el => el.textContent = '');
    }
}

// Initialize the form when the module is loaded
let addBookFormInstance = null;

export function init() {
    if (!addBookFormInstance) {
        addBookFormInstance = new AddBookForm();
    }
    return addBookFormInstance;
}

export function getFormInstance() {
    return addBookFormInstance;
}

// Made with Bob
