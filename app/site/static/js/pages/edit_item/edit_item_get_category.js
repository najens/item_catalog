define(['jquery', 'methods'], function($, methods) {

  $(document).ready(function() {

    // Define html elements
    var $categoryField = $('#category-field');

    // Send get request to server
    $.getJSON('/api/v1/categories?sort=name+asc')

    // If request successful, load form with data
    .done(function(data) {
      var categories = [];
      $.each(data.categories, function(key, val) {
        if (val.name == methods.getCategoryName()) {
          var htmlString = `
          <option selected value="${val.name}">
            ${methods.toTitleCase(val.name)}
          </option>
          `;
        } else {
          var htmlString = `
          <option value="${val.name}">
            ${methods.toTitleCase(val.name)}
          </option>
          `;
        }
        categories.push(htmlString);
      });
      $categoryField.append(categories);
    })

    // If request failed, display error in console
    .fail(function(error) {
      if (error.responseJSON.error) {
        console.log('Error: ' + error.responseJSON.error);
      }
    });

  });
});
