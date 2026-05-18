const FIELD_DEFINITIONS = {
    author: {
        label: 'Author',
        type: 'string',
        operators: ['$eq', '$ne'],
        inputType: 'text',
        placeholder: 'e.g., John Anthony'
    },
    title: {
        label: 'Title',
        type: 'string',
        operators: ['$eq', '$ne'],
        inputType: 'text',
        placeholder: 'e.g., The Great Gatsby'
    },
    genres: {
        label: 'Genres',
        type: 'array',
        operators: ['$in', '$nin'],
        inputType: 'multiselect',
        options: [
            'Science Fiction',
            'Fantasy',
            'Mystery',
            'Thriller',
            'Romance',
            'Historical Fiction',
            'Literary Fiction',
            'Horror',
            'Adventure',
            'Dystopian',
            'Young Adult',
            'Contemporary',
            'Classics'
        ]
    },
    rating: {
        label: 'Rating',
        type: 'number',
        operators: ['$eq', '$ne', '$gt', '$gte', '$lt', '$lte'],
        inputType: 'number',
        placeholder: 'e.g., 4.0',
        min: 0,
        max: 5,
        step: 0.1
    },
    publication_year: {
        label: 'Publication Year',
        type: 'number',
        operators: ['$eq', '$ne', '$gt', '$gte', '$lt', '$lte'],
        inputType: 'number',
        placeholder: 'e.g., 2020',
        min: 1800,
        max: new Date().getFullYear()
    },
    number_of_pages: {
        label: 'Number of Pages',
        type: 'number',
        operators: ['$eq', '$ne', '$gt', '$gte', '$lt', '$lte'],
        inputType: 'number',
        placeholder: 'e.g., 300',
        min: 1
    },
    is_checked_out: {
        label: 'Checked Out',
        type: 'boolean',
        operators: ['$eq', '$ne'],
        inputType: 'select',
        options: [
            { value: 'true', label: 'Yes' },
            { value: 'false', label: 'No' }
        ]
    }
};

const OPERATOR_LABELS = {
    '$eq': 'equals',
    '$ne': 'not equals',
    '$gt': 'greater than',
    '$gte': 'greater than or equal',
    '$lt': 'less than',
    '$lte': 'less than or equal',
    '$in': 'in',
    '$nin': 'not in'
};

export class FilterBuilder {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.filters = [];
        this.filterId = 0;
        
        if (!this.container) {
            console.error(`Container with id "${containerId}" not found`);
            return;
        }
        
        this.render();
    }
    
    render() {
        this.container.innerHTML = '';
        
        // Render existing filters
        this.filters.forEach(filter => {
            this.container.appendChild(this.createFilterRow(filter));
        });
        
        const addButton = document.createElement('button');
        addButton.type = 'button';
        addButton.className = 'filter-add-btn';
        addButton.innerHTML = '<span>➕</span> Add Filter';
        addButton.addEventListener('click', () => this.addFilter());
        
        this.container.appendChild(addButton);
    }
    
    createFilterRow(filter) {
        const row = document.createElement('div');
        row.className = 'filter-row';
        row.dataset.filterId = filter.id;
        
        const fieldGroup = this.createFieldGroup(filter);
        row.appendChild(fieldGroup);
        
        const operatorGroup = this.createOperatorGroup(filter);
        row.appendChild(operatorGroup);
        
        const valueGroup = this.createValueGroup(filter);
        row.appendChild(valueGroup);
        
        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.className = 'filter-remove-btn';
        removeBtn.textContent = '✕';
        removeBtn.setAttribute('aria-label', 'Remove filter');
        removeBtn.addEventListener('click', () => this.removeFilter(filter.id));
        row.appendChild(removeBtn);
        
        return row;
    }
    
    createFieldGroup(filter) {
        const group = document.createElement('div');
        group.className = 'filter-field';
        
        const label = document.createElement('label');
        label.textContent = 'Field';
        label.htmlFor = `field-${filter.id}`;
        
        const select = document.createElement('select');
        select.id = `field-${filter.id}`;
        select.value = filter.field || '';
        
        const emptyOption = document.createElement('option');
        emptyOption.value = '';
        emptyOption.textContent = 'Select field...';
        select.appendChild(emptyOption);
        
        Object.entries(FIELD_DEFINITIONS).forEach(([key, def]) => {
            const option = document.createElement('option');
            option.value = key;
            option.textContent = def.label;
            if (key === filter.field) {
                option.selected = true;
            }
            select.appendChild(option);
        });
        
        select.addEventListener('change', (e) => {
            filter.field = e.target.value;
            filter.operator = '';
            filter.value = '';
            this.render();
        });
        
        group.appendChild(label);
        group.appendChild(select);
        return group;
    }
    
    createOperatorGroup(filter) {
        const group = document.createElement('div');
        group.className = 'filter-field';
        
        const label = document.createElement('label');
        label.textContent = 'Operator';
        label.htmlFor = `operator-${filter.id}`;
        
        const select = document.createElement('select');
        select.id = `operator-${filter.id}`;
        select.disabled = !filter.field;
        
        if (filter.field) {
            const fieldDef = FIELD_DEFINITIONS[filter.field];
            
            const emptyOption = document.createElement('option');
            emptyOption.value = '';
            emptyOption.textContent = 'Select operator...';
            select.appendChild(emptyOption);
            
            fieldDef.operators.forEach(op => {
                const option = document.createElement('option');
                option.value = op;
                option.textContent = OPERATOR_LABELS[op];
                if (op === filter.operator) {
                    option.selected = true;
                }
                select.appendChild(option);
            });
        }
        
        select.addEventListener('change', (e) => {
            filter.operator = e.target.value;
            
            if (filter.operator && filter.field) {
                const fieldDef = FIELD_DEFINITIONS[filter.field];
                if (fieldDef.type === 'boolean' && filter.value === '' && fieldDef.options.length > 0) {
                    filter.value = fieldDef.options[0].value === 'true';
                }
            }
            
            this.render();
        });
        
        group.appendChild(label);
        group.appendChild(select);
        return group;
    }
    
    createValueGroup(filter) {
        const group = document.createElement('div');
        group.className = 'filter-field';
        
        const label = document.createElement('label');
        label.textContent = 'Value';
        label.htmlFor = `value-${filter.id}`;
        
        let input;
        
        if (!filter.field) {
            input = document.createElement('input');
            input.type = 'text';
            input.disabled = true;
            input.placeholder = 'Select field first';
        } else {
            const fieldDef = FIELD_DEFINITIONS[filter.field];
            
            if (fieldDef.inputType === 'multiselect') {
                input = this.createMultiSelect(filter, fieldDef);
            } else if (fieldDef.inputType === 'select') {
                input = this.createSelect(filter, fieldDef);
            } else {
                input = this.createInput(filter, fieldDef);
            }
        }
        
        input.id = `value-${filter.id}`;
        
        group.appendChild(label);
        group.appendChild(input);
        return group;
    }
    
    createInput(filter, fieldDef) {
        const input = document.createElement('input');
        input.type = fieldDef.inputType;
        input.value = filter.value || '';
        input.placeholder = fieldDef.placeholder || '';
        
        if (fieldDef.min !== undefined) input.min = fieldDef.min;
        if (fieldDef.max !== undefined) input.max = fieldDef.max;
        if (fieldDef.step !== undefined) input.step = fieldDef.step;
        
        input.addEventListener('change', (e) => {
            filter.value = fieldDef.type === 'number' ? parseFloat(e.target.value) : e.target.value;
        });
        
        return input;
    }
    
    createSelect(filter, fieldDef) {
        const select = document.createElement('select');
        const hasExplicitValue = filter.value !== '';
        
        fieldDef.options.forEach((opt, index) => {
            const option = document.createElement('option');
            option.value = opt.value;
            option.textContent = opt.label;
            if (opt.value === filter.value || (!hasExplicitValue && index === 0)) {
                option.selected = true;
            }
            select.appendChild(option);
        });
        
        if (!hasExplicitValue && fieldDef.type === 'boolean' && fieldDef.options.length > 0) {
            filter.value = fieldDef.options[0].value === 'true';
        }
        
        select.addEventListener('change', (e) => {
            filter.value = e.target.value === 'true';
        });
        
        return select;
    }
    
    createMultiSelect(filter, fieldDef) {
        const input = document.createElement('input');
        input.type = 'text';
        input.value = Array.isArray(filter.value) ? filter.value.join(', ') : '';
        input.placeholder = 'Enter values separated by commas';
        input.setAttribute('list', `datalist-${filter.id}`);
        
        const datalist = document.createElement('datalist');
        datalist.id = `datalist-${filter.id}`;
        fieldDef.options.forEach(opt => {
            const option = document.createElement('option');
            option.value = opt;
            datalist.appendChild(option);
        });
        
        input.addEventListener('change', (e) => {
            filter.value = e.target.value
                .split(',')
                .map(v => v.trim())
                .filter(v => v.length > 0);
        });
        
        const container = document.createElement('div');
        container.appendChild(input);
        container.appendChild(datalist);
        
        return container;
    }
    
    addFilter() {
        const filter = {
            id: this.filterId++,
            field: '',
            operator: '',
            value: ''
        };
        this.filters.push(filter);
        this.render();
    }
    
    removeFilter(filterId) {
        this.filters = this.filters.filter(f => f.id !== filterId);
        this.render();
    }
    
    clearFilters() {
        this.filters = [];
        this.render();
    }
    
    getFilterPredicates() {
        const predicates = {};
        
        this.filters.forEach(filter => {
            if (!filter.field || !filter.operator || filter.value === '') {
                return;
            }
            
            const fieldDef = FIELD_DEFINITIONS[filter.field];
            let value = filter.value;
            
            if (fieldDef.type === 'number' && typeof value === 'string') {
                value = parseFloat(value);
            } else if (fieldDef.type === 'boolean' && typeof value === 'string') {
                value = value === 'true';
            }
            
            if (filter.operator === '$eq') {
                predicates[filter.field] = value;
            } else {
                if (!predicates[filter.field]) {
                    predicates[filter.field] = {};
                }
                predicates[filter.field][filter.operator] = value;
            }
        });
        
        return predicates;
    }
    
    hasFilters() {
        return this.filters.some(f => f.field && f.operator && f.value !== '');
    }
    
    getFilterCount() {
        return this.filters.filter(f => f.field && f.operator && f.value !== '').length;
    }
}
