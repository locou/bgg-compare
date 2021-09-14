<html>
% include('head.tpl', title='bbg-compare | cached users')
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