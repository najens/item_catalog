// Load required dependencies
define(["jquery", "submitForm", "setHeaders"],
    /**
     * @description setup file to be used as module
     * @param $ jQuery from jquery module
     * @callback submitForm function from submitForm module
     * @return itemDelete function to define itemDelete module
     */
    function($, submitForm) {

        /**
         * @description send ajax request to delete item
         * @param {string} itemId id of item
         */
        const itemDelete = function(itemId) {

            // Process the form when button is clicked
            $("form").on("submit", (function(event) {

                // Create ajax configuration object
                const ajaxConfig = {
                    type: "DELETE",
                    url: `/api/v1/items/${itemId}`,
                    datatype: "json"
                };

                // Send ajax request to server
                submitForm(ajaxConfig);

                // Override default form functionality
                event.preventDefault();
            }));
        };

        // Return itemDelete function
        return itemDelete;
    }
);
