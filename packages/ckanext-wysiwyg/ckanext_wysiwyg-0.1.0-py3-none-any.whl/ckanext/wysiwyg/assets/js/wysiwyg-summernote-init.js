this.ckan.module('wysiwyg-summernote-init', function ($) {
    return {
        options: {},
        initialize: function () {
            $.proxyAll(this, /_/);

            this._initEditor();
        },
        _initEditor: function () {
            this.el.summernote({
                minHeight: 300,
                callbacks: {
                    onImageUpload: (file) => {
                        this.onImageUpload(file[0]);
                    },
                },
            });
        },
        onImageUpload: function (file) {
            let self = this;
            let data = new FormData();
            data.append("upload", file);

            $.ajax({
                data: data,
                type: "POST",
                url: ckan.url('/wysiwyg/upload_file'), //Your own back-end uploader
                cache: false,
                contentType: false,
                processData: false,
                success: function (response) {
                    if (response.error) {
                        return self.sandbox.publish("ap:notify", response.error.message, "error");
                    }

                    if (!response.url) {
                        return;
                    }

                    self.el.summernote('editor.insertImage', response.url);
                }
            });
        }
    };
});
