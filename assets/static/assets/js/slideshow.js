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
});
