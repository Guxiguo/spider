/*
 * @Author: your name
 * @Date: 2021-01-18 14:42:06
 * @LastEditTime: 2021-02-06 17:48:48
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \chordsofcode\static\assets\js\register.js
 */

//点击注册按钮，提交注册-ajax-start
$("[name='login_Button']").click(function () {
    var isEmail = checkEmail();//邮箱格式验证
    if (!isEmail) {
        return;
    }
    var isPassword = checkPassword();//密码格式验证
    if (!isPassword) {
        return;
    }
    //滑动验证-start
    var isDragText = false;
    var dragtext = document.getElementsByName("dragTest")[0].innerHTML
    if (dragtext == "验证通过") {
        var isDragText = true;
    }
    else {
        alert("请完成滑动验证");
    }
    //滑动验证-end
    if (!isDragText) {
        return
    }
    if (isEmail && isPassword && isDragText) {
        $.ajax({
            url: "/login_port/",
            type: "post",
            dataType: "json",
            data: {
                email: document.getElementsByName("email")[0].value,
                password: document.getElementsByName("password")[0].value,
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
    }
});
//点击注册按钮，提交注册-ajax-end

//邮箱和合法性检查-start
function checkEmail() {
    var reg = new RegExp("^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$"); //正则表达式
    var obj = document.getElementsByName("email")[0]; //要验证的对象
    if (obj.value === "") { //输入不能为空
        alert("邮箱不能为空");
        return false;

    } else if (!reg.test(obj.value)) { //正则验证不通过，格式不对
        alert("邮箱格式不正确");
        return false;

    } else {
        return true;
    }
}
//邮箱和合法性检查-end

//密码和合法性检查-start
function checkPassword() {
    var obj = document.getElementsByName("password")[0]; //要验证的对象
    if (obj.value === "") { //输入不能为空
        alert("密码不能为空");
        return false;

    }
    else {
        return true;
    }
}
//密码和合法性检查-end