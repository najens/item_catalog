define(
  ['jquery', 'methods', 'submitForm', 'setHeaders', 'deleteItemGet'],
  function($, methods, submitForm) {

  $(document).ready(function() {

    // Define html elements
    var $form = $('#form');

    // Process the form when button is clicked
    $('form').on('submit', (function(event) {

      // Create ajax configuration object
      var ajaxConfig = {};
      ajaxConfig.type = 'DELETE';
      ajaxConfig.url = `/api/v1/items/${methods.getItemId()}`;
      ajaxConfig.datatype = 'json';

      // Send ajax request to server
      submitForm(ajaxConfig);

      // Override default form functionality
      event.preventDefault();

    }));
  });
});
