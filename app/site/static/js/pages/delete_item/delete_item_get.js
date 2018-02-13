define(['jquery', 'methods', 'itemDelete'], function($, methods, itemDelete) {

  $(document).ready(function() {

    // Get item Id from url
    var itemId = methods.getItemId();

    // Define html elements
    var $form = $('#delete-item-form');
    var $errorAlert = $('#error-alert');

    // Send get request to server
    $.getJSON(`/api/v1/items/${itemId}`)

    // If request successful, load form with delete prompt
    .done(function(data){
      var itemId = data.item.id;
      var itemName = data.item.name;
      var itemNameCap = methods.toTitleCase(itemName);
      var public_id = data.item.user_id;

      if (methods.getCookie('public_id') === public_id) {

        var htmlString = `
        <div class="form-group">
          <h3>
            Are you sure you want to delete
            <span>${itemNameCap}</span>?
          </h3>
          <div class="form-btn">
            <button type="submit">Delete</button>
          </div>
        </div>
        `;

        $form.append(htmlString);

        itemDelete(itemId);

      } else {
        var alert = 'You are not authorized to view this page!'
        $errorAlert.text(alert).show();
      }

    })

    // If request failed, display error in console
    .fail(function(error) {
      if (error.responseJSON.error) {
        console.log('Error: ' + error.responseJSON.error);
      }
    });

  });

});