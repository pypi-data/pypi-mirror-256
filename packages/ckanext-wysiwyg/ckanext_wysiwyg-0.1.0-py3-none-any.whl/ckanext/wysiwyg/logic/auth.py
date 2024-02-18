import ckan.types as types


def wysiwyg_file_upload(
    context: types.Context, data_dict: types.DataDict
) -> types.AuthResult:
    return {"success": True}


def wysiwyg_file_get(
    context: types.Context, data_dict: types.DataDict
) -> types.AuthResult:
    return {"success": True}
