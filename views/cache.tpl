<html>
<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Sans:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <link href="/style.css" rel="stylesheet" type="text/css">
    <script src="https://kit.fontawesome.com/9e34df6d41.js" crossorigin="anonymous"></script>
</head>
<body>
<div class="container">
    <div class="block block-primary">
        <h1><i class="fas fa-database"></i> Cached Collections</h1>
        <p><a href="/">Back to Main Page</a></p>
    </div>
    <div class="wrapper_loading_status">
        <div class="grid_title">Username</div>
        <div class="grid_collection">Created At</div>
        <div class="grid_rating">Updated At</div>
        % for user in result:
            <div class="grid_title">
                <a href="/bgg/{{user['username']}}"><i class="fas fa-user"></i> {{ user.username }}</a> <a href="https://boardgamegeek.com/user/{{user['username']}}"><i class="fas fa-external-link-alt"></i> BGG</a>
            </div>
            <div class="grid_collection">
                {{ user.created_at }}
            </div>
            <div class="grid_rating">
                {{ user.updated_at }}
            </div>
        % end
        </div>
    </div>
% include('footer.tpl')
</body>
</html>