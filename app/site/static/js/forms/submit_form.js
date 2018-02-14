// Load required dependencies
define(["jquery"],
    /**
    * @description setup file to be used as module
    * @param $ load jquery from requirejs
    * @return submitForm function to define submitForm module
    */
    function($) {

        /**
         * @description send ajax request to server and handle response
         * @param {!ObjType} ajaxConfig object of ajax configuration settings
         */
        const submitForm = function(ajaxConfig) {

            // Send ajax request to server
            $.ajax(ajaxConfig)

            // If request successful, alert user and return to home page
            .done(function(data) {
                // Get success alert from server response
                const alert = data.success;
                // If success alert, display alert message
                if (alert) {
                    console.log("Success: " + alert);
                    $(document).ready(function() {
                        $("#success-alert").text(alert).show();
                        $("#error-alert").hide();
                    });
                    // Wait a second, then return to home page
                    setTimeout(function() {
                        window.location.href = "/";
                    }, 1000);
                }
            })

            // If request failed, alert user
            .fail(function(error) {
                // Get error alert from server response
                const alert = error.responseJSON.error;
                // If error alert, display alert message
                if (alert) {
                    console.log("Error: " + alert);
                    $(document).ready(function() {
                        $("#error-alert").text(alert).show();
                        $("#success-alert").hide();
                        // Wait a second, then hid message
                        setTimeout(function() {
                            $errorAlert.text(alert).hide();
                        }, 3000);
                    });
                }
            });
        };

        // Return submitForm function
        return submitForm;
    }
);
