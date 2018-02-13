requirejs.config({
    baseUrl: 'http://localhost:5000/app/site/static/js',
    paths: {
        // the left side is the module ID,
        // the right side is the path to
        // the jQuery file, relative to baseUrl.
        // Also, the path should NOT include
        // the '.js' file extension. This example
        // is using jQuery 1.9.0 located at
        // js/lib/jquery-1.9.0.js, relative to
        // the HTML page.
        jquery: [
          'https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min',
          // If the CDN location fails, load from this location
          'lib/jquery-3.3.1.min'
        ],
        methods: 'methods/methods',
        formAlerts: 'forms/form_alerts',
        submitForm: 'forms/submit_form',
        setHeaders: 'headers/set_headers',
        categoryPut: 'pages/edit_category/category_put',
        categoryDelete: 'pages/delete_category/category_delete',
        itemPost: 'pages/new_item/item_post',
        itemDelete: 'pages/delete_item/item_delete',
        itemPut: 'pages/edit_item/item_put',
        editItemGetCategory: 'pages/edit_item/edit_item_get_category'
    }
});
