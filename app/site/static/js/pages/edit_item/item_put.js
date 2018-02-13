define(['jquery', 'submitForm', 'setHeaders'], function($, submitForm) {

  const itemPut = function(itemId) {

    // Process the form when button is clicked
    $('form').on('submit', (function(event) {

      // Define html elements
      var $nameField = $('#name-field');
      var $descriptionField = $('#description-field');
      var $categoryField = $('#category-field');

      // Create ajax configuration object
      var ajaxConfig = {};
      ajaxConfig.type = 'PUT';
      ajaxConfig.url = `/api/v1/items/${itemId}`;
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

  };

  return itemPut;

});
