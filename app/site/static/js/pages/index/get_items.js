// Load required dependencies
define(["jquery", "methods"],
    /**
     * @description get items and display on page
     * @param $ jQuery from jquery module
     * @param {!ObjType} methods object of methods from methods module
     */
    function($, methods) {

        $(document).ready(function() {

            // Send get requet to server
            $.getJSON("/api/v1/items?sort=id+desc&count=10")

            // If request successful, display list of items
            .done(function(data) {

                const items = [];
                console.log("Success: Items were succesfully loaded!");

                $.each(data.items, function(key, val) {

                    const public_id = val.user_id;
                    let item = val.name;
                    item = methods.toTitleCase(item);
                    const category = val.category_name;
                    const categoryCap = methods.toTitleCase(category);
                    const id = val.id;
                    const link = val.link;
                    const itemString = `${item} (${categoryCap})`

                    // If user id matches item user id, display
                    // item, json, edit, and delete links on page
                    if (methods.getCookie('public_id') === public_id ) {

                        const htmlString = `
                        <li>
                            <a class='items' href=
                                '/${category}/${id}'>${itemString}</a>
                            <a class='links json' href='${link}'>JSON</a>
                            <a class='links edit' href=
                                '/${category}/${id}/edit'>Edit</a>
                            <a class='links delete' href=
                                '/${category}/${id}/delete'>Delete</a>
                        </li>
                        `;

                        // Add html to list
                        items.push(htmlString);

                    // If user id does not match item user id, only
                    // display item and json links on page
                    } else {
                        const htmlString = `
                        <li>
                            <a class='items' href=
                                '/${category}/${id}'>${itemString}</a>
                            <a class='links json' href='${link}'>JSON</a>
                        </li>
                        `;

                        // Add html to list
                        items.push(htmlString);
                    }
                });

                // Insert html onto page
                $("#items").append(items);
            })

            // If request failed, display error
            .fail(function(error) {
                if (error.responseJSON.error) {
                    console.log(`Error: ${error.responseJSON.error}`);
                    $("#items").empty();
                    $("#items").append(error.responseJSON.error);
                }
            });
        });
    }
);
