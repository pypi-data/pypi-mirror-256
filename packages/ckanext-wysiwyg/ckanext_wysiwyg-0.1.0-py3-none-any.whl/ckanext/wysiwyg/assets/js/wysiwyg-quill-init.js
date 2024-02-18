this.ckan.module('wysiwyg-quill-init', function ($) {
    return {
        options: {
            inputId: null,
            forDisplay: false
        },
        initialize: function () {
            $.proxyAll(this, /_/);

            this.container = $(".form-group-quill");
            this.inputEl = document.getElementById(this.options.inputId);
            this.form = this.el.closest("form");

            this._initEditor();

            this.form.on("submit", (e) => {
                this.inputEl.value = JSON.stringify(window.quill.getContents());
            })

            $(".form-label-quill").click(() => {
                window.quill.focus()
            })

            window.quill.root.addEventListener("focus", () => {
                this.container.addClass("focused");
            });
            window.quill.root.addEventListener("blur", () => {
                this.container.removeClass("focused");
            });
        },
        _initEditor: function () {
            let config = {
                theme: 'snow',
                modules: {
                    toolbar: [
                        [{ header: [1, 2, false] }, { size: ['small', false, 'large', 'huge'] }],
                        [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                        ['bold', 'italic', 'underline', 'strike'],
                        ['image', 'link', 'video', 'code-block'],
                        ['clean']
                    ]
                }
            }

            if (this.options.forDisplay) {
                config = { readOnly: true };
            }

            window.quill = new Quill(this.el[0], config);

            if (this.inputEl.value && this.inputEl.value.trim()) {
                window.quill.setContents(JSON.parse(this.inputEl.value));
            }
        },
    };
});
