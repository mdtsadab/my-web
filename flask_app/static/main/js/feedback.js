// Feedback modal functions
function toggleMenu() {
    const navRight = document.querySelector('.nav-right');
    navRight.classList.toggle('show');
}

function openFeedbackModal() {
    document.getElementById('feedbackModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

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

function submitFeedback(event) {
    event.preventDefault();
    
    const form = document.getElementById('feedbackForm');
    const formData = new FormData(form);
    
    fetch('/feedback', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Redirect to feedback list page
            window.location.href = '/feedback-list';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error submitting feedback. Please try again.');
    });
}