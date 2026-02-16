const http = require('http');

// Create the server instance
const server = http.createServer((req, res) => {
    // Case 1: Success (200 OK)
    if (req.url === '/') {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end('<h1>Welcome! Server is running.</h1>');
    }
    
    // Case 2: Simulated Error (500 Internal Server Error)
    else if (req.url === '/error') {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Internal Server Error');
    }

    // Case 3: Not Found (404 Not Found)
    else{
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found');}
});

server.listen(8081, 'localhost', () => {
    console.log('Server started http://localhost:8081');
});
