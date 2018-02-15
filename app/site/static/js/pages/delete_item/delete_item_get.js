// Load required dependencies
define(["jquery", "methods", "itemDelete"],
    /**
     * @description get item and delete it when form is submitted
     * @param $ jQuery from jquery module
     * @param {!ObjType} methods object of methods from methods module
     * @callback itemDelete function that deletes item
     */
    function($, methods, itemDelete) {

        $(document).ready(function() {

            // Get item Id from url
            const itemId = methods.getItemId();

            // Send get request to server
            $.getJSON(`/api/v1/items/${itemId}`)

            // If request successful, load form with delete prompt
            .done(function(data){

                const public_id = data.item.user_id;

                // If user id matches item user id, display form
                if (methods.getCookie("public_id") === public_id) {

                    const itemId = data.item.id;
                    let itemName = data.item.name;
                    itemName = methods.toTitleCase(itemName);
                    const htmlString = `
                    <div class="form-group">
                        <h3>
                            Are you sure you want to delete
                            <span>${itemName}</span>?
                        </h3>
                        <div class="form-btn">
                            <button type="submit">Delete</button>
                        </div>
                    </div>
                    `;

                    // Insert html onto page
                    $("#delete-item-form").append(htmlString);

                    // Send ajax request to server when form is submitted
                    itemDelete(itemId);

                // If user id does not match category user id, display error
                } else {

                    const alert = "You are not authorized to view this page!"

                    // Display error alert on page
                    $("#error-alert").text(alert).show();
                }
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
