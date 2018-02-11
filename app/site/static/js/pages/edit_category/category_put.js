define(
  ['jquery', 'methods', 'submitForm', 'setHeaders'],
  function($, methods, submitForm) {

  $(document).ready(function() {

    // Define html elements
    var $nameField = $('#name-field');

    // Process the form when button is clicked
    $('form').on('submit', (function(event) {

      // Create ajax configuration object
      var ajaxConfig = {};
      ajaxConfig.type = 'PUT';
      ajaxConfig.url = `/api/v1/categories/${methods.getCategoryId()}`;
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
