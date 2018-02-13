define(
  ['jquery', 'methods', 'categoryDelete'],
  function($, methods, categoryDelete) {

  $(document).ready(function() {

    // Get category name from url
    var categoryName = methods.getCategoryName();

    // Define html elements
    var $form = $('#delete-category-form');
    var $errorAlert = $('#error-alert');

    // Send get request to server
    $.getJSON(`/api/v1/categories?name=${categoryName}&count=1`)

    // If request successful, load form with data
    .done(function(data){
      var category = data.categories[0];
      var categoryId = category.id;
      var public_id = category.user_id;
      var categoryNameCap = methods.toTitleCase(categoryName);

      if (methods.getCookie('public_id') === public_id) {
        var htmlString = `
        <div class="form-group">
          <h3>Are you sure you want to delete
            <span class="highlight">${categoryNameCap}</span>?
          </h3>
          <div class="form-btn">
            <button type="submit">Delete</button>
          </div>
        </div>
        `
        $form.append(htmlString);

        // Send ajax request to server when form is submitted
        categoryDelete(categoryId);

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
