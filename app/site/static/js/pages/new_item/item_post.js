define(
  ['jquery', 'submitForm', 'setHeaders'],
  function($, submitForm) {

  const itemPost = function() {

    // Process the form when button is clicked
    $('form').on('submit', (function(event) {

      //Define html elements
      var $nameField = $('#name-field');
      var $descriptionField = $('#description-field');
      var $categoryField = $('#category-field');

      // Create ajax configuration object
      var ajaxConfig = {};
      ajaxConfig.type = 'POST';
      ajaxConfig.url = '/api/v1/items';
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

  return itemPost;

});
