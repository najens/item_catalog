define(
  ['jquery', 'submitForm', 'setHeaders'],
  function($, submitForm) {

  const itemDelete = function(itemId) {

    // Define html elements
    var $form = $('#delete-item-form');

    // Process the form when button is clicked
    $('form').on('submit', (function(event) {

      // Create ajax configuration object
      var ajaxConfig = {};
      ajaxConfig.type = 'DELETE';
      ajaxConfig.url = `/api/v1/items/${itemId}`;
      ajaxConfig.datatype = 'json';

      // Send ajax request to server
      submitForm(ajaxConfig);

      // Override default form functionality
      event.preventDefault();

    }));

  };

  return itemDelete;

});
