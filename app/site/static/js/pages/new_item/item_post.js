// Load required dependencies
define(["jquery", "submitForm", "setHeaders"],
    /**
     * @description setup file to be used as module
     * @param $ jQuery from jquery module
     * @callback submitForm function from submitForm module
     * @return itemPost function to define itemPost module
     */
    function($, submitForm) {

        const itemPost = function() {

            // Process the form when button is clicked
            $("form").on("submit", (function(event) {

                // Create ajax configuration object
                const ajaxConfig = {
                    type: "POST",
                    url: "/api/v1/items",
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

        // Return itemPost function
        return itemPost;
    }
);
