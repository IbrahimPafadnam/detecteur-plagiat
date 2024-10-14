// static/js/main.js
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