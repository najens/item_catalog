// Load required dependencies
define(["jquery", "methods", "categoryPut"],
    /**
     * @description get category and update it when form is submitted
     * @param $ jQuery from jquery module
     * @param {!ObjType} methods object of methods from methods module
     * @callback categoryPut function that updates category
     */
    function($, methods, categoryPut) {

        $(document).ready(function() {

            // Get category name from url
            const categoryName = methods.getCategoryName();

            // Send get request to server
            $.getJSON(`/api/v1/categories?name=${categoryName}&count=1`)

            // If request successful, load form with data
            .done(function(data){

                const public_id = data.categories[0].user_id;

                // If user id matches category user id, display form
                if (methods.getCookie("public_id") === public_id) {

                    const categoryId = data.categories[0].id;
                    let categoryName = data.categories[0].name;
                    categoryName = methods.toTitleCase(categoryName);
                    const htmlString = `
                    <div class="form-group">
                        <h3>Edit Category</h3>
                        <div class="flex-col left">
                            <h4>
                                <label for="name">Name:</label>
                            </h4>
                            <input id="name-field" type="text" maxlength="100"
                                value="${categoryName}" autofocus required>
                        </div>
                        <div class="form-btn">
                            <button type="submit">Submit</button>
                        </div>
                    </div>
                    `;

                    // Insert html onto page
                    $("#edit-category-form").append(htmlString);

                    // Send ajax request to server when form is submitted
                    categoryPut(categoryId);

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
