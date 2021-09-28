<html>
% include('head.tpl', title='bbg-compare | cached users')
<body>
<div class="container">
    <div class="block block-primary">
        <h1><i class="fas fa-database"></i> Cached Collections</h1>
        <p><a href="/">Back to Main Page</a></p>
    </div>
    <div class="block">
        <script>
        $(document).ready(function() {
            $('#cached_users_table').DataTable({
                "lengthMenu": [ 25, 100, 500, 1000 ],
                "order": [[ 5, 'desc' ]],
                columnDefs: [
                   {type: 'non-empty-string', targets: 0},
                   {type: 'non-empty-string', targets: 2},
                   {type: 'non-empty-string', targets: 3},
                   {type: 'non-empty-string', targets: 4},
                   {orderable: false, targets: 1}
                ]
            });
        });
        </script>
        <table id="cached_users_table" style="width: 100%;">
            <thead>
            <tr>
                <th>Username <i class="fas light fa-sort"></i></th>
                <th>Links</th>
                <th>Games <i class="fas light fa-sort"></i></th>
                <th>Rating <i class="fas light fa-sort"></i></th>
                <th>Comments <i class="fas light fa-sort"></i></th>
                <th>Last Update <i class="fas light fa-sort"></i></th>
            </tr>
            </thead>
            <tbody>
            % for user in result:
            <tr>
                <td data-order="{{user['username']}}"><span><i class="fas light fa-user"></i> {{user['username']}}</span></td>
                <td>
                    <a href="/bgg/{{user['username']}}" class="tooltip" data-tooltip="Open Collection"><i class="fas light fa-cubes"></i> Collection</a> -
                    <a href="/bgg/{{user['username']}}?exclude=prevowned&exclude=preordered&exclude=wishlist1&exclude=wishlist2&exclude=wishlist3&exclude=wishlist4&exclude=wishlist5&exclude=fortrade&exclude=want&exclude=wanttoplay&exclude=wanttobuy&exclude=notag" class="tooltip" data-tooltip="Open Collection with the tag 'own'"><i class="fas light fa-cubes"></i> Collection <i>[tag='own']</i></a> -
                    <a href="https://boardgamegeek.com/user/{{user['username']}}" class="tooltip" data-tooltip="Open {{user['username']}}s BGG Profile"><i class="far light fa-user"></i> BGG</a>
                </td>
                <td data-order="{{user['total_items']}}"><i class="fas light fa-cubes"></i> {{"?" if user['total_items'] is None else user['total_items']}}</td>
                <td data-order="{{user['total_ratings']}}"><i class="fas light fa-star-half-alt"></i> {{"?" if user['total_ratings'] is None else user['total_ratings']}}</td>
                <td data-order="{{user['total_comments']}}"><i class="far light fa-comment"></i> {{"?" if user['total_comments'] is None else user['total_comments']}}</td>
                <td data-order="{{user['updated_at']}}">
                    % if user['expired']:
                    <span class="tooltip" data-tooltip="Cache expired">
                        {{user['updated_at']}}
                        <i class="far light fa-clock"></i>
                    </span>
                    % else:
                    {{user['updated_at']}}
                    % end
                </td>


            </tr>
            % end
            </tbody>
        </table>
    </div>
</div>
% include('footer.tpl')
</body>
</html>