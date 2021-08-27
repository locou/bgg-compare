<html>
<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Sans:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <link href="/style.css" rel="stylesheet" type="text/css">
    <link rel="icon" href="data:;base64,iVBORw0KGgo=">
    <script src="https://kit.fontawesome.com/9e34df6d41.js" crossorigin="anonymous"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="/script.js"></script>
</head>
<body>
<div class="container">
    <div class="block block-primary">
        <h1>Welcome to bgg-compare</h1>
        <p>This tool makes it possible to compare your collection with the ratings and comments of other selected users. Sort by number of plays, ratings and difference between your and their ratings.</p>
        <p>Start by typing your <a href="https://boardgamegeek.com/">https://boardgamegeek.com/</a> Username into the input textfield and hit Submit. It takes some time for the bgg-api to fetch your collection, so be patient. Usually it takes less then a minute.</p>
        <p>You may add any amount of additional users by clicking <i class="fas fa-user-plus"></i> <b>Add User</b>. Requested user collections are cached for 48h, so future requests are handeled much faster.</p>
    </div>

    <form id="form_build_collection" method="get" action="idk" onsubmit="send_user_form()">
        <input id="main_user" type="text" placeholder="Username" required>
        <p>
            <button class="button" type="submit"><i class="fas fa-cubes"></i> Submit</button>
            <button id="reset_fields" class="button reverse-color" type="reset"><i class="fas fa-redo-alt"></i> Reset</button>
            <a id="add_user_field" class="button"><i class="fas fa-user-plus"></i> Add User</a>
        </p>
    </form>
</div>
% include('footer.tpl')
</body>
</html>