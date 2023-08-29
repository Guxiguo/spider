/*
 * @Author: your name
 * @Date: 2021-01-18 14:42:06
 * @LastEditTime: 2021-02-06 17:49:57
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \chordsofcode\static\assets\js\register.js
 */
//点击获取邮箱验证-ajax-start
$("[name='emailcode_button']").click(function () {
    var isEmail = checkEmail();//邮箱格式验证
    if (isEmail) {
        document.getElementsByName("emailcode")[0].placeholder = "验证码已发送至您的邮箱"; //修改验证码input提示内容
        //按钮倒计时-start
        let count = 60;//倒计时60s
        const countDown = setInterval(() => {
            if (count === 0) {
                $("[name='emailcode_button']").text("重新发送").removeAttr("disabled");
                clearInterval(countDown);
            } else {
                $("[name='emailcode_button']").attr("disabled", true);
                $("[name='emailcode_button']").text(count + '秒后可重新获取');
            }
            count--;
        }, 1000);//时间间隔1s
        //按钮倒计时-end
        //请求后端发送邮箱验证码-ajax-start
        $.ajax({
            url: "/email_code_port/",
            type: "post",
            dataType: "json",
            data: {
                email: $("[name='email']").val(),
                csrfmiddlewaretoken: '{{ csrf_token }}',
            },
            success: function (result) {
                if (result.returnCode != 'true') {//后端验证出现错误
                    alert("发送验证码发生错误，请稍后重试--->" + result.returnCode + "(" + result.returnContent + ")");
                }
            }
        })
        //请求后端发送邮箱验证码-ajax-end
    }
})
//点击获取邮箱验证-ajax-end

//点击注册按钮，提交注册-ajax-start
$("[name='register_Button']").click(function () {
    // console.log("register test")
    var isUsername = false;//用户名验证
    if (document.getElementsByName("username")[0].value === "") {
        isUsername = false;
        alert("用户名不能为空");
        return;
    }
    else {
        isUsername = true;
    }
    var isEmail = checkEmail();//邮箱格式验证
    if (!isEmail) {
        return;
    }
    var isPassword = checkPassword();//密码格式验证
    if (!isPassword) {
        return;
    }
    var isSamePassword = false;//两次密码是否相同
    //判断两次输入密码-start
    if (isPassword) {
        //两次密码相同
        if (document.getElementsByName("password")[0].value == document.getElementsByName("passwordagain")[0].value) {
            isSamePassword = true
        }
        //两次密码不同
        else {
            alert("两次密码不相同");
            isSamePassword = false
            return;
        }
    }
    //判断两次输入密码-end
    var isEmailCode = checkEmailCode();//邮箱验证码
    if (!isEmailCode) {
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
    if (isUsername && isEmail && isPassword && isSamePassword && isEmailCode && isDragText) {
        $.ajax({
            url: "/register_port/",
            type: "post",
            dataType: "json",
            data: {
                username: document.getElementsByName("username")[0].value,
                email: document.getElementsByName("email")[0].value,
                password: document.getElementsByName("password")[0].value,
                emailcode: document.getElementsByName("emailcode")[0].value,
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

    } else if (obj.value.length < 8) { //长度小于8位
        alert("密码长度不能小于8位");
        return false;

    } else if (obj.value.length > 20) { //长度小于8位
        alert("密码长度不能大于20位");
        return false;
    }
    else {
        return true;
    }
}
//密码和合法性检查-end



//邮箱验证码合法性检查-start
function checkEmailCode() {
    var obj = document.getElementsByName("emailcode")[0]; //要验证的对象
    if (obj.value === "") { //输入不能为空
        alert("邮箱验证码不能为空");
        return false;

    } else if (obj.value.length != 4) { //长度不等于4位
        alert("邮箱验证码有误");
        return false;
    }
    else {
        return true;
    }
}
//邮箱验证码合法性检查-end