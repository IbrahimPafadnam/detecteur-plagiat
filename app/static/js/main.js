// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Initialiser les icônes Feather
    feather.replace();

    // Afficher le nom des fichiers sélectionnés
    const fileInput = document.getElementById('files');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const fileNames = Array.from(e.target.files).map(file => file.name).join(', ');
            const fileLabel = document.querySelector('label[for="file"]');
            fileLabel.innerHTML = `<i data-feather="file-text"></i> ${fileNames || 'Choisissez un ou plusieurs fichiers'}`;
            feather.replace();
        });
    }

    // Ajouter une animation de chargement lors de la soumission du formulaire
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function() {
            const submitButton = this.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyse en cours...';
        });
    }


    // Ajouter des tooltips Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
});




document.addEventListener('DOMContentLoaded', function() {
    const compareButtons = document.querySelectorAll('.compare-files');
    compareButtons.forEach(button => {
        button.addEventListener('click', function() {
            const file1 = this.dataset.file1;
            const file2 = this.dataset.file2;
            compareFiles(file1, file2);
        });
    });
});

function compareFiles(file1, file2) {
    Promise.all([
        getFileContent(file1),
        getFileContent(file2)
    ]).then(([content1, content2]) => {
        displayComparison(file1, content1, file2, content2);
    }).catch(error => {
        console.error('Error fetching file contents:', error);
    });
}

function getFileContent(filename) {
    return fetch('/get_file_content', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filename: filename }),
    })
    .then(response => response.json())
    .then(data => data.content);
}

function displayComparison(file1, content1, file2, content2) {
    document.getElementById('file1-name').textContent = file1;
    document.getElementById('file2-name').textContent = file2;
    
    const highlightedContent1 = highlightSimilarities(content1, content2);
    const highlightedContent2 = highlightSimilarities(content2, content1);
    
    document.getElementById('file1-content').innerHTML = highlightedContent1;
    document.getElementById('file2-content').innerHTML = highlightedContent2;
    
    document.getElementById('file-comparison').style.display = 'block';
}

function highlightSimilarities(text1, text2) {
    const words1 = text1.split(/\s+/);
    const words2 = text2.split(/\s+/);
    
    return words1.map(word => {
        if (words2.includes(word)) {
            return `<span class="highlighted">${word}</span>`;
        }
        return word;
    }).join(' ');
}