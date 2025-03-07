function downloadResults() {
    window.location.href = '/download';
}
$(document).ready(function () {
$('#upload-form').on('submit', function (e) {
    e.preventDefault();

    var formData = new FormData(this);
    $.ajax({
        url: '/upload',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            if (response.results) {
                $('#visualization').hide();
            $('.btn-success').hide();

                // Results Table
                var headers = Object.keys(response.results[0]);

                var resultHtml = '<h3>Processed Results</h3><table class="table"><thead><tr>';
                for (var i = headers.length - 1; i >= 0; i--) {
                    resultHtml += '<th>' + headers[i] + '</th>';
                }
                resultHtml += '</tr></thead><tbody>';

                response.results.forEach(function(row) {
                    resultHtml += '<tr>';
                    for (var i = headers.length - 1; i >= 0; i--) {
                        resultHtml += '<td>' + row[headers[i]] + '</td>';
                    }
                    resultHtml += '</tr>';
                });
                resultHtml += '</tbody></table>';

                $('#results').html(resultHtml);

                $('#visualization').show();
        $('.btn-success').show();
            } else {
                $('#results').html('<p>No results found.</p>');
            }
        },
        error: function (xhr, status, error) {
            console.error(xhr.responseText);
            alert('Error: ' + error);
        },
    });
});
});