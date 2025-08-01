// Hero Slideshow Variables
let currentSlideIndex = 0;
let slideInterval;
const slideAutoAdvanceDelay = 5000; // 5 seconds for testing
const slideTransitionDuration = 800; // 0.8 seconds

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing SIMPLE slideshow...');
    let slideIndex = 0;
    const slides = document.querySelectorAll('.hero-slide');
    const indicators = document.querySelectorAll('.indicator');
    const progressBar = document.querySelector('.progress-bar');
    let progressTimer;

    function startProgressBar() {
        if (progressBar) {
            progressBar.classList.remove('animate');
            // Force reflow to restart animation
            void progressBar.offsetWidth;
            progressBar.classList.add('animate');
        }
        if (progressTimer) clearTimeout(progressTimer);
        progressTimer = setTimeout(() => {
            if (progressBar) progressBar.classList.remove('animate');
        }, slideAutoAdvanceDelay);
    }

    function showSlide(n) {
        console.log('Showing slide:', n);
        slides.forEach(slide => {
            slide.style.opacity = '0';
            slide.style.transform = 'translateX(100%)';
            slide.classList.remove('active');
        });
        if (slides[n]) {
            slides[n].style.opacity = '1';
            slides[n].style.transform = 'translateX(0)';
            slides[n].classList.add('active');
        }
        indicators.forEach((indicator, i) => {
            indicator.classList.toggle('active', i === n);
        });
        startProgressBar();
    }

    function nextSlide() {
        slideIndex = (slideIndex + 1) % slides.length;
        showSlide(slideIndex);
    }

    showSlide(0);
    setInterval(nextSlide, slideAutoAdvanceDelay);
    startProgressBar();
    console.log('Simple slideshow started!');
});

function initializeHeroSlideshow() {
    const slides = document.querySelectorAll('.hero-slide');
    const indicators = document.querySelectorAll('.indicator');
    console.log('Found slides:', slides.length);
    console.log('Found indicators:', indicators.length);
    if (slides.length === 0) {
        console.error('No slides found!');
        return;
    }
    updateSlideVisibility();
    startSlideshow();
    setupSlideNavigation();
    const heroSection = document.querySelector('.hero');
    if (heroSection) {
        heroSection.addEventListener('mouseenter', function() {
            console.log('Pausing slideshow');
            pauseSlideshow();
        });
        heroSection.addEventListener('mouseleave', function() {
            console.log('Resuming slideshow');
            startSlideshow();
        });
    }
}

function updateSlideVisibility() {
    const slides = document.querySelectorAll('.hero-slide');
    const indicators = document.querySelectorAll('.indicator');
    console.log('Updating slide visibility, current index:', currentSlideIndex);
    slides.forEach((slide, index) => {
        slide.classList.remove('active', 'prev');
        if (index === currentSlideIndex) {
            slide.classList.add('active');
            console.log('Setting slide', index, 'as active');
        } else if (index === currentSlideIndex - 1 || (currentSlideIndex === 0 && index === slides.length - 1)) {
            slide.classList.add('prev');
        }
    });
    indicators.forEach((indicator, index) => {
        indicator.classList.toggle('active', index === currentSlideIndex);
    });
    updateProgressBar();
}

function updateProgressBar() {
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        const progress = ((currentSlideIndex + 1) / document.querySelectorAll('.hero-slide').length) * 100;
        progressBar.style.width = progress + '%';
        console.log('Progress bar updated to:', progress + '%');
    }
}

function nextSlide() {
    const slides = document.querySelectorAll('.hero-slide');
    const oldIndex = currentSlideIndex;
    currentSlideIndex = (currentSlideIndex + 1) % slides.length;
    console.log('Next slide: from', oldIndex, 'to', currentSlideIndex);
    updateSlideVisibility();
}

function prevSlide() {
    const slides = document.querySelectorAll('.hero-slide');
    const oldIndex = currentSlideIndex;
    currentSlideIndex = (currentSlideIndex - 1 + slides.length) % slides.length;
    console.log('Previous slide: from', oldIndex, 'to', currentSlideIndex);
    updateSlideVisibility();
}

function goToSlide(index) {
    const slides = document.querySelectorAll('.hero-slide');
    if (index >= 0 && index < slides.length) {
        console.log('Going to slide:', index);
        currentSlideIndex = index;
        updateSlideVisibility();
    }
}

function startSlideshow() {
    pauseSlideshow();
    console.log('Starting slideshow with delay:', slideAutoAdvanceDelay);
    slideInterval = setInterval(function() {
        console.log('Auto-advancing slide...');
        nextSlide();
    }, slideAutoAdvanceDelay);
}

function pauseSlideshow() {
    if (slideInterval) {
        console.log('Pausing slideshow');
        clearInterval(slideInterval);
        slideInterval = null;
    }
}

function setupSlideNavigation() {
    const prevBtn = document.querySelector('.hero-nav-btn.prev');
    const nextBtn = document.querySelector('.hero-nav-btn.next');
    console.log('Setting up navigation buttons:', prevBtn, nextBtn);
    if (prevBtn) prevBtn.addEventListener('click', function() {
        console.log('Previous button clicked');
        prevSlide();
        startSlideshow();
    });
    if (nextBtn) nextBtn.addEventListener('click', function() {
        console.log('Next button clicked');
        nextSlide();
        startSlideshow();
    });
    const indicators = document.querySelectorAll('.indicator');
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', function() {
            console.log('Indicator clicked:', index);
            goToSlide(index);
            startSlideshow();
        });
    });
}

function changeSlide(direction) {
    console.log('changeSlide called with direction:', direction);
    if (direction === 1) {
        nextSlide();
    } else {
        prevSlide();
    }
    startSlideshow();
}

function currentSlide(index) {
    console.log('currentSlide called with index:', index);
    goToSlide(index - 1);
    startSlideshow();
}

document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            const tabType = this.getAttribute('data-tab');
            console.log('Loading content for:', tabType);
        });
    });
    
    // Initialize Recent Assets Enhanced Features
    initializeRecentAssets();
});

// Recent Assets Enhanced Functionality
function initializeRecentAssets() {
    console.log('Initializing enhanced recent assets features...');
    
    // Initialize view toggle
    initializeViewToggle();
    
    // Initialize filter dropdown
    initializeFilterDropdown();
    
    // Initialize filters
    initializeFilters();
    
    // Initialize quick actions
    initializeQuickActions();
    
    // Initialize keyboard navigation
    initializeKeyboardNavigation();
    
    // Initialize accessibility features
    initializeAccessibility();
}

function initializeKeyboardNavigation() {
    document.addEventListener('keydown', function(e) {
        const modal = document.getElementById('quickViewModal');
        
        // Close modal with Escape key
        if (e.key === 'Escape' && modal && modal.classList.contains('active')) {
            closeQuickView();
        }
        
        // Filter shortcuts
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case 'f':
                    e.preventDefault();
                    document.getElementById('assetFilter')?.click();
                    break;
                case '1':
                    e.preventDefault();
                    document.querySelector('[data-view="grid"]')?.click();
                    break;
                case '2':
                    e.preventDefault();
                    document.querySelector('[data-view="list"]')?.click();
                    break;
            }
        }
    });
}

function initializeAccessibility() {
    // Add ARIA labels and roles
    const assetCards = document.querySelectorAll('.asset-card');
    assetCards.forEach((card, index) => {
        card.setAttribute('role', 'button');
        card.setAttribute('tabindex', '0');
        card.setAttribute('aria-label', `Asset ${index + 1}: ${card.querySelector('.asset-card-title')?.textContent || 'Unknown asset'}`);
        
        // Add keyboard support for asset cards
        card.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                card.click();
            }
        });
    });
    
    // Add ARIA labels to buttons
    const viewButtons = document.querySelectorAll('.view-btn');
    viewButtons.forEach(btn => {
        const view = btn.getAttribute('data-view');
        btn.setAttribute('aria-label', `Switch to ${view} view`);
    });
    
    // Add live region for filter results
    const assetGrid = document.getElementById('recentAssetsGrid');
    if (assetGrid) {
        assetGrid.setAttribute('aria-live', 'polite');
        assetGrid.setAttribute('aria-label', 'Asset grid');
    }
}

function initializeViewToggle() {
    const viewButtons = document.querySelectorAll('.view-btn');
    const assetGrid = document.getElementById('recentAssetsGrid');
    
    if (!assetGrid) return;
    
    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Update active button
            viewButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Update grid view
            const viewType = this.getAttribute('data-view');
            assetGrid.className = viewType === 'list' ? 'asset-grid list-view' : 'asset-grid';
            
            console.log('View changed to:', viewType);
        });
    });
}

function initializeFilterDropdown() {
    const filterBtn = document.getElementById('assetFilter');
    const filterDropdown = document.querySelector('.filter-dropdown');
    
    if (!filterBtn || !filterDropdown) return;
    
    filterBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        filterDropdown.classList.toggle('active');
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!filterDropdown.contains(e.target)) {
            filterDropdown.classList.remove('active');
        }
    });
    
    // Prevent dropdown close when clicking inside
    const filterMenu = document.querySelector('.filter-menu');
    if (filterMenu) {
        filterMenu.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
}

function initializeFilters() {
    const filterSelects = document.querySelectorAll('.filter-select');
    const filterCheckboxes = document.querySelectorAll('.filter-checkboxes input[type="checkbox"]');
    
    filterSelects.forEach(select => {
        select.addEventListener('change', applyFilters);
    });
    
    filterCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', applyFilters);
    });
}

function applyFilters() {
    const assetGrid = document.getElementById('recentAssetsGrid');
    const emptyState = document.getElementById('emptyState');
    const assetCards = assetGrid.querySelectorAll('.asset-card');
    
    // Get filter values
    const sortBy = document.querySelector('[data-filter="sort"]')?.value || 'newest';
    const categoryFilter = document.querySelector('[data-filter="category"]')?.value || '';
    const freeFilter = document.querySelector('[data-filter="free"]')?.checked || false;
    const newFilter = document.querySelector('[data-filter="new"]')?.checked || false;
    
    console.log('Applying filters:', { sortBy, categoryFilter, freeFilter, newFilter });
    
    // Filter cards
    const visibleCards = [];
    assetCards.forEach(card => {
        let visible = true;
        
        // Category filter
        if (categoryFilter && card.getAttribute('data-category') !== categoryFilter) {
            visible = false;
        }
        
        // Free filter
        if (freeFilter && card.getAttribute('data-free') !== 'true') {
            visible = false;
        }
        
        // New filter
        if (newFilter && card.getAttribute('data-new') !== 'true') {
            visible = false;
        }
        
        if (visible) {
            visibleCards.push(card);
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
    
    // Sort visible cards
    sortCards(visibleCards, sortBy);
    
    // Show/hide empty state
    if (visibleCards.length === 0) {
        assetGrid.style.display = 'none';
        emptyState.style.display = 'block';
    } else {
        assetGrid.style.display = 'grid';
        emptyState.style.display = 'none';
    }
    
    console.log(`Filtered results: ${visibleCards.length} assets visible`);
}

function sortCards(cards, sortBy) {
    const assetGrid = document.getElementById('recentAssetsGrid');
    
    cards.sort((a, b) => {
        switch (sortBy) {
            case 'newest':
                return new Date(b.getAttribute('data-date')) - new Date(a.getAttribute('data-date'));
            case 'oldest':
                return new Date(a.getAttribute('data-date')) - new Date(b.getAttribute('data-date'));
            case 'rating':
                return parseFloat(b.getAttribute('data-rating')) - parseFloat(a.getAttribute('data-rating'));
            case 'title':
                return a.getAttribute('data-title').localeCompare(b.getAttribute('data-title'));
            default:
                return 0;
        }
    });
    
    // Reorder DOM elements
    cards.forEach(card => {
        assetGrid.appendChild(card);
    });
}

function initializeQuickActions() {
    // Initialize quick view buttons
    window.openQuickView = function(assetId) {
        console.log('Opening quick view for asset:', assetId);
        
        // Create modal HTML if it doesn't exist
        let modal = document.getElementById('quickViewModal');
        if (!modal) {
            modal = createQuickViewModal();
            document.body.appendChild(modal);
        }
        
        // Load asset data (this would normally be an AJAX call)
        loadAssetQuickView(assetId, modal);
        
        // Show modal
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    };
    
    // Initialize wishlist buttons
    window.toggleWishlist = function(assetId) {
        console.log('Toggling wishlist for asset:', assetId);
        
        const wishlistBtn = event.target.closest('.wishlist-btn');
        const isAdded = wishlistBtn.classList.contains('added');
        
        if (isAdded) {
            wishlistBtn.classList.remove('added');
            showToast('Removed from wishlist', 'info');
        } else {
            wishlistBtn.classList.add('added');
            showToast('Added to wishlist', 'success');
        }
        
        // Here you would normally make an AJAX call to update the server
        // fetch(`/api/wishlist/toggle/${assetId}/`, { method: 'POST' })
    };
}

function createQuickViewModal() {
    const modal = document.createElement('div');
    modal.id = 'quickViewModal';
    modal.className = 'quick-view-modal';
    modal.innerHTML = `
        <div class="quick-view-content">
            <div class="quick-view-header">
                <h3>Asset Details</h3>
                <button class="quick-view-close" onclick="closeQuickView()">&times;</button>
            </div>
            <div class="quick-view-body" id="quickViewBody">
                <div class="loading-spinner">Loading...</div>
            </div>
        </div>
    `;
    
    // Close on background click
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeQuickView();
        }
    });
    
    return modal;
}

function loadAssetQuickView(assetId, modal) {
    const body = modal.querySelector('#quickViewBody');
    
    // Simulate loading (in real app, this would be an AJAX call)
    body.innerHTML = '<div class="loading-spinner">Loading asset details...</div>';
    
    setTimeout(() => {
        body.innerHTML = `
            <div class="asset-quick-preview">
                <div class="asset-image-large">
                    <img src="/media/thumbnails/placeholder.jpg" alt="Asset Preview" style="width: 100%; border-radius: 8px;">
                </div>
                <div class="asset-details">
                    <h4>Sample Asset Title</h4>
                    <p><strong>Creator:</strong> Sample Creator</p>
                    <p><strong>Category:</strong> 3D Models</p>
                    <p><strong>Description:</strong> This is a sample asset description that would normally be loaded from the server.</p>
                    <div class="asset-actions">
                        <button class="btn btn-primary">Download</button>
                        <button class="btn btn-secondary" onclick="toggleWishlist(${assetId})">Add to Wishlist</button>
                    </div>
                </div>
            </div>
        `;
    }, 500);
}

window.closeQuickView = function() {
    const modal = document.getElementById('quickViewModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
};

function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <span>${message}</span>
        </div>
    `;
    
    container.appendChild(toast);
    
    // Show toast
    setTimeout(() => toast.classList.add('show'), 100);
    
    // Remove toast after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 3000);
}

// Animation utilities
function showLoadingState() {
    const assetGrid = document.getElementById('recentAssetsGrid');
    const loadingGrid = document.getElementById('assetGridLoading');
    
    if (assetGrid && loadingGrid) {
        assetGrid.style.display = 'none';
        loadingGrid.style.display = 'grid';
    }
}

function hideLoadingState() {
    const assetGrid = document.getElementById('recentAssetsGrid');
    const loadingGrid = document.getElementById('assetGridLoading');
    
    if (assetGrid && loadingGrid) {
        loadingGrid.style.display = 'none';
        assetGrid.style.display = 'grid';
    }
}

// Add smooth animations when assets are loaded
function animateAssetsIn() {
    const assetCards = document.querySelectorAll('.asset-card');
    
    assetCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}
