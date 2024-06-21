//const url = 'http://127.0.0.1:8000/api/v1/';
const url = 'https://fastapi-chatbot-quejas-y-sugerencias.onrender.com/api/v1/';
const assistant_name = 'Asistente de quejas';
const welcome_message = '👋 ¡Hola!, ¿Que necesitas saber el día de hoy?';
let id_mensaje = 0;

// --------------------------------------------------
//                    functions
// --------------------------------------------------

function format_chatbot_message(id){

  const chatbotMessage = `
  <div class='chatbot-message col-12 py-4 d-flex justify-content-center' id='${id}' style='display:none;'>
      <div class='d-flex col-8' id='chatbot-message-content'>
          <img src='/static/imgs/chatbot.png' width='40' height='40'>
          <div class='m-2'>
              <h6>${assistant_name}</h6>
              <p></p>
              <div class='container-animacion'>
                <div class='cargando'>
                  <div class='pelotas'></div>
                  <div class='pelotas'></div>
                  <div class='pelotas'></div>
                </div>
              </div>
          </div>
      </div>
  </div>`;

  return chatbotMessage;

}


function format_user_message(message){

  const userMessage = `
  <div class='user-message col-12 py-4 d-flex justify-content-center'>
      <div class='d-flex col-8' id='user-message-content'>
          <img src='/static/imgs/user.png' width='40' height='40'>
          <div class='m-2'>
              <h6>Tú</h6>
              <p>${message}</p>
          </div>
      </div>
  </div>`;

  return userMessage;

}


function hide_message_container(){
  $('#btn-enviar').hide();
  $('#input-message').hide();
}


function show_message_container(){
  $('#btn-enviar').show();
  $('#input-message').show();
}


function disable_form_message(){
  $('#btn-detener').show();
  $('#btn-enviar').hide();
  $('#input-message').prop('disabled', true);
}


function enable_form_message(){
  let send_button = $('#btn-enviar');
  send_button.css('color', '#000000');
  send_button.css('background-color', '#c5c5c5');
  send_button.prop('disabled', true);
  send_button.show();
  $('#btn-detener').hide();
  $('#input-message').prop('disabled', false);
}


async function initialize(){

  await create_conversational_thread();
  
  let send_button = $('#btn-enviar');
  send_button.css('background-color', '#c5c5c5');
  send_button.css('color', '#000000');
  send_button.prop('disabled', true);
  $('#btn-detener').hide();
  hide_message_container();
}


function get_message(){
  const message = $('#input-message').val();
  $('#input-message').val('');
  return message;
}


async function send_message(id, user_message, signal){

  const message_url = url + 'chatbot/message';
  const thread_id = localStorage.getItem('thread_id');
  const dates = JSON.parse(localStorage.getItem('dates'));

  console.log(dates);
  console.log(typeof dates);


  const response = await fetch(message_url, {
    signal: signal,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ dates, thread_id, user_message })
  }).then(
    response => response.json()
  ).then(
    async (data) => {
      const md = window.markdownit();
      const resultHtml = md.render(data['msg']);
      console.log(data);
      console.log(resultHtml);
      $(`#${id} .m-2 p`).append(resultHtml);
    }
  ).catch(error => {

    if (error.name === 'AbortError') {
      $(`#${id} .m-2 p`).append('<h7 class="text-secondary">Mensaje detenido<h7>');
    } else {
      $(`#${id} .m-2 p`).append('<h7 class="text-danger">Hubo un error en el mensaje<h7>');
    }
  
  });

  return response;
}


async function delete_conversation_thread(){
	var requestOptions = {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		}
	};

  const thread_url = url+'chatbot/thread_id/'+localStorage.getItem('thread_id')
	navigator.sendBeacon(thread_url, requestOptions);

	localStorage.removeItem('thread_id');
}


async function create_conversational_thread(){
  const thread_url = url+'chatbot/thread_id';
  //let url = '';
  const response = await fetch(thread_url, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  }).then(response => response.json())
    .then(data => data
    ).catch(error => {
      return {'msg':'<h7 class="text-danger">Error, no se ha podido establecer una conversacion<h7>'};
    });
  
  localStorage.setItem('thread_id', response['thread_id']);

  return response;
}


// --------------------------------------------------
//                      events
// --------------------------------------------------

$('#input-message').on('keyup', function(event){

  let text = $(this).val();
  let button = $('#btn-enviar');

  if(text.trim() === ""){
    button.css('color', '#000000');
    button.css('background-color', '#c5c5c5');
    button.prop('disabled', true);
  }else{
    if (event.keyCode === 13) {
      button.trigger('click');
    }

    button.css('color', '#ffffff');
    button.css('background-color', '#007bff');
    button.prop('disabled', false);
  }

});


$('#confirm-button').click(function() {

  function isValidDate(date) {
    return date instanceof Date && !isNaN(date);
  }

  const fromDate = new Date($('#datepicker').val());
  const toDate = new Date($('#datepicker2').val());

  if (!isValidDate(fromDate) || !isValidDate(toDate)) {
    console.log('Una o ambas fechas son inválidas');
  }

  if(fromDate>toDate){
    console.log('error');
  }

  localStorage.setItem('dates', JSON.stringify({'from_date':fromDate, 'to_date':toDate}));
  show_message_container();

});


$('#btn-enviar').on('click', async function(){

  disable_form_message();
  const userMessage = get_message();
  // getting identifier to add in chatbot message
  const id = 'container-chatbot-message-'+id_mensaje++;
  const formattedChatbotMessage = format_chatbot_message(id);
  const formattedUserMessage = format_user_message(userMessage);

  // adding messages to conversation
  $('.conversation').append(formattedUserMessage);
  $('.conversation').append(formattedChatbotMessage);

  window.scrollTo(0, document.documentElement.scrollHeight);

  // sending message to chatbot
  controller = new AbortController();
  const signal = controller.signal;
  const response = await send_message(id, userMessage, signal);

  $('.container-animacion').remove();
  $(`#${id}`).fadeIn();

  window.scrollTo(0, document.documentElement.scrollHeight);

  enable_form_message();

});


$('#btn-detener').on('click', function(){
  enable_form_message();
  if (controller) {
    controller.abort(); // Se llama al método abort() del controlador para cancelar la petición
    console.log('Petición cancelada');
  }
});


$(window).on('beforeunload', async function() {
  if(localStorage.getItem('thread_id')!==null){
    await delete_conversation_thread();
  }
});


// --------------------------------------------------
//                 initialization
// --------------------------------------------------

$(document).ready(async function() {
  await initialize();
  $("h6").text(`{{assistant_name}}`.replace("{{assistant_name}}", assistant_name));

  $(".loader-wrapper").fadeOut(1200, function() {
    $("#contenido").fadeIn(1500);
  });
});

//$( document ).ready(function(){});
//$( window ).on( "load", function(){});