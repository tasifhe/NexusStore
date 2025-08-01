// Enhanced Recent Assets Features
class RecentAssetsManager {
    constructor() {
        this.currentView = 'grid';
        this.currentFilters = {
            sort: 'newest',
            category: '',
            free: false,
            new: false
        };
        this.isLoading = false;
        this.assets = [];
        
        this.init();
    }

    init() {
        this.cacheAssets();
        this.setupEventListeners();
        this.setupKeyboardNavigation();
        this.setupIntersectionObserver();
        this.animateAssetsOnLoad();
    }

    cacheAssets() {
        const assetCards = document.querySelectorAll('.asset-card.enhanced');
        this.assets = Array.from(assetCards).map(card => ({
            element: card,
            data: {
                id: card.getAttribute('data-id'),
                category: card.getAttribute('data-category'),
                free: card.getAttribute('data-free') === 'true',
                new: card.getAttribute('data-new') === 'true',
                rating: parseFloat(card.getAttribute('data-rating')) || 0,
                date: new Date(card.getAttribute('data-date')),
                title: card.getAttribute('data-title')
            }
        }));
    }

    setupEventListeners() {
        // View toggle enhanced
        const viewButtons = document.querySelectorAll('.view-btn');
        viewButtons.forEach(btn => {
            btn.addEventListener('click', (e) => this.handleViewChange(e));
        });

        // Enhanced filter handling
        const sortSelect = document.querySelector('[data-filter="sort"]');
        if (sortSelect) {
            sortSelect.addEventListener('change', (e) => this.handleFilterChange(e));
        }

        const categorySelect = document.querySelector('[data-filter="category"]');
        if (categorySelect) {
            categorySelect.addEventListener('change', (e) => this.handleFilterChange(e));
        }

        const checkboxes = document.querySelectorAll('.filter-checkboxes input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', (e) => this.handleFilterChange(e));
        });

        // Asset card interactions
        this.setupAssetCardListeners();

        // Search functionality
        this.setupSearch();
    }

    setupAssetCardListeners() {
        this.assets.forEach(asset => {
            const element = asset.element;
            
            // Enhanced hover effects
            element.addEventListener('mouseenter', () => this.onAssetHover(element));
            element.addEventListener('mouseleave', () => this.onAssetLeave(element));
            
            // Keyboard navigation support
            element.setAttribute('tabindex', '0');
            element.addEventListener('keydown', (e) => this.onAssetKeydown(e, asset));
            
            // Click analytics
            element.addEventListener('click', () => this.trackAssetClick(asset.data.id));
        });
    }

    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeQuickView();
                this.closeFilterDropdown();
            }
            
            if (e.ctrlKey && e.key === 'f') {
                e.preventDefault();
                this.focusSearch();
            }
        });
    }

    setupIntersectionObserver() {
        const options = {
            threshold: 0.1,
            rootMargin: '50px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    this.lazyLoadImage(entry.target);
                }
            });
        }, options);

        this.assets.forEach(asset => {
            observer.observe(asset.element);
        });
    }

    setupSearch() {
        // Create search input if it doesn't exist
        const searchContainer = document.querySelector('.section-controls');
        if (searchContainer && !document.querySelector('.asset-search')) {
            const searchDiv = document.createElement('div');
            searchDiv.className = 'asset-search';
            searchDiv.innerHTML = `
                <input type="text" 
                       class="search-input" 
                       placeholder="Search assets..." 
                       aria-label="Search assets">
                <i class="fas fa-search search-icon"></i>
            `;
            searchContainer.insertBefore(searchDiv, searchContainer.firstChild);

            const searchInput = searchDiv.querySelector('.search-input');
            let searchTimeout;
            
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    this.performSearch(e.target.value);
                }, 300);
            });
        }
    }

    performSearch(query) {
        const normalizedQuery = query.toLowerCase().trim();
        
        this.assets.forEach(asset => {
            const title = asset.data.title.toLowerCase();
            const matches = title.includes(normalizedQuery) || normalizedQuery === '';
            
            asset.element.style.display = matches ? 'block' : 'none';
            
            if (matches && normalizedQuery) {
                this.highlightSearchTerm(asset.element, normalizedQuery);
            } else {
                this.removeHighlight(asset.element);
            }
        });

        this.updateEmptyState();
    }

    highlightSearchTerm(element, term) {
        const titleElement = element.querySelector('.asset-card-title');
        if (titleElement) {
            const text = titleElement.textContent;
            const regex = new RegExp(`(${term})`, 'gi');
            titleElement.innerHTML = text.replace(regex, '<mark>$1</mark>');
        }
    }

    removeHighlight(element) {
        const titleElement = element.querySelector('.asset-card-title');
        if (titleElement) {
            titleElement.innerHTML = titleElement.textContent;
        }
    }

    handleViewChange(e) {
        const viewType = e.target.getAttribute('data-view');
        this.currentView = viewType;
        
        // Update UI
        document.querySelectorAll('.view-btn').forEach(btn => btn.classList.remove('active'));
        e.target.classList.add('active');
        
        const assetGrid = document.getElementById('recentAssetsGrid');
        assetGrid.className = viewType === 'list' ? 'asset-grid list-view' : 'asset-grid';
        
        // Animate transition
        this.animateViewTransition();
        
        // Store preference
        localStorage.setItem('assetView', viewType);
    }

    handleFilterChange(e) {
        const filterType = e.target.getAttribute('data-filter');
        
        if (filterType === 'sort' || filterType === 'category') {
            this.currentFilters[filterType] = e.target.value;
        } else if (e.target.type === 'checkbox') {
            this.currentFilters[filterType] = e.target.checked;
        }
        
        this.applyFilters();
        this.updateFilterIndicator();
    }

    applyFilters() {
        this.showLoadingState();
        
        setTimeout(() => {
            let visibleAssets = this.assets.filter(asset => {
                return this.passesFilters(asset.data);
            });

            // Sort assets
            visibleAssets = this.sortAssets(visibleAssets);

            // Update visibility
            this.assets.forEach(asset => {
                const isVisible = visibleAssets.includes(asset);
                asset.element.style.display = isVisible ? 'block' : 'none';
                asset.element.style.order = isVisible ? visibleAssets.indexOf(asset) : 999;
            });

            this.updateEmptyState();
            this.hideLoadingState();
            this.animateFilteredAssets();
            
        }, 200); // Small delay for better UX
    }

    passesFilters(data) {
        // Category filter
        if (this.currentFilters.category && data.category !== this.currentFilters.category) {
            return false;
        }
        
        // Free filter
        if (this.currentFilters.free && !data.free) {
            return false;
        }
        
        // New filter
        if (this.currentFilters.new && !data.new) {
            return false;
        }
        
        return true;
    }

    sortAssets(assets) {
        return assets.sort((a, b) => {
            switch (this.currentFilters.sort) {
                case 'newest':
                    return b.data.date - a.data.date;
                case 'oldest':
                    return a.data.date - b.data.date;
                case 'rating':
                    return b.data.rating - a.data.rating;
                case 'title':
                    return a.data.title.localeCompare(b.data.title);
                default:
                    return 0;
            }
        });
    }

    updateFilterIndicator() {
        const filterBtn = document.getElementById('assetFilter');
        const hasActiveFilters = this.currentFilters.category || 
                                this.currentFilters.free || 
                                this.currentFilters.new ||
                                this.currentFilters.sort !== 'newest';
        
        if (hasActiveFilters) {
            filterBtn.classList.add('active');
        } else {
            filterBtn.classList.remove('active');
        }
    }

    updateEmptyState() {
        const visibleAssets = this.assets.filter(asset => 
            asset.element.style.display !== 'none'
        );
        
        const assetGrid = document.getElementById('recentAssetsGrid');
        const emptyState = document.getElementById('emptyState');
        
        if (visibleAssets.length === 0) {
            assetGrid.style.display = 'none';
            emptyState.style.display = 'block';
        } else {
            assetGrid.style.display = 'grid';
            emptyState.style.display = 'none';
        }
    }

    onAssetHover(element) {
        // Add subtle animation
        element.style.transform = 'translateY(-8px) scale(1.02)';
        
        // Preload related assets (simulate)
        const category = element.getAttribute('data-category');
        this.preloadRelatedAssets(category);
    }

    onAssetLeave(element) {
        element.style.transform = '';
    }

    onAssetKeydown(e, asset) {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            asset.element.click();
        }
        
        if (e.key === 'q') {
            e.preventDefault();
            openQuickView(asset.data.id);
        }
        
        if (e.key === 'w') {
            e.preventDefault();
            toggleWishlist(asset.data.id);
        }
    }

    lazyLoadImage(element) {
        const img = element.querySelector('img[data-src]');
        if (img) {
            img.src = img.getAttribute('data-src');
            img.removeAttribute('data-src');
            img.classList.add('loaded');
        }
    }

    preloadRelatedAssets(category) {
        // Simulate preloading related assets
        console.log(`Preloading assets from category: ${category}`);
    }

    trackAssetClick(assetId) {
        // Analytics tracking
        console.log(`Asset clicked: ${assetId}`);
        
        // You could send this to your analytics service
        // analytics.track('asset_clicked', { asset_id: assetId });
    }

    animateAssetsOnLoad() {
        this.assets.forEach((asset, index) => {
            asset.element.style.animationDelay = `${index * 0.1}s`;
            asset.element.classList.add('fade-in');
        });
    }

    animateViewTransition() {
        const assetGrid = document.getElementById('recentAssetsGrid');
        assetGrid.style.opacity = '0.5';
        assetGrid.style.transform = 'scale(0.98)';
        
        setTimeout(() => {
            assetGrid.style.opacity = '1';
            assetGrid.style.transform = 'scale(1)';
        }, 150);
    }

    animateFilteredAssets() {
        const visibleAssets = this.assets.filter(asset => 
            asset.element.style.display !== 'none'
        );
        
        visibleAssets.forEach((asset, index) => {
            asset.element.style.animationDelay = `${index * 0.05}s`;
            asset.element.classList.add('filter-animation');
            
            setTimeout(() => {
                asset.element.classList.remove('filter-animation');
            }, 600);
        });
    }

    showLoadingState() {
        this.isLoading = true;
        const assetGrid = document.getElementById('recentAssetsGrid');
        assetGrid.classList.add('loading');
    }

    hideLoadingState() {
        this.isLoading = false;
        const assetGrid = document.getElementById('recentAssetsGrid');
        assetGrid.classList.remove('loading');
    }

    closeQuickView() {
        const modal = document.getElementById('quickViewModal');
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
    }

    closeFilterDropdown() {
        const dropdown = document.querySelector('.filter-dropdown');
        if (dropdown) {
            dropdown.classList.remove('active');
        }
    }

    focusSearch() {
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.focus();
        }
    }

    // Public API
    refresh() {
        this.cacheAssets();
        this.applyFilters();
    }

    getActiveFilters() {
        return { ...this.currentFilters };
    }

    resetFilters() {
        this.currentFilters = {
            sort: 'newest',
            category: '',
            free: false,
            new: false
        };
        
        // Reset UI
        document.querySelector('[data-filter="sort"]').value = 'newest';
        document.querySelector('[data-filter="category"]').value = '';
        document.querySelectorAll('.filter-checkboxes input[type="checkbox"]').forEach(cb => {
            cb.checked = false;
        });
        
        this.applyFilters();
        this.updateFilterIndicator();
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('recentAssetsGrid')) {
        window.recentAssetsManager = new RecentAssetsManager();
    }
});

// Export for external use
window.RecentAssetsManager = RecentAssetsManager;
