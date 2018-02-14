// Load required dependencies
define(["jquery", "methods"],
    /**
     * @description set header before each ajax request
     * @param $ jQuery from jquery module
     * @param {!ObjType} methods object of methods from methods module
     */
    function($, methods) {

        // Configure default ajax parameters
        $.ajaxSetup({
              // Set headers before http request
              beforeSend: function(xhr) {
                  // Set CSRF token header
                  xhr.setRequestHeader(
                      "X-CSRF-Token", methods.getCookie("csrf_access_token")
                  );
              }
        });
    }
);
