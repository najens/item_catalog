define(
  ['jquery', 'submitForm', 'setHeaders'],
  function($, submitForm, setHeaders) {

  $(document).ready(function() {

    // Define html elements
    var $nameField = $('#name-field');

    // Process the form when button is clicked
    $('form').on('submit', (function(event) {

      // Create ajax configuration object
      var ajaxConfig = {};
      ajaxConfig.type = 'POST';
      ajaxConfig.url = '/api/v1/categories';
      ajaxConfig.datatype = 'json';
      ajaxConfig.data = {
        name: $nameField.val().toLowerCase()
      };

      // Send ajax request to server
      submitForm(ajaxConfig);

      // Override default form functionality
      event.preventDefault();

    }));
  });
});
