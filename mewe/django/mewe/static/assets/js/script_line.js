/*
 * @Author: hc J
 * @Date: 2023-06-29 10:36:15
 * @LastEditTime: 2023-06-29 15:21:25
 * @Description: file content
 */
/*
 * @Author: hc J
 * @Date: 2023-06-13 17:48:24
 * @LastEditTime: 2023-06-27 13:43:18
 * @Description: file content
 */

var start_time = 0
var isStart = false;
setInterval(function () {
    $.ajax({
        url: "/line_data_port/",
        type: "post",
        dataType: "json",
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
        },
        success: function (result) {
            console.log(result);
            if (result.returnCode && isStart) {
                console.log(result.state);
                if (result.state === "run") {
                    document.getElementsByName("run_state")[0].innerHTML = "正在采集";
                    document.getElementsByName("run_state")[0].style.backgroundColor = "#7fff00";
                } else {
                    document.getElementsByName("run_state")[0].innerHTML = "睡眠";
                    document.getElementsByName("run_state")[0].style.backgroundColor = "#ff4646";
                }
                document.getElementsByName("run_user")[0].innerHTML = result.users;
                document.getElementsByName("run_message")[0].innerHTML = result.messages;
                document.getElementsByName("run_relation")[0].innerHTML = result.relations;
            }
        }
    })
    if (isStart) {
        var currentTime = new Date().getTime();
        var elapsedTime = currentTime - start_time;

        var hours = Math.floor(elapsedTime / (1000 * 60 * 60));
        var minutes = Math.floor((elapsedTime % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((elapsedTime % (1000 * 60)) / 1000);

        var hoursStr = hours.toString().padStart(2, '0');
        var minutesStr = minutes.toString().padStart(2, '0');
        var secondsStr = seconds.toString().padStart(2, '0');

        document.getElementById("run_time").innerHTML = hoursStr + ':' + minutesStr + ':' + secondsStr;
    }
}, 1000);




function changeContent() {
    var radio = document.querySelector('input[name="type"]:checked').value;
    var content_p = document.getElementById("func_p");
    var content_input = document.getElementById("func_input");
    if (radio === "t") {
        content_p.innerHTML = "采集时间";
        content_input.setAttribute("placeholder", "采集时间(秒)");
    } else if (radio === "i") {
        content_p.innerHTML = "采集条数";
        content_input.setAttribute("placeholder", "采集条数");
    }
}

//提交任务
$("[name='start_line']").click(function () {
    console.log("提交任务");
    isStart = true;
    document.getElementsByName("run_email")[0].innerHTML = document.getElementsByName("email")[0].value;
    // document.getElementsByName("run_group")[0].innerHTML = document.getElementsByName("group_url")[0].value.split("/").pop();
    start_time = new Date().getTime();
    $.ajax({
        url: "/line_port/",
        type: "post",
        dataType: "json",
        data: {
            email: document.getElementsByName("email")[0].value,
            password: document.getElementsByName("password")[0].value,
            type: document.querySelector('input[name="type"]:checked').value,
            type_data: document.getElementById("func_input").value,
            interval: document.getElementsByName("interval_time")[0].value,
            save_path: document.getElementsByName("save_path")[0].value,
            browser: document.querySelector('input[name="browser"]:checked').value,
            browser_data: document.getElementsByName("drive_path")[0].value,
            csrfmiddlewaretoken: '{{ csrf_token }}',
        },
        success: function (result) {
            if (result.returnCode) {
                alert("任务提交成功")
            } else {
                alert("error")
            }
        }
    })
});