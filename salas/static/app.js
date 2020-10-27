/* This credentials are user for Basic Authentication in api requests */
let global_user;
let global_password;
let authorization;

let current_user_email;
let current_user_username;

let datepickerinicio, datepickerfin;

const API_PATH = location.pathname + 'api/v1/'

let Modalelem = document.querySelector('.modal');
let instance;

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const setUserPassword = function (user, password, token) {
    global_user = user;
    global_password = password;
    token = token;
    authorization = btoa(global_user+':'+global_password);
}

const generateUserButton = function(userData){
    /* Por cada usuario existente mostrar un boton con el formato:
    <a class="waves-effect waves-light btn-large tamanio">Button</a>
    */
    const usersList = document.getElementById("usersList");
    var aElem = document.createElement('a');
    aElem.classList.add("waves-effect");
    aElem.classList.add("waves-light");
    aElem.classList.add("btn-large");
    aElem.classList.add("tamanio");
    aElem.innerHTML = userData.username;
    usersList.appendChild(aElem);

    aElem.addEventListener("click", function(){
       current_user_email = userData.email;
       current_user_username = userData.username;
       instance.close();
    });
}

const generateSalaRadioButton = function(salaData){
    /* Por cada Sala, pondrá un RadioButton con el formato:
    <p>
          <label>
            <input name="group1" type="radio" checked />
            <span>Red</span>
          </label>
    </p>
     */
    const options = document.getElementById("salasOptions");
    var pElem = document.createElement('p');
    var labelElem = document.createElement('label');
    var radioElem = document.createElement('input');
    radioElem.type = 'radio';
    radioElem.name = "group1";
    radioElem.id = salaData.id;
    radioElem.value = salaData.id;
    var spanElem = document.createElement('span');
    spanElem.innerText = salaData.nombre;
    labelElem.appendChild(radioElem);
    labelElem.appendChild(spanElem);
    pElem.appendChild(labelElem);
    options.appendChild(pElem);
}

const initDateTimePickers = function() {
    let initDate = new Date();
    datepickerinicio = new MtrDatepicker({
      target: 'datepicker-inicio',
      timestamp: initDate.getTime(),
    });
    datepickerfin = new MtrDatepicker({
      target: 'datepicker-fin',
      timestamp: initDate.getTime(),
    });
}

const initListeners = function() {
    var reservarBtn = document.getElementById("reservarBtn");

    reservarBtn.addEventListener("click", function(){
        let radio = document.querySelector('input[name="group1"]:checked');
        if (!radio) {
            alert('Debes elegir una sala');
            return false;
        }
        let inicio = datepickerinicio;
        let fin = datepickerfin;

        let now = new Date().toISOString();
        let activo = (inicio >= now && now < fin );

        let diff = fin.getTimestamp() - inicio.getTimestamp();
        console.log("diferencia en horas" + diff);
        let horas = diff/(1000*60*60);
        console.log("diferencia en horas" + horas);

        if (horas>2){
            alert('No puedes reservar mas de 2 horas');
            return false;
        }

        req = {
            sala: location.protocol + '//' +location.host + API_PATH + 'salas/' + radio.value + '/',
            usuario: {
                email: current_user_email,
                username: current_user_username
            },
            inicio: inicio.toISOString(),
            fin: fin.toISOString(),
            activa: activo
        }

        const csrftoken = getCookie('csrftoken');

        fetch( API_PATH + 'reservaciones/', {
            method: "POST",
            headers: { 'Authorization': 'Basic ' + authorization,
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken},
            body: JSON.stringify(req),
        }).then((res) => {
            return res.json();
        })
        .then((res) => {
            console.log(res);
        }).catch(error => console.error(error));
    });
}

const getUsersList = function() {
    fetch(API_PATH + 'users/', {
        method: "GET",
        headers: { 'Authorization': 'Basic ' + authorization }
    }).then((res) => {
        return res.json();
    })
    .then((res) => {
        res.results.forEach((user) =>{
            generateUserButton(user);
        });
    }).catch(error => console.error(error));
}

const getSalasList = function() {
    fetch(API_PATH + 'salas/', {
        method: "GET",
        headers: { 'Authorization': 'Basic ' + authorization }
    }).then((res) => {
        return res.json();
    })
    .then((res) => {
        res.results.forEach((sala) =>{
            generateSalaRadioButton(sala);
        });
    }).catch(error => console.error(error));
}

const getReservacionesList = function() {
    fetch(API_PATH + 'reservaciones/', {
        method: "GET",
        headers: { 'Authorization': 'Basic ' + authorization }
    }).then((res) => {
        return res.json();
    })
    .then((res) => {
        res.forEach((reservacion) =>{
            console.log(reservacion);
        });
    }).catch(error => console.error(error));
}

const start = function(){
    getUsersList();
    getSalasList();
    initDateTimePickers();
    initListeners();
    instance = M.Modal.init(Modalelem,{
        dismissible:false, opacity: 1});
    instance.open();
    getReservacionesList();
}