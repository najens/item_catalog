define(['jquery', 'methods'], function($, methods) {

  const getCategory = function(categoryName) {

    // Send get request to server
    $.getJSON('/api/v1/categories?sort=name+asc')

    // If request successful, load form with data
    .done(function(data) {
      // Define html elements
      var $categoryField = $('#category-field');
      var categories = [];
      $.each(data.categories, function(key, val) {

        var category = val.name
        var categoryCap = methods.toTitleCase(category)

        if (val.name == categoryName) {
          var htmlString = `
          <option selected value="${category}">
            ${categoryCap}
          </option>
          `;
        } else {
          var htmlString = `
          <option value="${category}">
            ${categoryCap}
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

  };

  return getCategory;

});
