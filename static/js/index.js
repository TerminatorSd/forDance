/**
 * Created by xsd on 17-11-3.
 */
window.onload = function () {

};

function lookAt()
{
    var head = document.getElementsByTagName('header')[0];
    var info = document.getElementsByClassName('info')[0];
    var con = document.getElementsByClassName('container')[0];

    head.innerHTML = 'Who will dance with you tonight?';
    info.style.display = 'block';
    con.style.display = 'none';

}

function goBack()
{
    var head = document.getElementsByTagName('header')[0];
    var info = document.getElementsByClassName('info')[0];
    var con = document.getElementsByClassName('container')[0];

    head.innerHTML = 'Dance is good for your health.';
    info.style.display = 'none';
    con.style.display = 'block';

}

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
               alert('Good boy/girl, see you later');
               window.location.reload();
            }

        },
        fail: function () {
            console.log("Request for toDance failed!");
        }
    });
}

function getDance() {

    var place = document.getElementsByClassName('info_place')[0].value;
    var time = document.getElementsByClassName('info_date')[0].value;
    var csrf = document.getElementsByTagName('input')[0].value;


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