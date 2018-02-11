define(['jquery', 'methods'], function($, methods) {

  // Set headers before each ajax request
  $.ajaxSetup({
      beforeSend: function(xhr) {
        // Set CSRF token header
        xhr.setRequestHeader(
          'X-CSRF-Token', methods.getCookie('csrf_access_token')
        );
      }
  });

});
