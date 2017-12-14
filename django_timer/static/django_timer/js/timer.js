function pad(number){
    if (number < 10){
        number = '0' + number
    }
    return number
}

function printDuration(duration){
    var seconds = Math.floor(duration)
    var minutes = Math.floor(seconds/60)
    var hours = Math.floor(minutes/60)
    seconds = seconds % 60
    minutes = minutes % 60
    if (hours) {
        return hours + ':' + pad(minutes) + ':' + pad(seconds)
    }
    return pad(minutes) + ':' + pad(seconds)
}

var timer = document.getElementById('django-timer')

if (timer) {
    var duration = timer.getAttribute('value')
    if ( duration && timer.classList.contains('active') ){
        setInterval(function() {
            duration++
            timer.innerHTML = printDuration(duration)
        }, 1000)
    }
}

var buttons = document.querySelectorAll('.django-timer button.ajax')
buttons.forEach( function(element) {
    element.addEventListener('click', 
        function(event) {
            event.preventDefault()
            event.stopPropagation()
            submitAction(element)
        }
    )
})

function submitAction(button){
    var xhttp = new XMLHttpRequest()
    var url = button.getAttribute('formaction')
    var csrftoken = document.querySelector('.django-timer [name=csrfmiddlewaretoken]').getAttribute('value')
    xhttp.open("POST", url, true)
    xhttp.setRequestHeader("X-CSRFToken", csrftoken)
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4){
            console.log(this)
            if (this.status == 200){
                window.location.reload()
            }
        }
    };
    xhttp.send()
}
