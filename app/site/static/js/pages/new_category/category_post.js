// Load required dependencies
define(["jquery", "submitForm", "setHeaders"],
    /**
     * @description post new category
     * @param $ jQuery from jquery module
     * @callback submitForm function from submitForm module
     */
    function($, submitForm) {

        $(document).ready(function() {

            // Process the form when button is clicked
            $('form').on('submit', (function(event) {

                // Create ajax configuration object
                var ajaxConfig = {
                    type: "POST",
                    url: "/api/v1/categories",
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
        });
    }
);
