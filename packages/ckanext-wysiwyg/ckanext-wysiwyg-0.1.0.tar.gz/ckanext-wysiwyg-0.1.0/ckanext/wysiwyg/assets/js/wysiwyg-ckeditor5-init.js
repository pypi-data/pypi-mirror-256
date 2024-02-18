this.ckan.module('wysiwyg-ckeditor5-init', function ($) {
    return {
        options: {},
        initialize: function () {
            $.proxyAll(this, /_/);

            this._initEditor();
        },
        _initEditor: function () {
            ClassicEditor.create(this.el[0], {
                extraPlugins: ["SimpleUploadAdapter", "GeneralHtmlSupport", "ImageInsert"],
                simpleUpload: {
                    uploadUrl: ckan.url('/wysiwyg/upload_file'),
                },
                mediaEmbed: { previewsInData: true },
                htmlSupport: {
                    allow: [
                        {
                            name: "/^(div|p|h[2-4])$/'",
                        }
                    ]
                }
            });
        }
    };
});
