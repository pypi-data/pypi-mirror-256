// Before executing the URL "example.com/extract/53" there should be a check for whether
// the file with file_id 53 had already been processed. Create an "is_processed" field
// in the GameCollection model so that it can be set to True for processed files.

// Try using vanilla JavaScript instead of jQuery.
// Call urls asynchronously using vanilla javascript and use the return values.


$(document).ready(function() {

    var process_alert = "Processing of games is in progress...";

    $("#process_progress").html(process_alert);

    xhr = new XMLHttpRequest();

    var extraction_url = $("#upload_url").text();

    var process_alert = "Processing x of games is in progress...";

    xhr.open("GET", extraction_url);

    xhr.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status >= 200 && this.status < 300) {
                // Success
                $("#debugging_message").html("Debugging Message: " + extraction_url);
                $("#process_progress").html("Processing successful.");
            } else {
                // Unsuccessful
                $("#process_progress").html("Processing failed. Sorry.");
            }
        }
    }

    xhr.send();

});

