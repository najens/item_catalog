// Load required dependencies
define(["jquery", "submitForm", "setHeaders"],
    /**
     * @description setup file to be used as module
     * @param $ jQuery from jquery module
     * @callback submitForm function from submitForm module
     * @return categoryPut function to define categoryPut module
     */
    function($, submitForm) {

        /**
         * @description send ajax request to edit category
         * @param {string} categoryId id of category
         */
        const categoryPut = function(categoryId) {

            // Process the form when button is clicked
            $("form").on("submit", (function(event) {

                // Create ajax configuration object
                var ajaxConfig = {
                    type: "PUT",
                    url: `/api/v1/categories/${categoryId}`,
                    datatype: "json",
                    data: {
                        name: $("#name-field").val().toLowerCase()
                    }
                };

                // Send ajax request to server
                submitForm(ajaxConfig);

                // Override default form functionality
                event.preventDefault();
            }));
        };

        // Return categoryPut function
        return categoryPut;
    }
);
