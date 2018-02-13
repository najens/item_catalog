define(['jquery', 'methods', 'itemPut', 'editItemGetCategory'], function($, methods, itemPut, getCategory) {

  $(document).ready(function() {

    // Get item Id from url
    var itemId = methods.getItemId();

    // Define html elements
    var $form = $('#edit-item-form');
    var $errorAlert = $('#error-alert');

    // Send get request to server
    $.getJSON(`/api/v1/items/${itemId}`)

    // If request successful, load form with data
    .done(function(data){
      
      var itemId = data.item.id;
      var itemName = data.item.name;
      var itemNameCap = methods.toTitleCase(itemName);
      var itemDescription = data.item.description;
      var categoryName = data.item.category_name;
      var public_id = data.item.user_id;

      if (methods.getCookie('public_id') === public_id) {
        var htmlString = `
        <div class="form-group">
            <h3>Edit Item</h3>
            <div class="flex-col left">
                <h4>
                    <label for="name">Name:</label>
                </h4>
                <input id="name-field" type="text" size="26" maxlength="100"
                    name="name" value="${itemNameCap}" autofocus required>
                <h4>
                    <label for="description">Description:</label>
                </h4>
                <textarea id="description-field" name="description"
                    rows="5" cols="30" maxlength="200"
                    required>${itemDescription}</textarea>
                <h4>
                    <label for="category">Category:</label>
                </h4>
                <select id="category-field" name="category"></select>
            </div>
            <div class="form-btn">
                <button type="submit">Submit</button>
            </div>
        </div>
        `

        $form.append(htmlString);

        //Send ajax request to server
        getCategory(categoryName);

        // Send ajax request to server when form is submitted
        itemPut(itemId);

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
