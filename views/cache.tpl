<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Sans:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <link href="/style.css" rel="stylesheet" type="text/css">
    <script src="https://kit.fontawesome.com/9e34df6d41.js" crossorigin="anonymous"></script>
    <title>bbg-compare | cached users</title>
</head>
<body>
<div class="container">
    <div class="block block-primary">
        <h1><i class="fas fa-database"></i> Cached Collections</h1>
        <p><a href="/">Back to Main Page</a></p>
    </div>
    <div class="block">
        % for updated_at, users in grouped_users_by_updated_at.items():
        <h1>{{updated_at }}</h1>
        %for user in users:
        <span><a href="/bgg/{{user['username']}}"><i class="fas fa-user"></i> {{ user.username }}</a></span>
        %end
        % end
    </div>
</div>
% include('footer.tpl')
</body>
</html>