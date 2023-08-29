/*
 * @Author: your name
 * @Date: 2021-01-05 21:13:52
 * @LastEditTime: 2021-01-05 22:37:59
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \GraduationProject\前端模版\js\touchmedia.js
 */
touchmedia_flag = false;
function touchmedia_over_Dev() {
    var mediaQQ = document.getElementsByName("developer");
    if (!touchmedia_flag) {
        for (var i = 0; i < mediaQQ[0].children.length; i++) {
            mediaQQ[0].children[i].setAttribute("fill", "#ff4646")
            touchmedia_flag = true;
        }
    }
}
function touchmedia_out_Dev() {
    var mediaQQ = document.getElementsByName("developer");
    if (touchmedia_flag) {
        for (var i = 0; i < mediaQQ[0].children.length; i++) {
            mediaQQ[0].children[i].setAttribute("fill", "#ffffff")
            touchmedia_flag = false;
        }
    }
}
function touchmedia_over_QQ() {
    var mediaQQ = document.getElementsByName("mediaQQ");
    if (!touchmedia_flag) {
        for (var i = 0; i < mediaQQ[0].children.length; i++) {
            mediaQQ[0].children[i].setAttribute("fill", "#ff4646")
            touchmedia_flag = true;
        }
    }
}
function touchmedia_out_QQ() {
    var mediaQQ = document.getElementsByName("mediaQQ");
    if (touchmedia_flag) {
        for (var i = 0; i < mediaQQ[0].children.length; i++) {
            mediaQQ[0].children[i].setAttribute("fill", "#ffffff")
            touchmedia_flag = false;
        }
    }
}
function touchmedia_over_Bi() {
    var mediaQQ = document.getElementsByName("mediaBiliBili");
    if (!touchmedia_flag) {
        for (var i = 0; i < mediaQQ[0].children.length; i++) {
            mediaQQ[0].children[i].setAttribute("fill", "#ff4646")
            touchmedia_flag = true;
        }
    }
}
function touchmedia_out_Bi() {
    var mediaQQ = document.getElementsByName("mediaBiliBili");
    if (touchmedia_flag) {
        for (var i = 0; i < mediaQQ[0].children.length; i++) {
            mediaQQ[0].children[i].setAttribute("fill", "#ffffff")
            touchmedia_flag = false;
        }
    }
}
function touchmedia_over_Wb() {
    var mediaQQ = document.getElementsByName("mediaWeiBo");
    if (!touchmedia_flag) {
        for (var i = 0; i < mediaQQ[0].children.length; i++) {
            mediaQQ[0].children[i].setAttribute("fill", "#ff4646")
            touchmedia_flag = true;
        }
    }
}
function touchmedia_out_Wb() {
    var mediaQQ = document.getElementsByName("mediaWeiBo");
    if (touchmedia_flag) {
        for (var i = 0; i < mediaQQ[0].children.length; i++) {
            mediaQQ[0].children[i].setAttribute("fill", "#ffffff")
            touchmedia_flag = false;
        }
    }
}