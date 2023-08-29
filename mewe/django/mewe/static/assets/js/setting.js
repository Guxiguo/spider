
//用户名修改-ajax-start
$("[name='username_save_Button']").click(function () {
    var newUsername = document.getElementsByName("newUsername")[0].value; //获取用户名
    if (newUsername === "") {//不能为空
        alert("修改的用户名不能为空")
    }
    else {
        $.ajax({
            url: "/set_new_username_port/",
            type: "post",
            dataType: "json",
            data: {
                newUsername: newUsername,
                csrfmiddlewaretoken: '{{ csrf_token }}',
            },
            success: function (result) {
                if (result.returnCode == 'true') {
                    alert("用户名修改成功")
                }
                if (result.returnCode == 'false') {
                    alert("发生错误请稍后重试===>" + result.returnCode + "(" + result.returnContent + ")")
                }
            }
        })
    }
});
//用户名修改-ajax-end


//恢复默认设置-start
function restore() {
    document.getElementsByName("themeCode")[0].innerHTML = 'xcode'//code主题
    document.getElementsByName("themeResult")[0].innerHTML = 'xcode'//result主题
    document.getElementsByName("codeFontSize_input")[0].value = '15'//code字体-内容
    document.getElementsByName("codeFontSize_input")[0].setAttribute("placeholder", "15")//code字体-提示
    document.getElementsByName("resultFontSize_input")[0].value = '15'//result字体-内容
    document.getElementsByName("resultFontSize_input")[0].setAttribute("placeholder", "15")//result字体-提示
    document.getElementsByName("tabSize_input")[0].value = '4'//制表符-内容
    document.getElementsByName("tabSize_input")[0].setAttribute("placeholder", "4")//制表符-提示
    $.ajax({
        url: "/restore_edit_port/",
        type: "post",
        dataType: "json",
        data: {
            restore: 'true',
            csrfmiddlewaretoken: '{{ csrf_token }}',
        },
        success: function (result) {
            if (result.returnCode == 'true') {
                alert("编辑器设置已恢复默认设置")
            }
            if (result.returnCode == 'false') {
                alert("发生错误请稍后重试===>" + result.returnCode + "(" + result.returnContent + ")")
            }
        }
    })




}
//恢复默认设置-end


//编辑器设置-ajax-start
$("[name='edit_save_Button']").click(function () {
    codeFontSize_input = document.getElementsByName("codeFontSize_input")[0].value
    resultFontSize_input = document.getElementsByName("resultFontSize_input")[0].value
    tabSize_input = document.getElementsByName("tabSize_input")[0].value
    if (codeFontSize_input === "") {
        codeFontSize_input = "unchanged"
    }
    if (resultFontSize_input === "") {
        resultFontSize_input = "unchanged"
    }
    if (tabSize_input === "") {
        tabSize_input = "unchanged"
    }
    $.ajax({
        url: "/edit_setting_port/",
        type: "post",
        dataType: "json",
        data: {
            themeCode: document.getElementsByName("themeCode")[0].innerHTML,
            themeResult: document.getElementsByName("themeResult")[0].innerHTML,
            codeFontSize_input: codeFontSize_input,
            resultFontSize_input: resultFontSize_input,
            tabSize_input: tabSize_input,
            csrfmiddlewaretoken: '{{ csrf_token }}',
        },
        success: function (result) {
            if (result.returnCode == 'true') {
                alert("设置已保存")
            }
            if (result.returnCode == 'false') {
                alert("发生错误请稍后重试===>" + result.returnCode + "(" + result.returnContent + ")")
            }
        }
    })
});
//编辑器设置-ajax-end


//退出登录-start
$("[name='exit_Button']").click(function () {
    $.ajax({
        url: "/exit_port/",
        type: "post",
        dataType: "json",
        data: {
            exit: 'true',
            csrfmiddlewaretoken: '{{ csrf_token }}',
        },
        success: function (result) {
            if (result.returnCode == 'true') {
                // 页面跳转
                window.location.href = "/";
            }
            if (result.returnCode == 'false') {
                alert("发生错误请稍后重试===>" + result.returnCode + "(" + result.returnContent + ")")
            }
        }
    })
});
//退出登录-end
