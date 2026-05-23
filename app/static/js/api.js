const API_BASE_URL = '/api/library-books';

class APIError extends Error {
    constructor(message, status, data) {
        super(message);
        this.name = 'APIError';
        this.status = status;
        this.data = data;
    }
}

async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const config = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new APIError(
                data.detail || 'An error occurred',
                response.status,
                data
            );
        }
        
        return data;
    } catch (error) {
        if (error instanceof APIError) {
            throw error;
        }
        
        throw new APIError(
            error.message || 'Network error occurred',
            0,
            null
        );
    }
}

export async function searchBooks(searchParams) {
    const startTime = performance.now();
    
    try {
        const result = await apiRequest('/search', {
            method: 'POST',
            body: JSON.stringify(searchParams),
        });
        
        const endTime = performance.now();
        const responseTime = Math.round(endTime - startTime);
        
        return {
            ...result,
            responseTime,
        };
    } catch (error) {
        console.error('Search error:', error);
        throw error;
    }
}

export async function filterSearch(filter = {}, skip = 0, limit = 100) {
    return searchBooks({
        filter,
        skip,
        limit,
    });
}

export async function semanticSearch(query, filter = null, skip = 0, limit = 100) {
    const params = {
        query,
        skip,
        limit,
    };
    
    if (filter && Object.keys(filter).length > 0) {
        params.filter = filter;
    }
    
    return searchBooks(params);
}

export async function lexicalSearch(keywords, filter = null, skip = 0, limit = 100) {
    const params = {
        keywords,
        skip,
        limit,
    };
    
    if (filter && Object.keys(filter).length > 0) {
        params.filter = filter;
    }
    
    return searchBooks(params);
}

export async function hybridSearch(query, keywords, filter = null, skip = 0, limit = 100) {
    const params = {
        query,
        keywords,
        skip,
        limit,
    };
    
    if (filter && Object.keys(filter).length > 0) {
        params.filter = filter;
    }
    
    return searchBooks(params);
}

export async function createBook(bookData) {
    return apiRequest('', {
        method: 'POST',
        body: JSON.stringify(bookData),
    });
}

export async function comparisonSearch(query, filter = null, limit = 20) {
    const hasQuery = query && query.trim();
    const searches = [];
    
    if (hasQuery) {
        searches.push(
            semanticSearch(query, filter, 0, limit)
                .then(result => ({ mode: 'semantic', ...result }))
                .catch(error => ({ mode: 'semantic', error: error.message, library_books: [], total: 0 }))
        );
        searches.push(
            lexicalSearch(query, filter, 0, limit)
                .then(result => ({ mode: 'lexical', ...result }))
                .catch(error => ({ mode: 'lexical', error: error.message, library_books: [], total: 0 }))
        );
        searches.push(
            hybridSearch(query, query, filter, 0, limit)
                .then(result => ({ mode: 'hybrid', ...result }))
                .catch(error => ({ mode: 'hybrid', error: error.message, library_books: [], total: 0 }))
        );
    } else {
        searches.push(
            Promise.resolve({
                mode: 'semantic',
                library_books: [],
                total: 0,
                responseTime: 0,
                message: 'No query provided'
            })
        );
        searches.push(
            Promise.resolve({
                mode: 'lexical',
                library_books: [],
                total: 0,
                responseTime: 0,
                message: 'No query provided'
            })
        );
        searches.push(
            Promise.resolve({
                mode: 'hybrid',
                library_books: [],
                total: 0,
                responseTime: 0,
                message: 'No query provided'
            })
        );
    }
    
    const results = await Promise.all(searches);
    
    return results.reduce((acc, result) => {
        const mode = result.mode;
        delete result.mode;
        acc[mode] = result;
        return acc;
    }, {});
}

export async function healthCheck() {
    const response = await fetch('/health');
    return response.json();
}

export { APIError };
