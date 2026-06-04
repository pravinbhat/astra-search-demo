/**
 * HTML Partial Loader
 * Dynamically loads HTML partials into the page
 */

class PartialLoader {
    constructor() {
        this.cache = new Map();
    }

    /**
     * Load a single partial and insert it into a target element
     * @param {string} partialPath - Path to the partial HTML file
     * @param {string} targetSelector - CSS selector for the target element
     * @param {string} insertMode - 'replace' (default) or 'append'
     * @returns {Promise<void>}
     */
    async loadPartial(partialPath, targetSelector, insertMode = 'replace') {
        try {
            // Check cache first
            let html;
            if (this.cache.has(partialPath)) {
                html = this.cache.get(partialPath);
            } else {
                const response = await fetch(partialPath);
                if (!response.ok) {
                    throw new Error(`Failed to load partial: ${partialPath} (${response.status})`);
                }
                html = await response.text();
                this.cache.set(partialPath, html);
            }

            // Insert into target
            const target = document.querySelector(targetSelector);
            if (!target) {
                throw new Error(`Target element not found: ${targetSelector}`);
            }

            if (insertMode === 'append') {
                target.insertAdjacentHTML('beforeend', html);
            } else {
                target.innerHTML = html;
            }
        } catch (error) {
            console.error(`Error loading partial ${partialPath}:`, error);
            throw error;
        }
    }

    /**
     * Load multiple partials in parallel
     * @param {Array<{path: string, target: string, mode?: string}>} partials
     * @returns {Promise<void>}
     */
    async loadPartials(partials) {
        const promises = partials.map(({ path, target, mode }) =>
            this.loadPartial(path, target, mode)
        );
        await Promise.all(promises);
    }

    /**
     * Clear the cache
     */
    clearCache() {
        this.cache.clear();
    }
}

// Create and export a singleton instance
const partialLoader = new PartialLoader();

export default partialLoader;

// Made with Bob
