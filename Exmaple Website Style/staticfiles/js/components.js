// Component functionality for GameAssetHub

// Modal Component
class Modal {
    constructor(modalId) {
        this.modal = document.getElementById(modalId);
        this.closeBtn = this.modal?.querySelector('.modal-close');
        this.init();
    }

    init() {
        if (!this.modal) return;

        // Close button event
        this.closeBtn?.addEventListener('click', () => this.close());

        // Click outside to close
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.close();
            }
        });

        // Escape key to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal.classList.contains('active')) {
                this.close();
            }
        });
    }

    open() {
        this.modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    close() {
        this.modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// Dropdown Component
class Dropdown {
    constructor(element) {
        this.dropdown = element;
        this.trigger = element.querySelector('.dropdown-trigger');
        this.menu = element.querySelector('.dropdown-menu');
        this.init();
    }

    init() {
        if (!this.trigger || !this.menu) return;

        this.trigger.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggle();
        });

        // Close when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.dropdown.contains(e.target)) {
                this.close();
            }
        });

        // Close on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.close();
            }
        });
    }

    toggle() {
        this.menu.classList.toggle('active');
    }

    close() {
        this.menu.classList.remove('active');
    }
}

// Filter Component
class Filter {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.filters = {};
        this.init();
    }

    init() {
        if (!this.container) return;

        // Initialize filter controls
        const filterControls = this.container.querySelectorAll('.filter-control');
        filterControls.forEach(control => {
            control.addEventListener('change', (e) => {
                this.handleFilterChange(e.target.name, e.target.value, e.target.checked);
            });
        });

        // Clear filters button
        const clearBtn = this.container.querySelector('.clear-filters');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearFilters());
        }
    }

    handleFilterChange(filterName, value, checked) {
        if (!this.filters[filterName]) {
            this.filters[filterName] = [];
        }

        if (checked) {
            if (!this.filters[filterName].includes(value)) {
                this.filters[filterName].push(value);
            }
        } else {
            this.filters[filterName] = this.filters[filterName].filter(v => v !== value);
        }

        this.applyFilters();
    }

    applyFilters() {
        // Emit custom event for filter application
        const event = new CustomEvent('filtersChanged', {
            detail: this.filters
        });
        document.dispatchEvent(event);
    }

    clearFilters() {
        this.filters = {};
        
        // Reset all filter controls
        const filterControls = this.container.querySelectorAll('.filter-control');
        filterControls.forEach(control => {
            control.checked = false;
            control.value = '';
        });

        this.applyFilters();
    }
}

// Carousel Component
class Carousel {
    constructor(element) {
        this.carousel = element;
        this.track = element.querySelector('.carousel-track');
        this.slides = Array.from(element.querySelectorAll('.carousel-slide'));
        this.prevBtn = element.querySelector('.carousel-prev');
        this.nextBtn = element.querySelector('.carousel-next');
        this.indicators = Array.from(element.querySelectorAll('.carousel-indicator'));
        
        this.currentSlide = 0;
        this.slideWidth = 0;
        this.init();
    }

    init() {
        if (!this.track || this.slides.length === 0) return;

        this.updateSlideWidth();
        this.updateCarousel();

        // Navigation buttons
        this.prevBtn?.addEventListener('click', () => this.prevSlide());
        this.nextBtn?.addEventListener('click', () => this.nextSlide());

        // Indicators
        this.indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', () => this.goToSlide(index));
        });

        // Touch/swipe support
        this.addTouchSupport();

        // Auto-play (if enabled)
        if (this.carousel.dataset.autoplay === 'true') {
            this.startAutoplay();
        }

        // Resize handler
        window.addEventListener('resize', () => this.updateSlideWidth());
    }

    updateSlideWidth() {
        this.slideWidth = this.slides[0]?.offsetWidth || 0;
    }

    updateCarousel() {
        const translateX = -this.currentSlide * this.slideWidth;
        this.track.style.transform = `translateX(${translateX}px)`;

        // Update indicators
        this.indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === this.currentSlide);
        });

        // Update navigation buttons
        this.prevBtn?.classList.toggle('disabled', this.currentSlide === 0);
        this.nextBtn?.classList.toggle('disabled', this.currentSlide === this.slides.length - 1);
    }

    prevSlide() {
        if (this.currentSlide > 0) {
            this.currentSlide--;
            this.updateCarousel();
        }
    }

    nextSlide() {
        if (this.currentSlide < this.slides.length - 1) {
            this.currentSlide++;
            this.updateCarousel();
        }
    }

    goToSlide(index) {
        if (index >= 0 && index < this.slides.length) {
            this.currentSlide = index;
            this.updateCarousel();
        }
    }

    addTouchSupport() {
        let startX = 0;
        let currentX = 0;
        let isDragging = false;

        this.track.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            isDragging = true;
        });

        this.track.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            currentX = e.touches[0].clientX;
        });

        this.track.addEventListener('touchend', () => {
            if (!isDragging) return;
            isDragging = false;

            const diff = startX - currentX;
            const threshold = 50;

            if (Math.abs(diff) > threshold) {
                if (diff > 0) {
                    this.nextSlide();
                } else {
                    this.prevSlide();
                }
            }
        });
    }

    startAutoplay() {
        this.autoplayInterval = setInterval(() => {
            if (this.currentSlide < this.slides.length - 1) {
                this.nextSlide();
            } else {
                this.currentSlide = 0;
                this.updateCarousel();
            }
        }, 5000);
    }

    stopAutoplay() {
        if (this.autoplayInterval) {
            clearInterval(this.autoplayInterval);
        }
    }
}

// Tabs Component
class Tabs {
    constructor(element) {
        this.tabsContainer = element;
        this.tabButtons = Array.from(element.querySelectorAll('.tab-button'));
        this.tabPanels = Array.from(element.querySelectorAll('.tab-panel'));
        this.activeTab = 0;
        this.init();
    }

    init() {
        if (this.tabButtons.length === 0 || this.tabPanels.length === 0) return;

        this.tabButtons.forEach((button, index) => {
            button.addEventListener('click', () => this.switchTab(index));
        });

        // Keyboard navigation
        this.tabButtons.forEach((button, index) => {
            button.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowRight') {
                    const nextIndex = (index + 1) % this.tabButtons.length;
                    this.switchTab(nextIndex);
                    this.tabButtons[nextIndex].focus();
                } else if (e.key === 'ArrowLeft') {
                    const prevIndex = (index - 1 + this.tabButtons.length) % this.tabButtons.length;
                    this.switchTab(prevIndex);
                    this.tabButtons[prevIndex].focus();
                }
            });
        });

        this.switchTab(this.activeTab);
    }

    switchTab(index) {
        if (index < 0 || index >= this.tabButtons.length) return;

        // Update buttons
        this.tabButtons.forEach((button, i) => {
            button.classList.toggle('active', i === index);
            button.setAttribute('aria-selected', i === index);
        });

        // Update panels
        this.tabPanels.forEach((panel, i) => {
            panel.classList.toggle('active', i === index);
            panel.setAttribute('aria-hidden', i !== index);
        });

        this.activeTab = index;

        // Emit custom event
        const event = new CustomEvent('tabChanged', {
            detail: { index, tabId: this.tabButtons[index].dataset.tab }
        });
        this.tabsContainer.dispatchEvent(event);
    }
}

// Lazy Loading Component
class LazyLoader {
    constructor(options = {}) {
        this.options = {
            threshold: 0.1,
            rootMargin: '50px',
            ...options
        };
        this.observer = null;
        this.init();
    }

    init() {
        if ('IntersectionObserver' in window) {
            this.observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.loadElement(entry.target);
                    }
                });
            }, this.options);

            this.observe();
        } else {
            // Fallback for older browsers
            this.loadAllElements();
        }
    }

    observe() {
        const lazyElements = document.querySelectorAll('[data-lazy]');
        lazyElements.forEach(element => {
            this.observer.observe(element);
        });
    }

    loadElement(element) {
        const src = element.dataset.lazy;
        
        if (element.tagName === 'IMG') {
            element.src = src;
        } else {
            element.style.backgroundImage = `url(${src})`;
        }

        element.classList.add('loaded');
        element.removeAttribute('data-lazy');
        
        if (this.observer) {
            this.observer.unobserve(element);
        }
    }

    loadAllElements() {
        const lazyElements = document.querySelectorAll('[data-lazy]');
        lazyElements.forEach(element => this.loadElement(element));
    }
}

// Initialize components when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Initialize modals
    document.querySelectorAll('.modal').forEach(modal => {
        new Modal(modal.id);
    });

    // Initialize dropdowns
    document.querySelectorAll('.dropdown').forEach(dropdown => {
        new Dropdown(dropdown);
    });

    // Initialize carousels
    document.querySelectorAll('.carousel').forEach(carousel => {
        new Carousel(carousel);
    });

    // Initialize tabs
    document.querySelectorAll('.tabs').forEach(tabs => {
        new Tabs(tabs);
    });

    // Initialize lazy loading
    new LazyLoader();

    // Initialize filters
    const filterContainer = document.querySelector('.filter-container');
    if (filterContainer) {
        new Filter(filterContainer.id);
    }
});

// Export components for external use
window.Components = {
    Modal,
    Dropdown,
    Filter,
    Carousel,
    Tabs,
    LazyLoader
};