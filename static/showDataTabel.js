function displayDataTable(data) {
    // Delete previously created data table so there is only 1 table displayed
    document.getElementById('dataTable').innerHTML = '';

    // Create a table element
    var table = document.createElement('table');

    // Create table header
    var thead = document.createElement('thead');
    var headerRow = document.createElement('tr');

    // The first row of the data array contains the column headers
    var columns = data[0];

    // Create header cells
    columns.forEach(function (column) {
        var th = document.createElement('th');
        th.textContent = column;
        headerRow.appendChild(th);
    });

    // Append the header row to the thead
    thead.appendChild(headerRow);

    // Append the thead to the table
    table.appendChild(thead);

    // Create table body
    var tbody = document.createElement('tbody');

    // Skip the first row (header), and create rows and cells for the data
    for (let i = 1; i < data.length; i++) {
        var tr = document.createElement('tr');
        data[i].forEach(function (cellData) {
            var td = document.createElement('td');
            td.textContent = cellData;
            tr.appendChild(td);
        });

        // Append the row to the tbody
        tbody.appendChild(tr);
    }

    // Append the tbody to the table
    table.appendChild(tbody);

    // Append the table to the container in the HTML document
    document.getElementById('dataTable').appendChild(table);
}
