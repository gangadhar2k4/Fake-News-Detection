/**
 * Dashboard JavaScript functionality for Fake News Detector
 * Handles interactive features, AJAX updates, and UI enhancements
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard functionality
    initializeDashboard();
    initializeTooltips();
    initializeFormHandlers();
    initializeRealTimeUpdates();
});

/**
 * Initialize main dashboard functionality
 */
function initializeDashboard() {
    // Add click-to-refresh functionality for statistics cards
    const statCards = document.querySelectorAll('.card.bg-info, .card.bg-success, .card.bg-danger, .card.bg-warning');
    statCards.forEach(card => {
        card.style.cursor = 'pointer';
        card.addEventListener('click', function() {
            refreshUserStats();
        });
    });

    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Initialize copy-to-clipboard functionality
    initializeClipboard();
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize form handlers and validation
 */
function initializeFormHandlers() {
    // Quick verification form handler
    const quickForms = document.querySelectorAll('form[action*="verify"]');
    quickForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            // Show loading state
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
            submitBtn.disabled = true;
            
            // Re-enable after 30 seconds as fallback
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 30000);
        });
    });

    // Bookmark toggle handlers
    const bookmarkForms = document.querySelectorAll('form[action*="bookmark"]');
    bookmarkForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            handleBookmarkToggle(this);
        });
    });

    // Search form auto-submit with debounce
    const searchInputs = document.querySelectorAll('input[name="search"]');
    searchInputs.forEach(input => {
        let debounceTimer;
        input.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                if (this.value.length > 2 || this.value.length === 0) {
                    this.form.submit();
                }
            }, 500);
        });
    });
}

/**
 * Handle bookmark toggle with AJAX
 */
function handleBookmarkToggle(form) {
    const formData = new FormData(form);
    const submitBtn = form.querySelector('button[type="submit"]');
    const icon = submitBtn.querySelector('i');
    
    // Show loading state
    icon.className = 'fas fa-spinner fa-spin';
    submitBtn.disabled = true;
    
    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update button state
            if (data.bookmarked) {
                submitBtn.classList.remove('btn-outline-warning');
                submitBtn.classList.add('btn-warning');
                icon.className = 'fas fa-bookmark';
                submitBtn.title = 'Remove bookmark';
            } else {
                submitBtn.classList.remove('btn-warning');
                submitBtn.classList.add('btn-outline-warning');
                icon.className = 'fas fa-bookmark';
                submitBtn.title = 'Bookmark';
            }
            
            // Show success message
            showToast('Bookmark updated successfully', 'success');
            
            // Refresh stats if on dashboard
            if (window.location.pathname.includes('dashboard')) {
                refreshUserStats();
            }
        } else {
            showToast('Failed to update bookmark', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('An error occurred', 'error');
        // Fallback to regular form submission
        form.submit();
    })
    .finally(() => {
        submitBtn.disabled = false;
    });
}

/**
 * Refresh user statistics via AJAX
 */
function refreshUserStats() {
    const statsApiUrl = '/dashboard/api/stats/';
    
    fetch(statsApiUrl, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.json())
    .then(data => {
        // Update stat cards
        updateStatCard('total_checks', data.total_checks);
        updateStatCard('true_news', data.true_news);
        updateStatCard('fake_news', data.fake_news);
        updateStatCard('bookmarked', data.bookmarked);
        
        showToast('Statistics updated', 'success');
    })
    .catch(error => {
        console.error('Error refreshing stats:', error);
    });
}

/**
 * Update individual stat card
 */
function updateStatCard(type, value) {
    const selectors = {
        'total_checks': '.card.bg-info .h4',
        'true_news': '.card.bg-success .h4',
        'fake_news': '.card.bg-danger .h4',
        'bookmarked': '.card.bg-warning .h4'
    };
    
    const element = document.querySelector(selectors[type]);
    if (element) {
        // Animate the number change
        animateNumber(element, parseInt(element.textContent), value, 500);
    }
}

/**
 * Animate number changes
 */
function animateNumber(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16); // 60fps
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current);
    }, 16);
}

/**
 * Initialize real-time updates
 */
function initializeRealTimeUpdates() {
    // Update stats every 5 minutes if on dashboard
    if (window.location.pathname.includes('dashboard')) {
        setInterval(refreshUserStats, 300000); // 5 minutes
    }
    
    // Auto-refresh trending topics every 10 minutes
    setInterval(refreshTrendingTopics, 600000); // 10 minutes
}

/**
 * Refresh trending topics
 */
function refreshTrendingTopics() {
    // This would typically make an AJAX call to get updated trending topics
    // For now, we'll just add a visual indicator that data is being refreshed
    const trendingCard = document.querySelector('.card:has(h5:contains("Trending Topics"))');
    if (trendingCard) {
        trendingCard.style.opacity = '0.7';
        setTimeout(() => {
            trendingCard.style.opacity = '1';
        }, 1000);
    }
}

/**
 * Initialize copy-to-clipboard functionality
 */
function initializeClipboard() {
    // Add copy buttons to article content in history
    const contentElements = document.querySelectorAll('.card-text');
    contentElements.forEach(element => {
        if (element.textContent.length > 50) {
            const copyBtn = document.createElement('button');
            copyBtn.className = 'btn btn-sm btn-outline-secondary ms-2';
            copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
            copyBtn.title = 'Copy content';
            copyBtn.addEventListener('click', function(e) {
                e.preventDefault();
                copyToClipboard(element.textContent);
                this.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(() => {
                    this.innerHTML = '<i class="fas fa-copy"></i>';
                }, 2000);
            });
            
            element.parentNode.appendChild(copyBtn);
        }
    });
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Content copied to clipboard', 'success');
        }).catch(err => {
            console.error('Failed to copy: ', err);
            fallbackCopyToClipboard(text);
        });
    } else {
        fallbackCopyToClipboard(text);
    }
}

/**
 * Fallback copy method for older browsers
 */
function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showToast('Content copied to clipboard', 'success');
    } catch (err) {
        console.error('Fallback copy failed: ', err);
        showToast('Failed to copy content', 'error');
    }
    
    document.body.removeChild(textArea);
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1080';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <i class="fas fa-${getToastIcon(type)} me-2 text-${getToastColor(type)}"></i>
                <strong class="me-auto">Fake News Detector</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    
    // Initialize and show toast
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 3000
    });
    
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

/**
 * Get toast icon based on type
 */
function getToastIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-triangle',
        'warning': 'exclamation-circle',
        'info': 'info-circle'
    };
    return icons[type] || icons['info'];
}

/**
 * Get toast color based on type
 */
function getToastColor(type) {
    const colors = {
        'success': 'success',
        'error': 'danger',
        'warning': 'warning',
        'info': 'info'
    };
    return colors[type] || colors['info'];
}

/**
 * Initialize keyboard shortcuts
 */
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl+Enter or Cmd+Enter to submit verification form
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const activeForm = document.querySelector('form:has(textarea:focus)');
            if (activeForm) {
                activeForm.submit();
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                const modal = bootstrap.Modal.getInstance(openModal);
                if (modal) {
                    modal.hide();
                }
            }
        }
    });
}

/**
 * Initialize progressive web app features
 */
function initializePWA() {
    // Add to home screen prompt
    let deferredPrompt;
    
    window.addEventListener('beforeinstallprompt', function(e) {
        e.preventDefault();
        deferredPrompt = e;
        
        // Show install button if not already installed
        if (!window.matchMedia('(display-mode: standalone)').matches) {
            showInstallPromotion();
        }
    });
    
    // Handle app installation
    window.addEventListener('appinstalled', function(e) {
        console.log('PWA was installed');
        hideInstallPromotion();
    });
}

/**
 * Show PWA install promotion
 */
function showInstallPromotion() {
    // Create install banner
    const installBanner = document.createElement('div');
    installBanner.className = 'alert alert-info alert-dismissible fade show position-fixed bottom-0 start-0 end-0 m-3';
    installBanner.style.zIndex = '1070';
    installBanner.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-mobile-alt me-3"></i>
            <div class="flex-grow-1">
                <strong>Install Fake News Detector</strong><br>
                <small>Add to your home screen for quick access</small>
            </div>
            <button type="button" class="btn btn-primary btn-sm me-2" onclick="installPWA()">
                Install
            </button>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    document.body.appendChild(installBanner);
}

/**
 * Hide PWA install promotion
 */
function hideInstallPromotion() {
    const installBanner = document.querySelector('.alert:has(.fa-mobile-alt)');
    if (installBanner) {
        installBanner.remove();
    }
}

/**
 * Install PWA
 */
function installPWA() {
    if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then(function(choiceResult) {
            if (choiceResult.outcome === 'accepted') {
                console.log('User accepted the install prompt');
                hideInstallPromotion();
            }
            deferredPrompt = null;
        });
    }
}

/**
 * Initialize chart interactions
 */
function initializeChartInteractions() {
    // Add click handlers to chart elements for drill-down functionality
    const charts = Chart.instances;
    Object.values(charts).forEach(chart => {
        chart.options.onClick = function(event, elements) {
            if (elements.length > 0) {
                const element = elements[0];
                const datasetIndex = element.datasetIndex;
                const index = element.index;
                
                // Handle chart clicks for navigation
                if (chart.canvas.id === 'resultsChart') {
                    const labels = ['True', 'Fake', 'Partially True'];
                    const filterType = labels[index];
                    if (filterType) {
                        window.location.href = `/verifier/history/?result_filter=${filterType}`;
                    }
                }
            }
        };
    });
}

/**
 * Initialize accessibility features
 */
function initializeAccessibility() {
    // Add ARIA labels to interactive elements
    document.querySelectorAll('[data-bs-toggle]').forEach(element => {
        if (!element.getAttribute('aria-label')) {
            const toggle = element.getAttribute('data-bs-toggle');
            element.setAttribute('aria-label', `Toggle ${toggle}`);
        }
    });
    
    // Add keyboard navigation for custom elements
    document.querySelectorAll('.card[style*="cursor: pointer"]').forEach(card => {
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
        card.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });
}

/**
 * Initialize error handling
 */
function initializeErrorHandling() {
    // Global error handler
    window.addEventListener('error', function(e) {
        console.error('Global error:', e.error);
        showToast('An unexpected error occurred', 'error');
    });
    
    // Unhandled promise rejection handler
    window.addEventListener('unhandledrejection', function(e) {
        console.error('Unhandled promise rejection:', e.reason);
        showToast('A network error occurred', 'error');
    });
    
    // Network status monitoring
    window.addEventListener('online', function() {
        showToast('Connection restored', 'success');
    });
    
    window.addEventListener('offline', function() {
        showToast('Connection lost. Some features may not work.', 'warning');
    });
}

// Initialize additional features when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeKeyboardShortcuts();
    initializePWA();
    initializeChartInteractions();
    initializeAccessibility();
    initializeErrorHandling();
});

// Make functions available globally for inline event handlers
window.installPWA = installPWA;
window.refreshUserStats = refreshUserStats;
window.showToast = showToast;
