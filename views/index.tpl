<html>
<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Sans:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <link href="/style.css" rel="stylesheet" type="text/css">
    <link rel="icon" href="data:;base64,iVBORw0KGgo=">
    <script src="https://kit.fontawesome.com/9e34df6d41.js" crossorigin="anonymous"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
<div class="container">
    <form id="form_build_collection" method="get" action="idk" onsubmit="send_user_form()">
        <input id="main_user" type="text" required>
        <button type="submit">Submit</button>
        <button type="reset">Reset</button>
    </form>
    <a id="add_user_field">Add a user</a>
    <script type=text/javascript>
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
    $('a#add_user_field').click(function() {
        $('form#form_build_collection').append('<div class="add_user_container"><input type="text" name="add_user" class="add_user_input" /><a class="remove_user_input">REMOVE</a></div>');
    });

    $('a.remove_user_input').each(function() {
        console.log('hey')
        $(this).on("click", function(index){
            console.log('hey')
            $(this).remove()
        });
    });

    </script>
</div>
</body>
</html>