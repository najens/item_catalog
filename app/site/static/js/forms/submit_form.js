define(['jquery'], function($) {

  // Submit form and handle response
  const submitForm = function(ajaxConfig) {

    var $successAlert = $('#success-alert');
    var $errorAlert = $('#error-alert');

    // Send ajax request to server
    $.ajax(ajaxConfig)

    // If request successful, alert user and return to home page
    .done(function(data) {
      const alert = data.success;
      if (alert) {
        console.log('Success: ' + alert);
        $(document).ready(function() {
          $successAlert.text(alert).show();
          $errorAlert.hide();
        });
        setTimeout(function() {
          window.location.href = '/';
        }, 1000);
      }
    })

    // If request failed, alert user
    .fail(function(error) {
      const alert = error.responseJSON.error;
      if (alert) {
        console.log('Error: ' + alert);
        $(document).ready(function() {
          $errorAlert.text(alert).show();
          $successAlert.hide();
          setTimeout(function() {
            $errorAlert.text(alert).hide();
          }, 3000);
        });
      }
    });

  };

  return submitForm;

});
