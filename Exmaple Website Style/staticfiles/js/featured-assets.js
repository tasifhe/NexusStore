// Featured Assets Section JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeFeaturedSection();
});

function initializeFeaturedSection() {
    // Initialize tab switching
    initializeFeaturedTabs();
    
    // Initialize carousel enhancements
    initializeCarouselEnhancements();
    
    // Add hover effects
    addFeaturedCardHoverEffects();
}

// Featured tabs functionality
function initializeFeaturedTabs() {
    const tabButtons = document.querySelectorAll('.fab-featured-tabs .tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remove active class from all buttons
            tabButtons.forEach(btn => {
                btn.classList.remove('active');
                btn.setAttribute('aria-selected', 'false');
            });
            
            // Hide all tab contents
            tabContents.forEach(content => {
                content.style.display = 'none';
                content.classList.remove('active');
            });
            
            // Activate clicked button
            this.classList.add('active');
            this.setAttribute('aria-selected', 'true');
            
            // Show target tab content
            const targetContent = document.getElementById('tab-' + targetTab);
            if (targetContent) {
                targetContent.style.display = 'block';
                targetContent.classList.add('active');
                
                // Restart carousel if it exists
                const carousel = targetContent.querySelector('.carousel');
                if (carousel) {
                    const bsCarousel = new bootstrap.Carousel(carousel);
                    bsCarousel.cycle();
                }
            }
        });
    });
}

// Carousel enhancements
function initializeCarouselEnhancements() {
    const carousels = document.querySelectorAll('.fab-featured-carousel');
    
    carousels.forEach(carousel => {
        // Add smooth transition effects
        carousel.addEventListener('slide.bs.carousel', function(event) {
            const activeItem = event.relatedTarget;
            const card = activeItem.querySelector('.fab-product-card');
            
            if (card) {
                card.style.transform = 'scale(0.95)';
                card.style.opacity = '0.8';
                
                setTimeout(() => {
                    card.style.transform = 'scale(1)';
                    card.style.opacity = '1';
                }, 150);
            }
        });
        
        // Add pause on hover
        carousel.addEventListener('mouseenter', function() {
            const bsCarousel = bootstrap.Carousel.getInstance(this);
            if (bsCarousel) {
                bsCarousel.pause();
            }
        });
        
        carousel.addEventListener('mouseleave', function() {
            const bsCarousel = bootstrap.Carousel.getInstance(this);
            if (bsCarousel) {
                bsCarousel.cycle();
            }
        });
    });
}

// Featured card hover effects
function addFeaturedCardHoverEffects() {
    const featuredCards = document.querySelectorAll('.fab-product-card');
    
    featuredCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            // Add glow effect
            this.style.boxShadow = '0 20px 60px rgba(102, 126, 234, 0.2), 0 8px 32px rgba(0, 0, 0, 0.15)';
            
            // Scale image slightly
            const image = this.querySelector('.fab-product-img');
            if (image) {
                image.style.transform = 'scale(1.05)';
            }
            
            // Enhance badges
            const badges = this.querySelectorAll('.badge');
            badges.forEach(badge => {
                badge.style.transform = 'scale(1.05)';
            });
        });
        
        card.addEventListener('mouseleave', function() {
            // Reset effects
            this.style.boxShadow = '';
            
            const image = this.querySelector('.fab-product-img');
            if (image) {
                image.style.transform = '';
            }
            
            const badges = this.querySelectorAll('.badge');
            badges.forEach(badge => {
                badge.style.transform = '';
            });
        });
        
        // Add click effect for better UX
        card.addEventListener('click', function(e) {
            // Don't trigger if clicking on buttons
            if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON') {
                return;
            }
            
            // Find the "View Details" button and trigger it
            const viewDetailsBtn = this.querySelector('a[href*="asset_detail"]');
            if (viewDetailsBtn) {
                viewDetailsBtn.click();
            }
        });
    });
}

// Add loading animation for images
function addImageLoadingEffects() {
    const images = document.querySelectorAll('.fab-product-img');
    
    images.forEach(img => {
        if (img.tagName === 'IMG') {
            img.addEventListener('load', function() {
                this.style.opacity = '0';
                this.style.transform = 'scale(0.95)';
                
                setTimeout(() => {
                    this.style.transition = 'all 0.3s ease';
                    this.style.opacity = '1';
                    this.style.transform = 'scale(1)';
                }, 100);
            });
        }
    });
}

// Initialize image loading effects
document.addEventListener('DOMContentLoaded', function() {
    addImageLoadingEffects();
});

// Export functions for global use
window.FeaturedAssets = {
    initializeFeaturedSection,
    initializeFeaturedTabs,
    initializeCarouselEnhancements,
    addFeaturedCardHoverEffects,
    addImageLoadingEffects
};
