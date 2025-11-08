// Menu toggle for mobile
function toggleMenu() {
    const navRight = document.querySelector('.nav-right');
    navRight.classList.toggle('show');
}

// Open contact modal
function openFeedbackModal() {
    document.getElementById('feedbackModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

// Close contact modal
function closeFeedbackModal() {
    document.getElementById('feedbackModal').style.display = 'none';
    document.body.style.overflow = 'auto';
    document.getElementById('feedbackForm').reset();
    document.getElementById('feedbackSuccess').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('feedbackModal');
    if (event.target == modal) {
        closeFeedbackModal();
    }
}

// Close modal with Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeFeedbackModal();
    }
});

// Submit contact form
function submitFeedback(event) {
    event.preventDefault();
    
    const form = document.getElementById('feedbackForm');
    const formData = new FormData(form);
    const submitBtn = document.querySelector('.feedback-submit-btn');
    
    // Disable button and show loading state
    submitBtn.disabled = true;
    submitBtn.textContent = 'SENDING...';
    
    fetch('/feedback', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Redirect to messages page
            window.location.href = '/feedback-list';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error sending message. Please try again or email me directly at sadabmd@msu.edu');
        submitBtn.disabled = false;
        submitBtn.textContent = 'SEND MESSAGE';
    });
}