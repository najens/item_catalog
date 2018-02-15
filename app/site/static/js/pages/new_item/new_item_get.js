// Load required dependencies
define(["jquery", "methods", "itemPost"],
    /**
     * @description post new item when form is submitted
     * @param $ jQuery from jquery module
     * @param {!ObjType} methods object of methods from methods module
     * @callback itemPost function from itemPost module that posts item
     */
    function($, methods, itemPost) {

        $(document).ready(function() {

            // Send get request to server
            $.getJSON('/api/v1/categories?sort=name+asc')

            // If request successful, add category options to form
            .done(function(data) {

                var categories = [];

                $.each(data.categories, function(key, val) {

                    const htmlString = `
                    <option value="${val.name}">
                        ${methods.toTitleCase(val.name)}
                    </option>
                    `;

                    // Add html to list
                    categories.push(htmlString);
                });

                const htmlString = `
                <div class="form-group">
                    <h3>New Item</h3>
                    <div class="flex-col left">
                        <h4>
                            <label for="name">Name:</label>
                        </h4>
                        <input id="name-field" type="text" size=
                            "26" maxlength="100" name=
                            "name" autofocus required>
                        <h4>
                            <label for="description">Description:</label>
                        </h4>
                        <textarea id="description-field" name=
                            "description" rows="5" cols="30" maxlength=
                            "200" required></textarea>
                        <h4>
                            <label for="category">Category:</label>
                        </h4>
                        <select id="category-field" name="category">
                            ${categories}
                        </select>
                    </div>
                    <div class="form-btn">
                        <button type="submit">Submit</button>
                    </div>
                </div>
                `;

                // Insert html onto page
                $("#new-item-form").append(htmlString);

                // Send ajax request to server when form is submitted
                itemPost();
            })

            // If request failed, display error in console and on page
            .fail(function(error) {
                if (error.responseJSON.error) {
                    
                    console.log(`Error: ${error.responseJSON.error}`);
                    const alert = "Please add category before adding item!";

                    $(document).ready(function() {
                        $("#error-alert").text(alert).show();
                        $("#success-alert").hide();
                        // Wait a second, then hide message and return home
                        setTimeout(function() {
                            $("#error-alert").text(alert).hide();
                            window.location.href = "/";
                        }, 2000);
                    });
                }
            });
        });
    }
);
