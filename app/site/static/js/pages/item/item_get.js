define(['jquery', 'methods'], function($, methods) {

  $(document).ready(function() {

    // Define html elements
    var $itemContainer = $('#item-container');

    // Send get request to server
    $.getJSON(`/api/v1/items/${methods.getItemId()}`)

    // If request succesful, insert data into html container
    .done(function(data){
      var htmlString = `
      <div class="left item-info">
        <h3>${methods.toTitleCase(data.item.name)}</h3>
        <p>Description: ${data.item.description}</p>
      </div>
      `;
      $itemContainer.append(htmlString);
    })

    // If request failed, display error in console
    .fail(function(error) {
      if (error.responseJSON.error) {
        console.log('Error: ' + error.responseJSON.error);
      }
    });

  });
});
