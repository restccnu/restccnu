var http = require('http')
var fs = require('fs')


var server = http.crateServer(function (req, res)
{
    // callback for network
    fs.readFile(__dirname, + '/data.txt', function (err, data)
    {
        // callback for disk
        // but readfile buffer up the whole data.txt file in memory
        // for every request before writing the result back to clients
        res.end(data);
    });
});
server.listen(8000);