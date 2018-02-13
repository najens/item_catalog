define(
  ['jquery', 'submitForm', 'setHeaders'],
  function($, submitForm) {

  const categoryPut = function(categoryId) {

    // Process the form when button is clicked
    $('form').on('submit', (function(event) {

      // Define html elements
      var $nameField = $('#name-field');

      // Create ajax configuration object
      var ajaxConfig = {};
      ajaxConfig.type = 'PUT';
      ajaxConfig.url = `/api/v1/categories/${categoryId}`;
      ajaxConfig.datatype = 'json';
      ajaxConfig.data = {
        name: $nameField.val().toLowerCase()
      };

      // Send ajax request to server
      submitForm(ajaxConfig);

      // Override default form functionality
      event.preventDefault();

    }));

  };

  return categoryPut;

});
