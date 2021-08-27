$(document).ready(function() {
    $('a#add_user_field').click(function() {
        var lastField = $("#form_build_collection div:last");
        var intId = (lastField && lastField.length && lastField.data("idx") + 1) || 1;
        var add_user_field = $("<div class=\"add_user_field\" id=\"field" + intId + "\"/>");
        add_user_field.data("idx", intId);
        var fName = $("<input type=\"text\" class=\"add_user_input\" name=\"add_user\" placeholder=\"Additional Username\" />");
        var removeButton = $("<a class=\"button reverse-color\"><i class=\"fas fa-user-minus\"></i></a>");
        removeButton.click(function() {
            $(this).parent().remove();
        });
        add_user_field.append(fName);
        add_user_field.append(removeButton);
        $("#form_build_collection").append(add_user_field);
    });

    $('#reset_fields').click(function() {
        $('.add_user_field').each(function() {
            $(this).remove();
        });
    });
});

function send_user_form() {
    var form = document.getElementById("form_build_collection")
    form.action = "bgg\\" + document.getElementById("main_user").value;
    $('input.add_user_input').each(function( index ) {
    if (this.value == "") {
        this.remove();
    }
    });
    document.getElementById("form_build_collection").submit();
}
