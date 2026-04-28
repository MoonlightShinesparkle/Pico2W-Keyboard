const contenedor = document.getElementById('estrellas-container');

function crearEstrella() {
    const div = document.createElement('div');
    div.classList.add('estrella');
    div.style.left = `${Math.random() * 100}%`;
    div.style.animationDuration = `${Math.random() * 3 + 2}s`;
    const size = Math.random() * 15 + 10;
    div.style.width = `${size}px`;
    div.style.height = `${size}px`;
    div.style.animationName= "moverArriba";
    div.style.animationDuration= `${Math.random() * 3 + 2}s`;
    contenedor.appendChild(div);
    div.addEventListener('animationend', () => {
        div.remove();
    });
}

window.addEventListener("DOMContentLoaded", () => {
    setInterval(crearEstrella, 500);
});