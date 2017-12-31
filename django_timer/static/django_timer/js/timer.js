"use strict";

var Timer = {

    pad: function(number) {
        if (number < 10) {
            number = '0' + number
        }
        return number
    },

    printDuration: function(duration){
        var seconds = Math.floor(duration)
        var minutes = Math.floor(seconds/60)
        var hours = Math.floor(minutes/60)
        seconds = seconds % 60
        minutes = minutes % 60
        if (hours) {
            return hours + ':' + Timer.pad(minutes) + ':' + Timer.pad(seconds)
        }
        return Timer.pad(minutes) + ':' + Timer.pad(seconds)
    },

    incrementTimer: function(){
        Timer.duration ++
        Timer.timer.innerHTML = Timer.printDuration(Timer.duration)
    },

    init: function(){
        Timer.timer = document.getElementById('django-timer-display')
        Timer.duration = Timer.timer.getAttribute('value')
        if (Timer.timer && Timer.timer.classList.contains('active')) {
            setInterval(Timer.incrementTimer, 1000)
        }
    },
}

Timer.init()

var toggler = document.getElementById('django-timer-segments-toggler')
toggler.onclick = function(){
    var segments = document.querySelectorAll('.django-timer-segments li.inactive')
    segments.forEach(function(segment){
        segment.classList.toggle('hide')
    })
}

var buttons = document.querySelectorAll('.django-timer button.ajax')
buttons.forEach( function(element) {
    element.onclick = function(event){
        event.preventDefault()
        event.stopPropagation()
        submitAction(element)
    }
})

function submitAction(button){
    var xhttp = new XMLHttpRequest()
    var url = button.getAttribute('formaction')
    var csrftoken = document.querySelector('.django-timer [name=csrfmiddlewaretoken]').getAttribute('value')
    xhttp.open("POST", url, true)
    xhttp.setRequestHeader("X-CSRFToken", csrftoken)
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4){
            if (this.status == 200){
                window.location.reload()
            } else {
                console.log(this)
            }
        }
    };
    xhttp.send()
}
