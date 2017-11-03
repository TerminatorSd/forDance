/**
 * Created by xsd on 17-11-3.
 */
window.onload = function () {

};

function submitDance() {

    var name = document.getElementsByTagName('select')[0].value;
    var place = document.getElementsByTagName('select')[1].value;
    var csrf = document.getElementsByTagName('input')[0].value;
    var time = document.getElementsByTagName('input')[1].value;

    $.ajax({
        url: '/toDance/',
        dataType: 'JSON',
        type: 'POST',
        data: {
            name: name,
            place: place,
            time: time,
            csrfmiddlewaretoken: csrf
        },
        success: function (data) {
            console.log(data);

            if(data[0] === 'ok')
            {
               window.location.href = "/success/";
            }

        },
        fail: function () {
            console.log("Request for toDance failed!");
        }
    });
}

function getDance() {

    var place = document.getElementsByTagName('select')[0].value;
    var csrf = document.getElementsByTagName('input')[0].value;
    var time = document.getElementsByTagName('input')[1].value;

    $.ajax({
        url: '/getDance/',
        dataType: 'JSON',
        type: 'POST',
        data: {
            place: place,
            time: time,
            csrfmiddlewaretoken: csrf
        },
        success: function (data) {
            console.log(data);

            if(data[0]) {
                document.getElementsByClassName('record')[0].innerHTML = '';
                alert("今晚没人跳舞哦~");
            }

            else {
                var str = '';
                str += '<table> <tr> <th>name</th> <th>time</th> </tr> ';

                for (var item in data) {
                    str += '<tr><td>' + item + '</td><td>' + data[item] + '</td></tr>';
                }

                str += '</table>';
                document.getElementsByClassName('record')[0].innerHTML = str;
            }

        },
        fail: function () {
            console.log("Request for toDance failed!");
        }
    });

}