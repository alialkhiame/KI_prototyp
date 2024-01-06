let files = null;

function uploadFile(fileInput, x) {
    files = fileInput;
    console.log("uploadFile Call");
    // let fileInput = document.querySelector(".default-file-input");

    if (!files) {
        console.error('File input element not found');
        return;
    }

    files.fileNotClean = x;
    var formData = new FormData(document.getElementById('upload-form'));
    formData.append('file', files);
    formData.append('fileNotClean', x);
    console.log("i am here" + files);
    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
        .then(data => {
            populateVariableSelection(data.columns);
        }).catch(error => console.error('Error:', error));
}

function populateVariableSelection(columns) {
    var selectionDiv = document.getElementById('variable-selection');
    var targetColumnSelect = document.getElementById('target-column');
    selectionDiv.innerHTML = '';
    targetColumnSelect.innerHTML = '';

    columns.forEach(column => {
        // Checkbox for variable selection
        var checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = column;
        checkbox.name = 'variables';
        checkbox.value = column;

        var label = document.createElement('label');
        label.htmlFor = column;
        label.appendChild(document.createTextNode(column));

        selectionDiv.appendChild(checkbox);
        selectionDiv.appendChild(label);
        selectionDiv.appendChild(document.createElement('br'));

        // Option for target column
        var option = document.createElement('option');
        option.value = column;
        option.text = column;
        targetColumnSelect.appendChild(option);
    });

}

function startPrediction() {
    var selectedVariables = Array.from(document.querySelectorAll('input[name="variables"]:checked')).map(cb => cb.value);
    var targetColumn = document.getElementById('target-column').value;


    let fileInput = files;
    var formData = new FormData();


    console.log("Selected Variables:", JSON.stringify(selectedVariables));
    console.log("Target Column:", targetColumn);
    console.log("File Input Element:", fileInput);


    formData.append('selected_columns', JSON.stringify(selectedVariables));
    formData.append('target_column', targetColumn);
    formData.append('file', fileInput);
    formData.append('fileNotClean', fileInput.fileNotClean);

    console.log("Form Data:", formData); // Check the FormData contents

    fetch('/predict', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
        .then(data => {
            displayResults(data);
        }).catch(error => console.error('Error:', error));
    var form = document.getElementById('upload-form');
    var dataTa = document.getElementById('dataTable');
    var p = document.getElementById('h');
    var pp = document.getElementById('hh');
    var ppp = document.getElementById('overall-sentiment');
    var pppp = document.getElementById('overall-score');
    p.remove();
    pp.remove();
    ppp.remove();
    pppp.remove();
    form.remove();
    dataTa.remove();
}

function displayResults(data) {

    console.log("my Data" + data)


    var resultsDiv = document.getElementById('resultImage');

// Assuming 'data' is an object with 'plot_url' as a property containing the base64 string
// and another base64 string directly in 'data'
    resultsDiv.innerHTML =
        '<img src="data:image/png;base64,' + data.plot_url + '" />';

    // Display other results as needed
}