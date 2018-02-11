define(['jquery'], function($) {

  // Success alert
  const successAlert = function(alert) {
    if (alert) {
      console.log('Success: ' + alert);
      $successAlert.text(alert).show();
      $errorAlert.hide();
      setTimeout(function() {
        window.location.href = '/';
      }, 1000);
    }
  }

  // Fail alert
  const failAlert = function(alert) {
    if (alert) {
      console.log('Error: ' + alert);
      $errorAlert.text(alert).show();
      $successAlert.hide();
      setTimeout(function() {
        $errorAlert.text(alert).hide();
      }, 3000);
    }
  }

  // Create object of methods
  var formAlerts = {};
  formAlerts.successAlert = successAlert;
  formAlerts.failAlert = failAlert;

  console.log(formAlerts);

  return formAlerts;

});
