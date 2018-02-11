define(['jquery', 'methods', 'submitForm', 'setHeaders',
        'editItemGetItem', 'editItemGetCategory'],
        function($, methods, submitForm) {

  $(document).ready(function() {

    // Define html elements
    var $nameField = $('#name-field');
    var $descriptionField = $('#description-field');
    var $categoryField = $('#category-field');

    // Process the form when button is clicked
    $('form').on('submit', (function(event) {

      // Create ajax configuration object
      var ajaxConfig = {};
      ajaxConfig.type = 'PUT';
      ajaxConfig.url = `/api/v1/items/${methods.getItemId()}`;
      ajaxConfig.datatype = 'json';
      ajaxConfig.data = {
        name: $nameField.val().toLowerCase(),
        description: $descriptionField.val(),
        category: $categoryField.val().toLowerCase()
      };

      // Send ajax request to server
      submitForm(ajaxConfig);

      // Override default form functionality
      event.preventDefault();

    }));
  });
});
