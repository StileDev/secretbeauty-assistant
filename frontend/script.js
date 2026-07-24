// ---------- Thème clair/sombre ----------
const themeToggle = document.getElementById('themeToggle');
const savedTheme = localStorage.getItem('secretbeauty-theme') || 'dark';
document.body.setAttribute('data-theme', savedTheme);

themeToggle.addEventListener('click', () => {
  const current = document.body.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.body.setAttribute('data-theme', next);
  localStorage.setItem('secretbeauty-theme', next);
});

// ---------- Identifiant client (pour le backend) ----------
let contactId = localStorage.getItem('secretbeauty-contact');
if (!contactId) {
  contactId = 'client_' + Date.now();
  localStorage.setItem('secretbeauty-contact', contactId);
}

// ---------- Conversations affichées dans la sidebar ----------
const conversations = [
  {
    id: 'assistante',
    name: 'Assistante Secret Beauty',
    status: 'en ligne · lun–sam',
    messages: [
      { who:'bot', time:'09:12', html:`Bonjour, bienvenue chez <b>Secret Beauty</b> ✨ Je peux te renseigner sur nos soins, nos produits, nos horaires ou comment commander. Que veux-tu savoir ?` }
    ]
  }
];

let activeId = 'assistante';

const convList = document.getElementById('convList');
const chatInner = document.getElementById('chatInner');
const chatScroll = document.getElementById('chatScroll');
const topTitle = document.getElementById('topTitle');
const topStatus = document.getElementById('topStatus');
const inputEl = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const appEl = document.getElementById('app');
const menuBtn = document.getElementById('menuBtn');
const overlay = document.getElementById('overlay');
const quickReplies = document.getElementById('quickReplies');
const newChatBtn = document.getElementById('newChatBtn');

function currentConv(){ return conversations.find(c => c.id === activeId); }

function stripHtml(html){
  const tmp = document.createElement('div');
  tmp.innerHTML = html;
  const t = tmp.textContent;
  return t.length > 34 ? t.slice(0,34) + '…' : t;
}

function renderList(){
  convList.innerHTML = '';
  conversations.forEach(c => {
    const last = c.messages[c.messages.length - 1];
    const item = document.createElement('div');
    item.className = 'conv-item' + (c.id === activeId ? ' active' : '');
    item.innerHTML = `
      <div class="conv-name">${c.name}</div>
      <div class="conv-preview">${stripHtml(last.html)}</div>`;
    item.addEventListener('click', () => selectConversation(c.id));
    convList.appendChild(item);
  });
}

function renderChat(){
  const c = currentConv();
  topTitle.textContent = c.name;
  topStatus.textContent = c.status;
  chatInner.innerHTML = '';
  c.messages.forEach(appendMsgEl);
  scrollBottom();
}

function appendMsgEl(m){
  const row = document.createElement('div');
  row.className = 'msg-row ' + m.who;
  if(m.who === 'bot'){
    row.innerHTML = `
      <div class="msg-avatar"><img src="assets/logo.jpeg" alt="Secret Beauty" style="width:100%;height:100%;object-fit:cover;border-radius:8px;"></div>
      <div class="msg-content">
        <div class="msg-text">${m.html}</div>
        <div class="msg-time">${m.time}</div>
      </div>`;
  } else {
    row.innerHTML = `
      <div class="msg-content">
        <div class="msg-text">${m.html}</div>
        <div class="msg-time">${m.time}</div>
      </div>`;
  }
  chatInner.appendChild(row);
}

function scrollBottom(){ chatScroll.scrollTop = chatScroll.scrollHeight; }

function nowTime(){
  const d = new Date();
  return d.getHours().toString().padStart(2,'0') + ':' + d.getMinutes().toString().padStart(2,'0');
}

function selectConversation(id){
  activeId = id;
  renderList();
  renderChat();
  appEl.classList.remove('sidebar-open');
}

// ---------- Appel réel au backend Flask ----------
async function getReponseIA(message){
  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: message, contact_whatsapp: contactId })
    });
    const data = await res.json();
    return data.reponse || "Désolée, je n'ai pas pu répondre. Réessaie.";
  } catch (err) {
    console.error("Erreur fetch :", err);
    return "Impossible de contacter le serveur pour le moment. Vérifie que le backend tourne bien.";
  }
}

function showTyping(){
  const row = document.createElement('div');
  row.className = 'typing-row';
  row.id = 'typingRow';
  row.innerHTML = `
    <div class="msg-avatar">SB</div>
    <div class="typing-dots"><span></span><span></span><span></span></div>`;
  chatInner.appendChild(row);
  scrollBottom();
}
function removeTyping(){
  const t = document.getElementById('typingRow');
  if(t) t.remove();
}

async function handleSend(text){
  const value = (text !== undefined ? text : inputEl.value).trim();
  if(!value) return;
  const c = currentConv();
  const userMsg = { who:'user', time: nowTime(), html: value.replace(/</g,'&lt;') };
  c.messages.push(userMsg);
  appendMsgEl(userMsg);
  inputEl.value = '';
  scrollBottom();
  renderList();

  showTyping();
  const reponseBrute = await getReponseIA(value);
  removeTyping();

  const reponseFormatee = marked.parse(reponseBrute);

  const botMsg = { who:'bot', time: nowTime(), html: reponseFormatee };
  c.messages.push(botMsg);
  appendMsgEl(botMsg);
  scrollBottom();
  renderList();
}

sendBtn.addEventListener('click', () => handleSend());
inputEl.addEventListener('keydown', e => { if(e.key === 'Enter') handleSend(); });
quickReplies.addEventListener('click', e => {
  const btn = e.target.closest('.chip');
  if(btn) handleSend(btn.dataset.msg);
});

menuBtn.addEventListener('click', () => appEl.classList.add('sidebar-open'));
overlay.addEventListener('click', () => appEl.classList.remove('sidebar-open'));
newChatBtn.addEventListener('click', () => selectConversation('assistante'));

renderList();
renderChat();