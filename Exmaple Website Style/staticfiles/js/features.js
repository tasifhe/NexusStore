// Enhanced Features Section JavaScript

// Add enhanced interactive features
function enhanceFeatureInteractions() {
    const featureCards = document.querySelectorAll('.feature-card');
    
    featureCards.forEach((card, index) => {
        // Add click interaction with enhanced feedback
        card.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove previous clicked state
            featureCards.forEach(c => c.classList.remove('clicked'));
            
            // Add clicked state
            this.classList.add('clicked');
            
            // Show feature details tooltip
            showFeatureTooltip(this, index);
            
            // Remove clicked state after animation
            setTimeout(() => {
                this.classList.remove('clicked');
            }, 600);
        });
        
        // Enhanced hover effects
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-15px) scale(1.02)';
            this.style.transition = 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
        
        // Add loading animation on first view
        setTimeout(() => {
            card.classList.add('loading');
        }, index * 100);
    });
    
    // Enhanced statistics interactions
    const statItems = document.querySelectorAll('.stat-item');
    statItems.forEach(item => {
        item.addEventListener('click', function() {
            const counter = this.querySelector('h3[data-counter]');
            if (counter) {
                // Re-animate counter
                counter.classList.add('counting');
                const target = +counter.getAttribute('data-counter');
                animateCounterValue(counter, 0, target, 1000);
                
                setTimeout(() => {
                    counter.classList.remove('counting');
                }, 1000);
            }
        });
    });
}

// Enhanced counter animation
function animateCounterValue(element, start, end, duration) {
    const startTime = performance.now();
    
    function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function for smooth animation
        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
        const currentValue = Math.floor(start + (end - start) * easeOutQuart);
        
        element.textContent = currentValue;
        
        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = end;
        }
    }
    
    requestAnimationFrame(updateCounter);
}

// Feature tooltip system
function showFeatureTooltip(card, index) {
    const featureData = [
        { title: 'Premium Quality', description: 'Professionally crafted assets with high-quality textures and optimized meshes' },
        { title: 'Easy Integration', description: 'Compatible with Unity, Unreal Engine, Blender, and other popular tools' },
        { title: 'Fair Pricing', description: 'Affordable rates with free assets and regular discounts for developers' },
        { title: 'Community Driven', description: 'Active community of 1200+ creators sharing knowledge and resources' },
        { title: 'Instant Download', description: 'Immediate access to your purchases with secure download links' },
        { title: 'Multiple Formats', description: 'Available in FBX, OBJ, Blend, PNG, and other industry-standard formats' }
    ];
    
    const tooltip = createTooltip(featureData[index]);
    card.appendChild(tooltip);
    
    setTimeout(() => {
        tooltip.classList.add('show');
    }, 100);
    
    // Auto-hide tooltip after 3 seconds
    setTimeout(() => {
        tooltip.classList.remove('show');
        setTimeout(() => {
            tooltip.remove();
        }, 300);
    }, 3000);
}

function createTooltip(data) {
    const tooltip = document.createElement('div');
    tooltip.className = 'feature-tooltip';
    tooltip.innerHTML = `
        <strong>${data.title}</strong><br>
        ${data.description}
    `;
    
    return tooltip;
}

// Feature showcase system
function initializeFeatureShowcase() {
    let currentFeature = 0;
    const features = document.querySelectorAll('.feature-card');
    
    function showcaseNext() {
        // Remove previous showcase
        features.forEach(f => f.classList.remove('feature-showcase-active'));
        
        // Add showcase to current feature
        if (features[currentFeature]) {
            features[currentFeature].classList.add('feature-showcase-active');
        }
        
        currentFeature = (currentFeature + 1) % features.length;
    }
    
    // Start showcase rotation
    setInterval(showcaseNext, 5000);
}

// Scroll-based feature activation
function initializeScrollFeatures() {
    const observerOptions = {
        threshold: 0.3,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const featureObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // Trigger counter animation if it's a stat item
                const counter = entry.target.querySelector('h3[data-counter]');
                if (counter && !counter.classList.contains('animated')) {
                    counter.classList.add('animated');
                    const target = +counter.getAttribute('data-counter');
                    animateCounterValue(counter, 0, target, 2000);
                }
            }
        });
    }, observerOptions);
    
    // Observe all feature cards and stat items
    document.querySelectorAll('.feature-card, .stat-item').forEach(el => {
        featureObserver.observe(el);
    });
}

// Add keyboard navigation
function initializeKeyboardNavigation() {
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
            const features = document.querySelectorAll('.feature-card');
            const currentFeatured = document.querySelector('.feature-card.featured');
            let currentIndex = currentFeatured ? Array.from(features).indexOf(currentFeatured) : -1;
            
            if (e.key === 'ArrowRight') {
                currentIndex = (currentIndex + 1) % features.length;
            } else {
                currentIndex = currentIndex <= 0 ? features.length - 1 : currentIndex - 1;
            }
            
            // Remove all featured states
            features.forEach(f => f.classList.remove('featured'));
            
            // Add featured state to new card
            features[currentIndex].classList.add('featured');
            features[currentIndex].scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    });
}

// Initialize all enhanced features
document.addEventListener('DOMContentLoaded', function() {
    // Initialize original features
    initializeFeatures();
    
    // Initialize enhanced features
    enhanceFeatureInteractions();
    initializeFeatureShowcase();
    initializeScrollFeatures();
    initializeKeyboardNavigation();
});

// Export enhanced functions
window.FeatureSection = {
    ...window.FeatureSection,
    enhanceFeatureInteractions,
    animateCounterValue,
    showFeatureTooltip,
    initializeFeatureShowcase,
    initializeScrollFeatures,
    initializeKeyboardNavigation
};

// Features Section JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeFeatures();
});

function initializeFeatures() {
    // Initialize counter animations
    initializeCounters();
    
    // Initialize feature card interactions
    initializeFeatureCards();
    
    // Initialize scroll animations
    initializeScrollAnimations();
}

// Counter Animation
function initializeCounters() {
    const counters = document.querySelectorAll('[data-counter]');
    const speed = 200; // Animation speed

    const countUp = (counter) => {
        const target = +counter.getAttribute('data-counter');
        const count = +counter.innerText;
        const increment = target / speed;

        if (count < target) {
            counter.innerText = Math.ceil(count + increment);
            setTimeout(() => countUp(counter), 1);
        } else {
            counter.innerText = target;
        }
    };

    // Intersection Observer for counter animation
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                counter.innerText = '0';
                countUp(counter);
                counterObserver.unobserve(counter);
            }
        });
    }, {
        threshold: 0.7
    });

    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
}

// Feature Cards Interactions
function initializeFeatureCards() {
    const featureCards = document.querySelectorAll('.feature-card');
    
    featureCards.forEach(card => {
        // Add click interaction
        card.addEventListener('click', function() {
            // Add pulse animation
            this.style.animation = 'pulse 0.6s ease-in-out';
            setTimeout(() => {
                this.style.animation = '';
            }, 600);
        });
        
        // Add hover sound effect (optional)
        card.addEventListener('mouseenter', function() {
            // You can add a subtle sound effect here if desired
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Scroll Animations
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const scrollObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // Stagger animation for feature cards
                if (entry.target.classList.contains('feature-card')) {
                    const cards = entry.target.parentElement.querySelectorAll('.feature-card');
                    cards.forEach((card, index) => {
                        setTimeout(() => {
                            card.style.opacity = '1';
                            card.style.transform = 'translateY(0)';
                        }, index * 100);
                    });
                }
                
                scrollObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements for scroll animation
    const animateElements = document.querySelectorAll('.features-section .row, .features-section .section-header');
    animateElements.forEach(el => {
        scrollObserver.observe(el);
    });
}

// Feature Showcase Function
function showcaseFeature(featureIndex) {
    const features = document.querySelectorAll('.feature-card');
    
    // Reset all features
    features.forEach(feature => {
        feature.classList.remove('featured');
    });
    
    // Highlight selected feature
    if (features[featureIndex]) {
        features[featureIndex].classList.add('featured');
        features[featureIndex].scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    }
}

// Utility function to show feature details
function showFeatureDetails(featureTitle, featureDescription) {
    // Create modal or tooltip with feature details
    const modal = document.createElement('div');
    modal.className = 'feature-modal';
    modal.innerHTML = `
        <div class="feature-modal-content">
            <h4>${featureTitle}</h4>
            <p>${featureDescription}</p>
            <button onclick="closeFeatureModal()" class="btn btn-primary">Got it!</button>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Add click outside to close
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeFeatureModal();
        }
    });
}

function closeFeatureModal() {
    const modal = document.querySelector('.feature-modal');
    if (modal) {
        modal.remove();
    }
}

// Export functions for global use
window.FeatureSection = {
    showcaseFeature,
    showFeatureDetails,
    closeFeatureModal
};

// Add some CSS for feature modal if it doesn't exist
if (!document.querySelector('#feature-modal-styles')) {
    const style = document.createElement('style');
    style.id = 'feature-modal-styles';
    style.textContent = `
        .feature-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            animation: fadeIn 0.3s ease;
        }
        
        .feature-modal-content {
            background: white;
            padding: 2rem;
            border-radius: 1rem;
            max-width: 500px;
            margin: 1rem;
            text-align: center;
            animation: slideUp 0.3s ease;
        }
        
        .feature-card.featured {
            transform: translateY(-15px) scale(1.05);
            box-shadow: 0 25px 50px rgba(102, 126, 234, 0.3) !important;
            border: 2px solid #667eea;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideUp {
            from { transform: translateY(30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
}
