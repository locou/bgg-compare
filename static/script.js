function filterGlobal () {
    $('#collection_table').DataTable().search($('#global_filter').val()).draw();
}

function lessThanRegex(val, max) {
    var arr = []
    for(i=parseFloat(val); i<=parseFloat(max); i++) {
        arr.push(i);
    }
    return "^("+arr.join("|")+")$";
}

function filterColumn (i, val) {
    var regex = false;
    var smart = true;
    $('#collection_table').DataTable().column(i).search(val,regex,smart).draw();
}

function filterColumnRange (i, val, max) {
    var regex = true;
    var smart = false;
    val = lessThanRegex(val, max);
    $('#collection_table').DataTable().column(i).search(val,regex,smart).draw();
}

function orderColumn(i, direction) {
    $('#collection_table').DataTable().order([i, direction]).draw();
}

$(document).ready(function() {
    jQuery.extend( jQuery.fn.dataTableExt.oSort, {
        "non-empty-string-asc": function (str1, str2) {
            if (!isNaN(parseFloat(str1))) {
                str1 = parseFloat(str1);
            }
            if (!isNaN(parseFloat(str2))) {
                str2 = parseFloat(str2);
            }
            if(str1 == "" || str1 == "None")
                return 1;
            if(str2 == "" || str2 == "None")
                return -1;
            return ((str1 < str2) ? -1 : ((str1 > str2) ? 1 : 0));
        },

        "non-empty-string-desc": function (str1, str2) {
            if (!isNaN(parseFloat(str1))) {
                str1 = parseFloat(str1);
            }
            if (!isNaN(parseFloat(str2))) {
                str2 = parseFloat(str2);
            }
            if(str1 == "" || str1 == "None")
                return 1;
            if(str2 == "" || str2 == "None")
                return -1;
            return ((str1 < str2) ? 1 : ((str1 > str2) ? -1 : 0));
        }
    } );
    $('input.global_filter').on( 'keyup click', function () {
        filterGlobal();
    });

    $('input.column_filter').on( 'keyup click', function () {
        filterColumn($(this).data('column'), $(this).val());
    });

    var collection_table = $("#collection_table").DataTable({
        "dom": '<"container"il>pr<"game_container"t>p',
        "lengthMenu": [ 25, 50, 100, 500 ],
        "order": [[ 18, 'desc' ]],
        columnDefs: [
           {type: 'non-empty-string', targets: 0},
           {type: 'non-empty-string', targets: 1},
           {type: 'non-empty-string', targets: 2},
           {type: 'non-empty-string', targets: 3},
           {type: 'non-empty-string', targets: 4},
           {type: 'non-empty-string', targets: 5},
           {type: 'non-empty-string', targets: 6},
           {type: 'non-empty-string', targets: 7},
           {type: 'non-empty-string', targets: 8},
           {type: 'non-empty-string', targets: 9},
           {type: 'non-empty-string', targets: 10},
           {type: 'non-empty-string', targets: 11},
           {type: 'non-empty-string', targets: 12},
           {type: 'non-empty-string', targets: 13},
           {type: 'non-empty-string', targets: 14},
           {type: 'non-empty-string', targets: 15},
           {type: 'non-empty-string', targets: 16},
           {type: 'non-empty-string', targets: 17},
           {type: 'non-empty-string', targets: 18},
           {type: 'non-empty-string', targets: 19},
           {type: 'non-empty-string', targets: 20},
           {type: 'non-empty-string', targets: 21},
           {type: 'non-empty-string', targets: 22},
           {type: 'non-empty-string', targets: 23},
           {type: 'non-empty-string', targets: 24},
           {type: 'non-empty-string', targets: 25},
           {type: 'non-empty-string', targets: 26},
           {type: 'non-empty-string', targets: 27},
           {type: 'non-empty-string', targets: 28},
           {type: 'non-empty-string', targets: 29},
           {type: 'non-empty-string', targets: 30},
           {type: 'non-empty-string', targets: 31},
           {type: 'non-empty-string', targets: 32},
        ]
    });
    $(window).scroll(function() {
        if ($(this).scrollTop()) {
            $('#button-scroll-up').fadeIn(200);
        } else {
            $('#button-scroll-up').fadeOut(200);
        }
    });

    $("#button-scroll-up").click(function() {
        $("html, body").animate({scrollTop: 0}, 200);
    });

    $('.checkbox').click(function() {
        var icon = $(this).find('i');
        icon.toggleClass("fas fa-check-circle");
        icon.toggleClass("far fa-circle");
    });

    $('#toggle_sort_filter_block').click(function () {
        $('#sort_filter_block').slideToggle(100);
        $(this).find("i").toggleClass("fa-sort-up").toggleClass("fa-sort-down");
        $(this).find("span").toggle();
    });

    var items = $('div#game_container'), item = items.children('div.wrapper');
    $('.toggle_tag').not('.disabled').click(function() {
        var button = $(this);
        var button_icon = button.find('i');
        var tag = $(this).data('tag');
        var column = $(this).data('column');
        var class_show = "fa-eye"
        var class_hidden = "fa-eye-slash"
        var o = button.hasClass("hidden") ? "show" : "hidden";
        var oi = button_icon.hasClass(class_hidden) ? class_show : class_hidden;
        button_icon.removeClass(class_show).removeClass(class_hidden).addClass(oi)
        button.removeClass("show").removeClass("hidden").addClass(o);

        if(o == "hidden") {
            if (column == 8 || column == 9 || column == 10) {
                filterColumnRange(column, $(this).data('min'), $(this).data('max'));
            } else {
                filterColumn(column, '0');
            }
        } else {
            filterColumn(column, '');
        }
    });
    $("#toggle_combined_slider").on( "slide change" ,function (event, ui) {
        $(".slider_tag.hidden").each(function () {
            filterColumnRange($(this).data('column'), ui.value, $(this).data('max'));
        });
    });
    $('.sort').not('.disabled').click(function () {
        var button = $(this);
        var button_icon = button.find('i');
        var class_neutral = "fa-sort"
        var class_asc = "fa-sort-up"
        var class_desc = "fa-sort-down"
        var sort_by = $(this).data('sort');
        var o = button.hasClass("desc") ? "asc" : "desc";
        var oi = button_icon.hasClass(class_desc) ? class_asc : class_desc;
        $('div.sort').each(function() {
            $(this).removeClass("asc").removeClass("desc");
            $(this).find('i').removeClass(class_asc).removeClass(class_desc).addClass(class_neutral)
        })
        button.addClass(o);
        button_icon.addClass(oi);
        orderColumn($(this).attr('data-column'), o);
    });



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
        icon = $('.checkbox').find('i');
        icon.removeClass("fas fa-check-circle");
        icon.addClass("far fa-circle");
        $('.add_user_field').each(function() {
            $(this).remove();
        });
    });
});

function send_user_form() {
    var form = document.getElementById("form_build_collection")
    $('input.add_user_input').each(function( index ) {
    if (this.value == "") {
        this.remove();
    }
    });
    document.getElementById("form_build_collection").submit();
}
