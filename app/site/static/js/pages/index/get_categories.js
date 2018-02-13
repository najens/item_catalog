define(['jquery', 'methods'], function($, methods) {

  $(document).ready(function() {

    // Define html elements
    var $categories = $('#categories');
    var $items = $('#items');
    var $itemHeading = $('#item-heading')
    var $itemJSON = $('#item-json')

    // Send get request to server
    $.getJSON('/api/v1/categories?sort=name+asc')

    // If request successful, display categories
    .done(function(data) {
      var categories = [];
      console.log('Success: Categories were successfully loaded!');
      $.each(data.categories, function(key, val) {

        var public_id = val.user_id;
        var category = val.name;
        var categoryCap = methods.toTitleCase(category);
        var id = val.id;
        var htmlId = `category-${id}`
        var link = val.link;
        var itemListLength = val.items.length;

        // If user is logged in, display category edit and delete buttons
        if (methods.getCookie('public_id') === public_id) {
          var htmlString = `
            <li>
              <span id='${htmlId}' class='categories'>
                ${categoryCap}
              </span>
              <a class='links json' href='${link}'>JSON</a>
              <a class='links edit' href='/${category}/edit'>
                Edit
              </a>
              <a class='links delete' href='/${category}/delete'>
                Delete
              </a>
            </li>
          `;
          categories.push(htmlString);
        } else {
          var htmlString = `
            <li>
              <span id='${htmlId}' class='categories'>
                ${categoryCap}
              </span>
              <a class='links json' href='${link}'>JSON</a>
            </li>
          `;
          categories.push(htmlString);
        }

        // For each category displayed add a click function
        $categories.on("click", `#${htmlId}`, function() {

          // Send get request to server
          $.getJSON(`/api/v1/items?category=${category}&sort=name+asc`)

          // If request successful, display items for that category
          .done(function(data) {
            console.log('Success: Items were successfully loaded!');
            console.log(data);
            var items = [];
            $.each(data.items, function(key, val) {
              var public_id = val.user_id;
              var item = val.name;
              var itemCap = methods.toTitleCase(item);
              var id = val.id;
              var link = val.link;
              var category = val.category_name;
              var categoryCap = methods.toTitleCase(category);
              var itemString = `${itemCap} (${categoryCap})`;

              // If user is loggedin, display item edit and delete buttons
              if (methods.getCookie('public_id') === public_id) {
                var htmlString = `
                  <li>
                    <a class='items' href='/${category}/${id}'>
                      ${itemString}
                    </a>
                    <a class='links json' href='${link}'>JSON</a>
                    <a class='links edit' href='/${category}/${id}/edit'>
                      Edit
                    </a>
                    <a class='links delete' href='/${category}/${id}/delete'>
                      Delete
                    </a>
                  </li>
                `;
                items.push(htmlString);
              } else {
                  var htmlString = `
                    <li>
                      <a class='items' href='/${category}/${id}'>
                        ${itemString}
                      </a>
                      <a class='links json' href='${link}'>JSON</a>
                    </li>
                  `;
                items.push(htmlString);
              }
            });
            $itemHeading.empty();
            $itemJSON.show();
            $itemHeading.append(`${categoryCap} Items (${itemListLength})`);
            $items.empty();
            $items.append(items);
          })

          // If request failed, display error
          .fail(function(error) {
            if (error.responseJSON.error) {
              console.log('Error: ' + error.responseJSON.error);
              $itemHeading.empty();
              $itemJSON.hide();
              $itemHeading.append(`${categoryCap} Items (${itemListLength})`);
              $items.empty();
              $items.append(error.responseJSON.error);
            }
          });
        });
      });
      $categories.empty();
      $categories.append(categories);
    })

    // If request failed, display error
    .fail(function(error) {
      if (error.responseJSON.error) {
        console.log('Error: ' + error.responseJSON.error);
        $categories.append(error.responseJSON.error);
      }
    });

  });

});
