const messagesList = document.querySelector('.messages-list');
const messageForm = document.querySelector('.message-form');
const messageInput = document.querySelector('.message-input');



messageForm.addEventListener('submit', (event) => {
    event.preventDefault();
    

    const message = messageInput.value.trim();
    if (message.length === 0) {
      return;
    }
    
    const messageItem = document.createElement('li');
    messageItem.classList.add('message', 'sent');
    messageItem.innerHTML = `
    <div class="d-flex flex-row justify-content-end" style="margin-top: 30px; margin-right: 30px;"> 
    <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava5-bg.webp"
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
        <div class="header" style="padding: 10px; font-size: 13px"> 
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
      
        </div>
          `;
        messagesList.appendChild(messageItem);
        window.scrollTo(0, document.body.scrollHeight);


      });
  });
