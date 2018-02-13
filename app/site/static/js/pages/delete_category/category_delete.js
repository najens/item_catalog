define(['jquery', 'submitForm', 'setHeaders'],
  function($, submitForm) {

  const categoryDelete = function(categoryId) {

    // Process the form when button is clicked
    $('form').on('submit', (function(event) {

      // Create ajax configuration object
      var ajaxConfig = {};
      ajaxConfig.type = 'DELETE';
      ajaxConfig.url = `/api/v1/categories/${categoryId}`;
      ajaxConfig.datatype = 'json';

      // Send ajax request to server
      submitForm(ajaxConfig);

      // Override default form functionality
      event.preventDefault();

    }));

  }

  return categoryDelete;

});
