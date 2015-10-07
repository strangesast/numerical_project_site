console.log("hello");

var inputs = []

inputs.push(document.getElementById('scale_input'))
inputs.push(document.getElementById('rotate_input'))
inputs.push(document.getElementById('shear_input'))
inputs.push(document.getElementById('shearrotate_input_shear'))
inputs.push(document.getElementById('shearrotate_input_rotate'))
inputs.push(document.getElementById('rotateshear_input_rotate'))
inputs.push(document.getElementById('rotateshear_input_shear'))

for(var i=0; i < inputs.length; i++) {
    var input = inputs[i];
}

var updates = []

updates.push(document.getElementById('scale_update'))
updates.push(document.getElementById('rotate_update'))
updates.push(document.getElementById('shear_update'))
updates.push(document.getElementById('rotateshear_update'))
updates.push(document.getElementById('shearrotate_update'))

var submit_request_for_update = function(what) {
    var url = '/recalculate/' + what.type
    console.log(url)
    delete what['type']

    prom = new Promise(function(resolve, reject) {
        var request = new XMLHttpRequest();
        request.open('POST', url, true);
        request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
        request.send(JSON.stringify(what))
        request.onload = function() {
            resolve(request)
        }
    })

    return prom;
}

for(var i=0; i < updates.length; i++) {
    var update = updates[i];
    var qsa = update.parentNode.querySelectorAll('input')

    var dict = {};
    var inputs = [];
    var update_image = update.parentNode.parentNode.querySelector('img')
    for(var j=0; j<qsa.length; j++) {
        var input = qsa[j];
        inputs.push(input)
    }

    var click_function = function(_inputs, _image) {
        return function(e) {
            var values = []
            for(var a=0; a<_inputs.length; a++) {
                var target = e.target
                var input = _inputs[a];
                var name = input.name
                var value = input.value

                if(value != "") {
                    values.push({'name': input.name, 'value': input.value})
                }
            }
            if ( values.length > 0 ) {
                target.disabled = true;
                var req = submit_request_for_update({
                    'type' : target.name,
                    'values' : values
                });

                req.then(function(result) {
                    console.log(_image)
                    _image.src = _image.src.split('?')[0] + '?random=' + Date.now()
                    try {
                        console.log(JSON.parse(result.response))
                    } catch (e) {
                        console.log(result.response)
                    }
                }).catch(function() {
                    alert('failed to complete request')
                }).then(function() {
                    target.disabled = false;
                })
            }
        }
    }(inputs, update_image);

    update.addEventListener('click', click_function)
}
