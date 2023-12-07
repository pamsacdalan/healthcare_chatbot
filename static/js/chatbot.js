const messagesList = document.querySelector('.messages-list');
const messageForm = document.querySelector('.message-form');
const messageInput = document.querySelector('.message-input');
const submitButton = document.querySelector('.message-form button[type="submit"]');
// const time = document.querySelector('.message-content');


// var time_chat = document.getElementById('message-content').getAttribute('data-value')
var newDate = new Date().toLocaleDateString();
var newtime = new Date().toLocaleTimeString();
var container = document.getElementById('appt_button');

//var date_time = newDate +  " " + newtime;
var date_time = new Date(); 
var date_mm_dd_yyyy = new Date(date_time).toDateString().slice(4,16);
var time = date_time.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })
var date_formatted = date_mm_dd_yyyy + " " + time
console.log(date_formatted);


messageForm.addEventListener('submit', (event) => {
    event.preventDefault();
      
    const message = messageInput.value.trim();
    if (message.length === 0) {
      closeLoader()
      return;
    }
    
    const messageItem = document.createElement('li');
    messageItem.classList.add('message', 'sent');
    messageItem.innerHTML = `
    <div class="d-flex flex-row justify-content-end" style="margin-top: 30px; margin-right: 30px;"> 
    <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava2-bg.webp"
        alt="avatar 3" style="width: 30px; height: 80%; margin-left: 10px; margin-right: 5px;">
    <div class="header" style="padding: 10px; font-size: 13px"> 
        <li class="message sent" >


        <div class="message-text">
            <div class="message-sender">
                <b>You</b>
            </div>
          
            <div class="message-content">
                ${message}
              
            </div>
            <br>
            <div class="message-content text-muted" style="font-size: 10px;">
                ${date_formatted}
            </div>
        </div>
        </div>
        
        </div>
        </div>`;
    messagesList.appendChild(messageItem);

    messageInput.value = '';

    fetch('', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        'message': message
        
      })
      
    })
      .then(response => response.json())
      .then(data => {
        const response = data.response;
        const messageItem = document.createElement('li');
        messageItem.classList.add('message', 'received');
        
        messageItem.innerHTML = `
 
        <div class="d-flex flex-row justify-content-start" style="margin-top: 30px; margin-right: 30px;"> 
        <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava5-bg.webp"
            alt="avatar 3" style="width: 30px; height: 80%; margin-left: 10px; margin-right: 5px;">
        <div class="header text-black" style="padding: 10px; font-size: 13px; background-color: white;"> 
            <div class="message-content">

            <div class="message-content">
                <li class="message received">
        <div class="message-text">
            <div class="message-sender">
              <b>Quicare</b>
            </div>
            <div class="message-content">
                ${response}
            </div>
            <br>
            <div class="message-content text-muted" style="font-size: 10px;">
            ${date_formatted}
            </div>
        </div>
      
        </div>
        </div>
          `;
        messagesList.appendChild(messageItem);
        window.scrollTo(0, document.body.scrollHeight);
      messageItem.lastChild.scrollIntoView(true)
      closeLoader()
  });
  
});

// Spinner Functions

function openLoader() {
  document.getElementById("loadingModal").style.display = "block";

  messageInput.disabled = true; 
  submitButton.disabled = true;  
}

function closeLoader() {
  document.getElementById("loadingModal").style.display = "none";

  messageInput.disabled = false;
  submitButton.disabled = false;
}
