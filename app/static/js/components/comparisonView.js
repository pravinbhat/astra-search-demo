import { createBookCard } from './searchResults.js';

export function renderComparisonResults(results, onBookClick) {
    const modes = ['semantic', 'lexical', 'hybrid'];
    
    modes.forEach(mode => {
        const modeResults = results[mode];
        const container = document.querySelector(`.comparison-results-grid[data-mode="${mode}"]`);
        const column = container?.closest('.comparison-column');
        
        if (!container || !column) return;
        
        const countEl = column.querySelector('.comparison-count');
        const timeEl = column.querySelector('.comparison-time');
        
        if (modeResults.error) {
            if (countEl) countEl.textContent = 'Error';
            if (timeEl) timeEl.textContent = '';
            
            container.innerHTML = `
                <div class="comparison-error">
                    <span class="error-icon">⚠️</span>
                    <p>${modeResults.error}</p>
                </div>
            `;
            return;
        }
        
        if (modeResults.message) {
            if (countEl) countEl.textContent = '0 results';
            if (timeEl) timeEl.textContent = '';
            
            container.innerHTML = `
                <div class="comparison-info">
                    <span class="info-icon">ℹ️</span>
                    <p>${modeResults.message}</p>
                </div>
            `;
            return;
        }
        
        const count = modeResults.library_books?.length || 0;
        const total = modeResults.total || 0;
        const time = modeResults.responseTime || 0;
        
        if (countEl) countEl.textContent = `${count} of ${total} results`;
        if (timeEl) timeEl.textContent = `${time}ms`;
        
        container.innerHTML = '';
        
        if (count === 0) {
            container.innerHTML = `
                <div class="comparison-empty">
                    <span class="empty-icon">📭</span>
                    <p>No results</p>
                </div>
            `;
            return;
        }
        
        modeResults.library_books.forEach(book => {
            const card = createBookCard(book, onBookClick);
            container.appendChild(card);
        });
    });
}

export function clearComparisonResults() {
    const containers = document.querySelectorAll('.comparison-results-grid');
    containers.forEach(container => {
        container.innerHTML = '';
        
        const column = container.closest('.comparison-column');
        if (column) {
            const countEl = column.querySelector('.comparison-count');
            const timeEl = column.querySelector('.comparison-time');
            
            if (countEl) countEl.textContent = '';
            if (timeEl) timeEl.textContent = '';
        }
    });
}

export function generateComparisonSummary(results) {
    const summary = {
        totalResults: {},
        responseTimes: {},
        uniqueBooks: new Set()
    };
    
    Object.entries(results).forEach(([mode, modeResults]) => {
        if (modeResults.library_books) {
            summary.totalResults[mode] = modeResults.total || 0;
            summary.responseTimes[mode] = modeResults.responseTime || 0;
            
            modeResults.library_books.forEach(book => {
                summary.uniqueBooks.add(book._id);
            });
        }
    });
    
    return summary;
}

export function displayComparisonSummary(summary) {
    console.log('Comparison Summary:', {
        totalUniqueBooks: summary.uniqueBooks.size,
        resultsByMode: summary.totalResults,
        responseTimesByMode: summary.responseTimes
    });
}
