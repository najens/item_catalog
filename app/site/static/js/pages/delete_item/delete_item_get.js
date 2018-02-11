define(['jquery', 'methods'], function($, methods) {

  $(document).ready(function() {

    // Define html elements
    var $form = $('#form');

    // Send get request to server
    $.getJSON(`/api/v1/items/${methods.getItemId()}`)

    // If request successful, load form with delete prompt
    .done(function(data){
      var htmlString = `
      <div class="form-group">
        <h3>
          Are you sure you want to delete
          <span>${methods.toTitleCase(data.item.name)}</span>
          ?
        </h3>
        <div class="form-btn">
          <button type="submit">Delete</button>
        </div>
      </div>
      `;
      $form.append(htmlString);
    })

    // If request failed, display error in console
    .fail(function(error) {
      if (error.responseJSON.error) {
        console.log('Error: ' + error.responseJSON.error);
      }
    });

  });

});
