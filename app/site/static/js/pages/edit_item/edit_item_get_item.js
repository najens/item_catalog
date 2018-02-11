define(['jquery', 'methods'], function($, methods) {

  $(document).ready(function() {

    // Define html elements
    var $nameField = $('#name-field');
    var $descriptionField = $('#description-field');

    // Send get request to server
    $.getJSON(`/api/v1/items/${methods.getItemId()}`)

    // If request successful, load form with data
    .done(function(data){
      $nameField.val(methods.toTitleCase(data.item.name));
      $descriptionField.val(data.item.description);
    })

    // If request failed, display error in console
    .fail(function(error) {
      if (error.responseJSON.error) {
        console.log('Error: ' + error.responseJSON.error);
      }
    });

  });
});
