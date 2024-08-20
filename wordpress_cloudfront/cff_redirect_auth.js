function handler(event) {
    var request = event.request;
    var cookies = request.cookies;
    var host = request.headers.host.value;
    var newurl = 'https://' + host +'/wp-login.php'
    var uri = request.uri
    console.log("Event : " + JSON.stringify(event));
    
    
    var auth_cookie = Object.keys(cookies).filter(v => v.startsWith('wordpress_logged_in_'));
    
    console.log("size cookies: " + auth_cookie.length);
    
    if(auth_cookie.length != 0){
        console.log("Auth cookie : " + JSON.stringify(auth_cookie));
    }else if(!uri.includes("wp-admin/css") && !uri.includes("wp-admin/js") && !uri.includes("wp-admin/images")){
        var response = {
                statusCode: 302,
                statusDescription: 'Found',
                headers:
                    { "location": { "value": newurl } }
                }
        console.log("Response : " + JSON.stringify(response));
        return response;
    }
    
    return request;
}