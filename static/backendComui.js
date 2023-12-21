  function uploadFile() {
          var formData = new FormData(document.getElementById('upload-form'));
          formData.append('file', document.getElementById('file-upload').files[0]);
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

          console.log(selectedVariables + "and " + targetColumn + "and");
          formData.append('selected_columns', JSON.stringify(selectedVariables));
          formData.append('target_column', targetColumn);
          formData.append('data', document.getElementById('file-upload').files[0]);

          fetch('/predict', {
              method: 'POST',
              body: formData
          }).then(response => response.json())
              .then(data => {
                  displayResults(data);
              }).catch(error => console.error('Error:', error));
      }
         function displayResults(data) {
          if (data.error) {
              alert(data.error);
              return;
          }
          var resultsDiv = document.getElementById('results');
          resultsDiv.innerHTML = '<img src="data:image/png;base64,' + data.plot_url + '" />';
          // Display other results as needed
      }