$(document).ready(function() {
    $('body').fadeIn(1000);
});

$('#login').on('click', async function(event){
    event.preventDefault();

    const response = await fetch('http://127.0.0.1:8000/api/v1/authentication/oauth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            username: $('#username').val(),
            password: $('#password').val()
        })
    }).then(async (response) => {
        
        if(response.status===200) {
            return response.json();
        }else{
            $('#message').show().delay(3000).fadeOut();
            throw new Error('Request failed with status');
        }
    
    }).then(async (data) => {

        localStorage.setItem('tokens', JSON.stringify(data));
        return data;
    
    }).catch(error => {
        console.error('Error:', error);
    });

    if(response){
        window.location.href = '/frontend/chat';
    }

})
