/*
    Este módulo de JavaScript se utilizará para lo siguiente:
    1. Obtener las disciplinas que un entrenador imparte, y en función de esto, activará los
       checkboxes en el formulario que será usado para editar la información de un
       entrenador.
    2. Obtener las disciplinas que un atleta entrena, y en función de esto, activará los
       checkboxes en el formulario que será usado para editar la información de un atleta.
    3. Obtener el sexo de una persona, y en función de esto, el select que lo contenga,
       se seleccionará automáticamente al cargar el formulario para editar la información
       de un atleta o un entrenador.
*/

let contador = 1; // Variable para manejar el JSON que el backend nos dará como respuesta.
let checkbox;     // Variable que almacenará un checkbox. 
let peticion;     // Variable que almacenará las respuestas del backend en función de la petición.
let respuesta;    // Variable que convertirá en formato JSON la respuesta del backend.

// Variable que almacena los labels de los checkboxes.
let etiquetas = document.querySelectorAll('.form-check-label');

// Función que activa los checkboxes.
const activarCheckbox = () => {
    if (typeof (etiquetas) === 'object' && typeof(respuesta) === 'object') {
        etiquetas.forEach(etiq => {
            if (respuesta[`${contador}`] === etiq.innerText) {
                checkbox = document.querySelector(`.form-check-input[id=${etiq.attributes.for.nodeValue}]`);
                checkbox.checked = true;
            }
        });
    }
    
    contador = 1;
};

// Función que obtiene las disciplinas que un atleta entrena.
const atletasDisciplinas = async (pk) => {
    peticion = await fetch(`http://localhost:8000/entrenamientos/atletas_disciplinas/${pk}/`, {
        method: 'GET',
    });

    respuesta = await peticion.json();

    for (contador in respuesta) {
        activarCheckbox();
    }
};

// Función que obtiene las disciplinas que un entrenador imparte.
const entrenadoresDisciplinas = async(pk) => {
    peticion = await fetch(`http://localhost:8000/entrenamientos/entrenadores_disciplinas/${pk}/`, {
        method: 'GET',
    });

    respuesta = await peticion.json();

    for (contador in respuesta) {
        activarCheckbox();
    }
    
};
// Función que obtiene el sexo de una persona (ya sea un atleta o entrenador).
const personaSexo = async (pk) => {
    peticion = await fetch(`http://localhost:8000/entrenamientos/persona_sexo/${pk}/`, {
        method: 'GET'
    });

    respuesta = await peticion.json();
    const option = document.querySelector(`option[value=${respuesta['sexo']}]`);
    option.selected = true;
};

export { atletasDisciplinas, entrenadoresDisciplinas, personaSexo };