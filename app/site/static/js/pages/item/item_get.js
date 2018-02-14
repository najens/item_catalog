// Load required dependencies
define(["jquery", "methods"],
    /**
     * @description get item and display on page
     * @param $ jQuery from jquery module
     * @param {!ObjType} methods object of methods from methods module
     */
    function($, methods) {

        $(document).ready(function() {

            // Get item id from url
            const itemId = ${methods.getItemId()};

            // Send get request to server
            $.getJSON(`/api/v1/items/${itemId}`)

            // If request succesful, insert data into html container
            .done(function(data){

                let itemName = data.item.name;
                itemName = methods.toTitleCase(itemName);
                const itemDescription = data.item.description;
                const htmlString = `
                <div class="left item-info">
                    <h3>${itemName}</h3>
                    <p>Description: ${itemDescription}</p>
                </div>
                `;

                // Insert html onto page
                $("#item-container").append(htmlString);
            })

            // If request failed, display error in console
            .fail(function(error) {
                if (error.responseJSON.error) {
                    console.log(`Error: ${error.responseJSON.error}`);
                }
            });
        });
    }
);
