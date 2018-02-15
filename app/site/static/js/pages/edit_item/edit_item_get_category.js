// Load required dependencies
define(["jquery", "methods"],
    /**
     * @description setup file to be used as requirejs module
     * @param $ jQuery from jquery module
     * @param {!ObjType} methods object of methods from methods module
     * @return getCategory function to define getCategory module
     */
    function($, methods) {

        /**
         * @description send ajax request to get category
         * @param {string} categoryName name of category
         */
        const getCategory = function(categoryName) {

            // Send get request to server
            $.getJSON("/api/v1/categories?sort=name+asc")

            // If request successful, load form with data
            .done(function(data) {

                var categories = [];

                // Create html option for each category and append to list
                $.each(data.categories, function(key, val) {

                    var category = val.name
                    var categoryCap = methods.toTitleCase(category)

                    // If category matches current category, select it
                    if (category == categoryName) {

                        const htmlString = `
                        <option selected value="${category}">
                            ${categoryCap}
                        </option>
                        `;

                        // Add html to list
                        categories.push(htmlString);

                    } else {
                        const htmlString = `
                        <option value="${category}">
                            ${categoryCap}
                        </option>
                        `;

                        // Add html to list
                        categories.push(htmlString);
                    }
                });

                // Insert html onto page
                $("#category-field").append(categories);
            })

            // If request failed, display error in console
            .fail(function(error) {
                if (error.responseJSON.error) {
                    console.log(`Error: ${error.responseJSON.error}`);
                }
            });
        };

        // Return getCategory function
        return getCategory;
    }
);
