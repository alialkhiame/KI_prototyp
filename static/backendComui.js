
let files=null;

function uploadFile(fileInput, x) {
    files = x;
console.log("uploadFile Call");
   // let fileInput = document.querySelector(".default-file-input");

    if (!fileInput) {
        console.error('File input element not found');
        return;
    }


    var formData = new FormData(document.getElementById('upload-form'));
    formData.append('file', fileInput);

    console.log("i am here"+fileInput);
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
    var formData = new FormData();
    let fileInput = files;



    console.log("Selected Variables:", selectedVariables);
    console.log("Target Column:", targetColumn);
    console.log("File Input Element:", fileInput);


    formData.append('data', fileInput);


    console.log("Form Data:", formData); // Check the FormData contents

    fetch('/predict', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
    .then(data => {
        displayResults(data);
    }).catch(error => console.error('Error:', error));
}
  function displayResults(data) {

            console.log("my Data"+data)
            if (data.error) {
                alert(data.error);
                return;
            }
            var resultsDiv = document.getElementById('results');
             var resultsDiv2 = document.getElementById('asd');
            resultsDiv.innerHTML = '<img src="data:image/png;base64,' + data + '" />';
            resultsDiv2.innerHTML = data;
            resultsDiv.innerHTML = '<img src="data:image/png;base64,' + data.plot_url + '" />';
            // Display other results as needed
        }