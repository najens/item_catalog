// Load required dependencies
define(["jquery", "methods", "itemPut", "editItemGetCategory"],
    /**
     * @description get item and update it when form is submitted
     * @param $ jQuery from jquery module
     * @param {!ObjType} methods object of methods from methods module
     * @callback itemPut function from itemPut module that updates item
     * @callback getCategory function that gets and inserts array of
     *                       categories into form from editItemGetCategory
     *                       module
     */
    function($, methods, itemPut, getCategory) {

        $(document).ready(function() {

            // Get item Id from url
            var itemId = methods.getItemId();

            // Send get request to server
            $.getJSON(`/api/v1/items/${itemId}`)

            // If request successful, load form with data
            .done(function(data){

                const public_id = data.item.user_id;

                // If user id matches item user id, display form
                if (methods.getCookie("public_id") === public_id) {

                    const itemId = data.item.id;
                    let itemName = data.item.name;
                    itemName = methods.toTitleCase(itemName);
                    const itemDescription = data.item.description;
                    const categoryName = data.item.category_name;
                    const htmlString = `
                    <div class="form-group">
                        <h3>Edit Item</h3>
                        <div class="flex-col left">
                            <h4>
                                <label for="name">Name:</label>
                            </h4>
                            <input id="name-field" type="text" size=
                                "26" maxlength="100" name="name" value=
                                "${itemName}" autofocus required>
                            <h4>
                                <label for="description">Description:</label>
                            </h4>
                            <textarea id="description-field" name=
                                "description" rows="5" cols="30" maxlength=
                                "200" required>${itemDescription}</textarea>
                            <h4>
                                <label for="category">Category:</label>
                            </h4>
                            <select id="category-field" name="category">
                            </select>
                        </div>
                        <div class="form-btn">
                            <button type="submit">Submit</button>
                        </div>
                    </div>
                    `;

                    // Insert html onto page
                    $("#edit-item-form").append(htmlString);

                    // Send ajax request to server when form is submitted
                    getCategory(categoryName);

                    // Send ajax request to server when form is submitted
                    itemPut(itemId);

                // If user id does not match item user id, display error
                } else {

                    var alert = "You are not authorized to view this page!";

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
