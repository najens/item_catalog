define(['jquery', 'methods', 'submitForm', 'setHeaders'],
  function($, methods, submitForm) {

  $(document).ready(function() {

    // Process the form when button is clicked
    $('form').on('submit', (function(event) {

      // Create ajax configuration object
      var ajaxConfig = {};
      ajaxConfig.type = 'DELETE';
      ajaxConfig.url = `/api/v1/categories/${methods.getCategoryId()}`;
      ajaxConfig.datatype = 'json';

      // Send ajax request to server
      submitForm(ajaxConfig);

      // Override default form functionality
      event.preventDefault();

    }));
  });
});
