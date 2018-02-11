define(['jquery', 'methods'], function($, methods) {

  $(document).ready(function() {

    // Define html elements
    var $items = $('#items');

    // Send get requet to server
    $.getJSON('/api/v1/items?sort=id+desc&count=10')

    // If request successful, display list of items
    .done(function(data) {

      var items = [];
      console.log('Success: Items were succesfully loaded!');

      $.each(data.items, function(key, val) {

        var item = val.name;
        var category = val.category_name;
        var id = val.id;
        var link = val.link;
        var itemCap = methods.toTitleCase(item);
        var categoryCap = methods.toTitleCase(category);
        var itemString = `${itemCap} (${categoryCap})`

        if (methods.getCookie('public_id') === val.user_id ) {
          var htmlString = `
            <li>
              <a class='items' href='/${category}/${id}'>${itemString}</a>
              <a class='links json' href='${link}'>JSON</a>
              <a class='links edit' href='/${category}/${id}/edit'>Edit</a>
              <a class='links delete' href='/${category}/${id}/delete'>
                Delete
              </a>
            </li>
          `;
          items.push(htmlString);
        } else {
            var htmlString = `
              <li>
                <a class='items' href='/${category}/${id}'>${itemString}</a>
                <a class='links json' href='${link}'>JSON</a>
              </li>
            `;
          items.push(htmlString);
        }
      });

      $items.append(items);

    })

    // If request failed, display error
    .fail(function(error) {
      if (error.responseJSON.error) {
        console.log('Error: ' + error.responseJSON.error);
        $items.empty();
        $items.append(error.responseJSON.error);
      }
    });

  });

});
