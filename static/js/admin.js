// Admin Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Modal handling
    setupModals();
    
    // Form submissions
    setupFormSubmissions();
});

// Setup modal functionality
function setupModals() {
    // Add Subject button
    const addSubjectBtn = document.querySelector('a[href*="add_subject"]');
    if (addSubjectBtn) {
        addSubjectBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showModal('addSubjectModal');
        });
    }
    
    // Add Chapter buttons
    const addChapterBtns = document.querySelectorAll('a[href*="add_chapter"]');
    addChapterBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            showModal('addChapterModal');
        });
    });
    
    // Add Quiz button
    const addQuizBtn = document.querySelector('a[href*="add_quiz"]');
    if (addQuizBtn) {
        addQuizBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showModal('addQuizModal');
        });
    }
    
    // Add Question buttons
    const addQuestionBtns = document.querySelectorAll('a.btn-edit');
    addQuestionBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            showModal('addQuestionModal');
        });
    });
    
    // Cancel buttons
    const cancelBtns = document.querySelectorAll('.btn-cancel');
    cancelBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            hideAllModals();
        });
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            hideAllModals();
        }
    });
}

// Show a specific modal
function showModal(modalId) {
    hideAllModals();
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show');
    }
}

// Hide all modals
function hideAllModals() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.classList.remove('show');
    });
}

// Setup form submissions
function setupFormSubmissions() {
    // Subject form
    const subjectForm = document.querySelector('#addSubjectModal .form-actions .btn-save');
    if (subjectForm) {
        subjectForm.addEventListener('click', function() {
            const name = document.getElementById('subject-name').value;
            const description = document.getElementById('subject-description').value;
            
            if (!name) {
                alert('Please enter a subject name');
                return;
            }
            
            // Send data to server
            submitFormData('/admin/subject/add', {
                name: name,
                description: description
            });
        });
    }
    
    // Chapter form
    const chapterForm = document.querySelector('#addChapterModal .form-actions .btn-save');
    if (chapterForm) {
        chapterForm.addEventListener('click', function() {
            const name = document.getElementById('chapter-name').value;
            const description = document.getElementById('chapter-description').value;
            
            if (!name) {
                alert('Please enter a chapter name');
                return;
            }
            
            // Send data to server
            submitFormData('/admin/chapter/add', {
                name: name,
                description: description
            });
        });
    }
    
    // Quiz form
    const quizForm = document.querySelector('#addQuizModal .form-actions .btn-save');
    if (quizForm) {
        quizForm.addEventListener('click', function() {
            const chapterId = document.getElementById('quiz-chapter-id').value;
            const title = document.getElementById('quiz-title').value;
            const duration = document.getElementById('quiz-duration').value;
            
            if (!chapterId || !title || !duration) {
                alert('Please fill in all required fields');
                return;
            }
            
            // Send data to server
            submitFormData('/admin/quiz/add', {
                chapter_id: chapterId,
                title: title,
                duration: duration
            });
        });
    }
    
    // Question form
    const questionSaveBtn = document.querySelector('#addQuestionModal .btn-save');
    if (questionSaveBtn) {
        questionSaveBtn.addEventListener('click', function() {
            saveQuestion(true);
        });
    }
    
    const questionFinishBtn = document.querySelector('#addQuestionModal .btn-finish');
    if (questionFinishBtn) {
        questionFinishBtn.addEventListener('click', function() {
            saveQuestion(false);
        });
    }
}

// Save question data
function saveQuestion(addAnother) {
    const chapterId = document.getElementById('chapter-id').value;
    const title = document.getElementById('question-title').value;
    const statement = document.getElementById('question-statement').value;
    const option1 = document.getElementById('option1').value;
    const option2 = document.getElementById('option2').value;
    const option3 = document.getElementById('option3').value;
    const option4 = document.getElementById('option4').value;
    const correctOption = document.getElementById('correct-option').value;
    
    if (!chapterId || !title || !statement || !option1 || !option2 || !option3 || !option4 || !correctOption) {
        alert('Please fill in all required fields');
        return;
    }
    
    // Send data to server
    submitFormData('/admin/question/add', {
        chapter_id: chapterId,
        title: title,
        statement: statement,
        options: [option1, option2, option3, option4],
        correct_option: correctOption,
        add_another: addAnother
    });
}

// Submit form data to server
function submitFormData(url, data) {
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message || 'Operation successful!');
            if (!data.add_another) {
                hideAllModals();
                // Reload page to show new data
                window.location.reload();
            } else {
                // Clear form for next entry
                clearFormFields();
            }
        } else {
            alert(data.message || 'An error occurred');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing your request');
    });
}

// Clear form fields
function clearFormFields() {
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        if (input.type !== 'button' && input.type !== 'submit') {
            input.value = '';
        }
    });
} 