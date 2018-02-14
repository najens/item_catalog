// Load required dependencies
define(["jquery", "submitForm", "setHeaders"],
    /**
     * @description setup file to be used as module
     * @param $ jQuery from jquery module
     * @callback submitForm function from submitForm module
     * @return itemPut function to define itemPut module
     */
    function($, submitForm) {

        /**
         * @description send ajax request to edit item
         * @param {string} itemId id of item
         */
        const itemPut = function(itemId) {

            // Process the form when button is clicked
            $("form").on("submit", (function(event) {

                // Create ajax configuration object
                var ajaxConfig = {
                    type: "PUT",
                    url: `/api/v1/items/${itemId}`,
                    datatype: "json",
                    data: {
                        name: $("#name-field").val().toLowerCase(),
                        description: $("#description-field").val(),
                        category: $("#category-field").val().toLowerCase()
                    }
                };

                // Send ajax request to server
                submitForm(ajaxConfig);

                // Override default form functionality
                event.preventDefault();
            }));
        };

        // Return itemPut function
        return itemPut;
    }
);
