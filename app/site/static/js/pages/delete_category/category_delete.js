// Load required dependencies
define(["jquery", "submitForm", "setHeaders"],
    /**
     * @description setup file to be used as module
     * @param $ jQuery from jquery module
     * @callback submitForm function from submitForm module
     * @return categoryDelete function to define categoryDelete module
     */
    function($, submitForm) {

        /**
         * @description send ajax request to delete category
         * @param {string} categoryId id of category
         */
        const categoryDelete = function(categoryId) {

            // Process the form when button is clicked
            $("form").on("submit", (function(event) {

                // Create ajax configuration object
                const ajaxConfig = {
                    type: "DELETE",
                    url: `/api/v1/categories/${categoryId}`,
                    datatype: "json"
                };

                // Send ajax request to server
                submitForm(ajaxConfig);

                // Override default form functionality
                event.preventDefault();
            }));
        };

        // Return categoryDelete function
        return categoryDelete;
    }
);
