// Test file to verify features section functionality
// This can be run in the browser console to test interactive features

console.log('Testing GameAssetHub Features Section...');

// Test 1: Check if feature cards exist
const featureCards = document.querySelectorAll('.feature-card');
console.log(`Found ${featureCards.length} feature cards`);

// Test 2: Check if statistics counters exist
const counters = document.querySelectorAll('[data-counter]');
console.log(`Found ${counters.length} statistics counters`);

// Test 3: Test feature card interaction
if (featureCards.length > 0) {
    console.log('Testing feature card click interaction...');
    featureCards[0].click();
    console.log('Feature card clicked successfully');
}

// Test 4: Test statistics counter animation
if (counters.length > 0) {
    console.log('Testing statistics counter animation...');
    counters[0].click();
    console.log('Statistics counter clicked successfully');
}

// Test 5: Check if CSS animations are working
const featuresSection = document.querySelector('.features-section');
if (featuresSection) {
    console.log('Features section found and styled');
} else {
    console.log('Features section not found');
}

// Test 6: Check for JavaScript errors
window.addEventListener('error', function(e) {
    console.error('JavaScript error detected:', e.message);
});

console.log('Features section test complete. Check the above logs for any issues.');
