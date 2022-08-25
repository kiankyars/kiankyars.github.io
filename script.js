document.addEventListener('DOMContentLoaded', function() {
    let pills = document.getElementsByClassName('nav-link');
    for (let i = 0; i < pills.length; i++){
        pills[i].addEventListener('mouseenter', function(){
        pills[i].classList.add("active");
    });
    pills[i].addEventListener('mouseleave', function(){
        pills[i].classList.remove("active");
    });
}
})