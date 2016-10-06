// Facebook SDK handles the call to the facebook API and redirects the user to 
// the appropriate page after successful confirmation
function statusChangeCallback(response) {
    if (response.status === 'connected') {
        authenticate();
    } else if (response.status === 'not_authorized') {
        swal('...Oops!', 'Please click OK to log into this app.', 'error');

    } else {
        swal('...Oops!', 'Seems you are not logged into facebook', "error");
    }
}

function loginFacebook() {
    FB.login(function(response) {
        statusChangeCallback(response);
    }, {
        scope: 'public_profile,email'
    });
}

window.fbAsyncInit = function() {
    FB.init({
        appId: '1205949532779825',
        cookie: true,
        xfbml: false,
        version: 'v2.5'
    });
};
// Load the SDK asynchronously
(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s);
    js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

function authenticate() {
    FB.api('/me', {
        locale: 'en_US',
        fields: 'name, email, id'
    }, function(response) {
        $.ajax({
            type: "POST",
            url: $SCRIPT_ROOT + "/social/login",
            data: JSON.stringify(response),
            contentType: 'application/json;charset=UTF-8',
            success: function(result) {
                swal('Welcome', result.status, 'success');
                setTimeout(function() {
                    window.location.href = $SCRIPT_ROOT + "/dashboard"
                }, 2000);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
}