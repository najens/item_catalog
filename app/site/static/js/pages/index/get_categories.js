// Load required dependencies
define(["jquery", "methods"],
    /**
     * @description get categories and display on page
     * @param $ jQuery from jquery module
     * @param {!ObjType} methods object of methods from methods module
     */
    function($, methods) {

        $(document).ready(function() {

            // Send get request to server
            $.getJSON("/api/v1/categories?sort=name+asc")

            // If request successful, display list of categories
            .done(function(data) {

                const categories = [];
                console.log("Success: Categories were successfully loaded!");

                $.each(data.categories, function(key, val) {

                    const public_id = val.user_id;
                    const category = val.name;
                    const categoryCap = methods.toTitleCase(category);
                    const id = val.id;
                    const htmlId = `category-${id}`
                    const link = val.link;
                    const itemListLength = val.items.length;

                    // If user id matches category user id, display
                    // category, json, edit, and delete links on page
                    if (methods.getCookie("public_id") === public_id) {

                        const htmlString = `
                        <li>
                            <span id='${htmlId}' class='categories'>
                                ${categoryCap}
                            </span>
                            <a class='links json' href='${link}'>JSON</a>
                            <a class='links edit' href=
                                '/${category}/edit'>Edit</a>
                            <a class='links delete' href=
                                '/${category}/delete'>Delete</a>
                        </li>
                        `;

                        // Add html to list
                        categories.push(htmlString);

                    // If user id does not match category user id, only
                    // display cateogry and json links on page
                    } else {
                        var htmlString = `
                        <li>
                            <span id='${htmlId}' class=
                                'categories'>${categoryCap}</span>
                            <a class='links json' href='${link}'>JSON</a>
                        </li>
                        `;

                        // Add html to list
                        categories.push(htmlString);
                    }

                    // For each category displayed add a click function
                    $("#categories").on("click", `#${htmlId}`, function() {

                        // Send get request to server
                        $.getJSON(`/api/v1/items?category=
                              ${category}&sort=name+asc`
                        )

                        // If request successful, display
                        // list of items for that category
                        .done(function(data) {

                            console.log(
                                "Success: Items were successfully loaded!"
                            );
                            const items = [];

                            $.each(data.items, function(key, val) {

                                const public_id = val.user_id;
                                const item = val.name;
                                const itemCap = methods.toTitleCase(item);
                                const id = val.id;
                                const link = val.link;
                                const category = val.category_name;
                                const categoryCap =
                                    methods.toTitleCase(category);
                                const itemString =
                                    `${itemCap} (${categoryCap})`;

                                // If user id matches item user id, display
                                // item, json, edit, and delete links on page
                                if (methods.getCookie("public_id")
                                    === public_id) {

                                    const htmlString = `
                                    <li>
                                        <a class='items' href=
                                            '/${category}/${id}'>
                                            ${itemString}
                                        </a>
                                        <a class='links json' href=
                                            '${link}'>JSON</a>
                                        <a class='links edit' href=
                                            '/${category}/${id}/edit'>
                                            Edit
                                        </a>
                                        <a class='links delete' href=
                                            '/${category}/${id}/delete'>
                                            Delete
                                        </a>
                                    </li>
                                    `;

                                    // Add html to list
                                    items.push(htmlString);

                                // If user id does not match item user id,
                                // only display item and json links on page
                                } else {

                                    const htmlString = `
                                    <li>
                                        <a class='items' href=
                                            '/${category}/${id}'>
                                            ${itemString}
                                        </a>
                                        <a class='links json' href=
                                            '${link}'>JSON</a>
                                    </li>
                                    `;

                                    // Add html to list
                                    items.push(htmlString);
                                }
                            });

                            // Insert html onto page
                            $("#item-heading".empty();
                            $("#item-json").show();
                            $("#item-heading".append(
                                `${categoryCap} Items (${itemListLength})`
                            );
                            $("#items").empty();
                            $("#items").append(items);
                        })

                        // If request failed, display error on page
                        .fail(function(error) {
                            if (error.responseJSON.error) {
                                console.log(
                                    `Error: ${error.responseJSON.error}`
                                );
                                $("#item-heading".empty();
                                $("#item-json").hide();
                                $("#item-heading".append(
                                    `${categoryCap} Items (${itemListLength})`
                                );
                                $("#items").empty();
                                $("#items").append(error.responseJSON.error);
                            }
                        });
                    });
                });

                // Insert html onto page
                $("#categories").empty();
                $("#categories").append(categories);
            })

            // If request failed, display error
            .fail(function(error) {
                if (error.responseJSON.error) {
                    console.log(`Error: ${error.responseJSON.error}`);
                    $("#categories").append(error.responseJSON.error);
                }
            });
        });
    }
);
