/*
 * @Author: hc J
 * @Date: 2023-06-13 17:48:24
 * @LastEditTime: 2023-06-13 17:48:25
 * @Description: file content
 */
//-----------------------------------------------------------
//-----------------------------------------------------------
//全局变量-start

var SAVE = false;

//全局变量-end
//-----------------------------------------------------------
//-----------------------------------------------------------




//-----------------------------------------------------------
//-----------------------------------------------------------
// 初始化-start
//-----------------------------------------------------------
//-----------------------------------------------------------
//经过计算获得恰到好处的编辑器高度
document.getElementById("editordiv").style.height = document.body.scrollHeight - document.getElementsByClassName("hero_area")[0].offsetHeight + "px"
var userSettings = {//初始化参数
    'codeTheme': '',
    'resultTheme': '',
    'codeFont': '',
    'resultFont': '',
    'tabSize': '',
    'fileContent': '',
    'visited': '',
    'edited': '',
}
//请求编辑器设置和初始内容-start
$.ajax({
    url: "/edit_ini_port/",
    type: "post",
    dataType: "json",
    data: {
        codeFile_id: document.getElementsByName("codeFile_id")[0].innerHTML,
        csrfmiddlewaretoken: '{{ csrf_token }}',
    },
    success: function (result) {
        if (result.returnCode == 'true') {
            userSettings['codeTheme'] = result.codeTheme
            userSettings['resultTheme'] = result.resultTheme
            userSettings['codeFont'] = result.codeFont
            userSettings['resultFont'] = result.resultFont
            userSettings['tabSize'] = result.tabSize
            userSettings['fileContent'] = result.fileContent
            userSettings['visited'] = result.visited
            userSettings['edited'] = result.edited
            edit_ini()
            result_ini()
        }
        if (result.returnCode == 'false') {
            alert("发生错误请稍后重试===>" + result.returnCode + "(" + result.returnContent + ")")
        }
    }
})
//请求编辑器设置和初始内容-end

//编辑器初始化-start
function edit_ini() {
    // 编辑器-start-----------------------------------------------------------
    ace.require("ace/ext/language_tools");
    var editor = ace.edit("code-editor"); //实例化
    editor.setTheme("ace/theme/" + userSettings['codeTheme'])
    editor.session.setMode("ace/mode/python")
    editor.setFontSize(parseInt(userSettings['codeFont'])); //字体大小
    editor.getSession().setTabSize(parseInt(userSettings['tabSize'])); //制表符长度
    editor.setShowPrintMargin(false);
    if (userSettings['visited'] == "1" && userSettings['edited'] == "0") {//无权编辑，只读
        editor.setReadOnly(true)
    }
    editor.setOptions({
        enableBasicAutocompletion: true,
        enableSnippets: true,
        enableLiveAutocompletion: true, //实时自动补全
    });
    editor.getSession().getValue() //获取全部内容
    editor.getSession().setUseWrapMode(true);//代码折叠
    editor.session.getLength() //总行数
    editor.getSession().setValue(userSettings['fileContent']) //初始化内容
    // 编辑器-end-----------------------------------------------------------

}
//编辑器初始化-end


//输出初始化-start
function result_ini() {
    // 输出-start-----------------------------------------------------------
    ace.require("ace/ext/language_tools");
    var result = ace.edit("code-result"); //实例化
    result.setTheme("ace/theme/" + userSettings['resultTheme'])
    result.session.setMode("ace/mode/text")
    result.setFontSize(parseInt(userSettings['resultFont'])); //字体大小
    result.getSession().setTabSize(4); //制表符长度
    result.setShowPrintMargin(false);
    result.setReadOnly(true)
    result.setHighlightActiveLine(false);
    result.renderer.setShowGutter(false);
    result.setOptions({
        wrap: true,//换行
    });
    // result.setOptions({
    //     enableBasicAutocompletion: true,
    //     enableSnippets: true,
    //     enableLiveAutocompletion: true, //实时自动补全
    // });
    // result.getSession().getValue() //获取全部内容
    // result.session.getLength() //总行数
    //监听是否有变化
    // result.getSession().on('change', function (e) {
    //     // console.log(result.getShowGutter())
    //     console.log(result.getSession().getValue())
    //     console.log('内容有变化')
    //     // result.session.getLength()
    //     // result.insert('a')
    // });
    result.getSession().setValue("运行结果") //初始化内容
    // 输出-end-----------------------------------------------------------

}
//输出初始化-end


//-----------------------------------------------------------
//-----------------------------------------------------------
// 初始化-end
//-----------------------------------------------------------
//-----------------------------------------------------------



//-----------------------------------------------------------
//-----------------------------------------------------------
// 实时保存-start
//-----------------------------------------------------------
//-----------------------------------------------------------

// 保存函数-start
function save_code() {
    // console.log("save now")
    var editor = ace.edit("code-editor"); //实例化
    // console.log(editor.getSession().getValue())
    $.ajax({
        url: "/save_code_port/",
        type: "post",
        dataType: "json",
        data: {
            codeFile_id: document.getElementsByName("codeFile_id")[0].innerHTML,
            codeContent: editor.getSession().getValue(),
            csrfmiddlewaretoken: '{{ csrf_token }}',
        },
        success: function (result) {
            if (result.returnCode == 'true') {
                // document.getElementsByName("edit_save_Button")[0].innerHTML = "<svg t=\"1613638315403\" class=\"icon\" viewBox=\"0 0 1024 1024\" version=\"1.1\"\
                // xmlns = \"http://www.w3.org/2000/svg\" p - id=\"8055\" width = \"25\" height = \"25\" >\
                //     <path\
                //       d=\"M893.3 293.3L730.7 130.7c-7.5-7.5-16.7-13-26.7-16V112H144c-17.7 0-32 14.3-32 32v736c0 17.7 14.3 32 32 32h736c17.7 0 32-14.3 32-32V338.5c0-17-6.7-33.2-18.7-45.2zM384 184h256v104H384V184z m456 656H184V184h136v136c0 17.7 14.3 32 32 32h320c17.7 0 32-14.3 32-32V205.8l136 136V840z\"\
                //       p-id=\"8056\" fill=\"#ffffff\"></path>\
                //     <path\
                //       d=\"M512 442c-79.5 0-144 64.5-144 144s64.5 144 144 144 144-64.5 144-144-64.5-144-144-144z m0 224c-44.2 0-80-35.8-80-80s35.8-80 80-80 80 35.8 80 80-35.8 80-80 80z\"\
                //       p-id=\"8057\" fill=\"#ffffff\"></path>\
                //   </svg >"+ "保存";
                // document.getElementsByName("edit_save_Button")[0].setAttribute("title", "上次保存时间:" + result.save_time);
            }
            if (result.returnCode == 'false') {
                alert("发生错误请稍后重试===>" + result.returnCode + "(" + result.returnContent + ")")
            }
        }
    })
}
// 保存函数-end


//编辑保存-start
document.onkeydown = function (e) {
    // alert("你按下了：" + e.key);
    SAVE = true;
}
document.onmousedown = function (e) {
    SAVE = true;
}
document.onmouseup = function (e) {
    SAVE = false;
}
var editor = ace.edit("code-editor"); //实例化
editor.getSession().on('change', function (e) {
    // if (SAVE) {
        save_code();
        // SAVE = false;
    // }
});
// const countDown1 = setInterval(() => {
//     save_code()
// }, 1000);//时间间隔3s
//编辑保存-end



//-----------------------------------------------------------
//-----------------------------------------------------------
// 实时保存-end
//-----------------------------------------------------------
//-----------------------------------------------------------


//-----------------------------------------------------------
//-----------------------------------------------------------
// 库安装-start
//-----------------------------------------------------------
//-----------------------------------------------------------


// 弹窗-打开-start
function pipinstall() {
    // console.log(document.body.scrollHeight - document.getElementsByClassName("hero_area")[0].offsetHeight);
    document.getElementById('windowLight').style.display = 'block';
    document.getElementById('windowFade').style.display = 'block'
}
// 弹窗-打开-end

// 库安装-start
$("[name='code_window_create_Button']").click(function () {
    var libName = document.getElementsByName('code_window_input')[0].value;
    if (libName === "") {
        alert("库名不能为空")
        return;
    }
    else {
        document.getElementsByName('code_window_input')[0].value = '';//清空内容
        document.getElementById('windowLight').style.display = 'none';
        document.getElementById('windowFade').style.display = 'none';
        document.getElementsByName('installlib')[0].innerHTML = '<svg t=\"1614321011390\" class=\"icon\" viewBox=\"0 0 1024 1024\" version=\"1.1\"\
        xmlns = \"http://www.w3.org/2000/svg\" p - id=\"8057\" width = \"25\" height = \"25\" >\
                    <path\
                      d=\"M888.3 757.4h-53.8c-4.2 0-7.7 3.5-7.7 7.7v61.8H197.1V197.1h629.8v61.8c0 4.2 3.5 7.7 7.7 7.7h53.8c4.2 0 7.7-3.4 7.7-7.7V158.7c0-17-13.7-30.7-30.7-30.7H158.7c-17 0-30.7 13.7-30.7 30.7v706.6c0 17 13.7 30.7 30.7 30.7h706.6c17 0 30.7-13.7 30.7-30.7V765.1c0-4.3-3.5-7.7-7.7-7.7z\"\
                      p-id=\"8058\" fill=\"#ffffff\"></path>\
                    <path\
                      d=\"M902 476H588v-76c0-6.7-7.8-10.5-13-6.3l-141.9 112c-4.1 3.2-4.1 9.4 0 12.6l141.9 112c5.3 4.2 13 0.4 13-6.3v-76h314c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8z\"\
                      p-id=\"8059\" fill=\"#ffffff\"></path>\
                  </svg >正在安装';
        $.ajax({
            url: "/pip_install_port/",
            type: "post",
            dataType: "json",
            data: {
                libName: libName,
                csrfmiddlewaretoken: '{{ csrf_token }}',
            },
            success: function (result) {
                if (result.returnCode == 'true') {
                    alert(result.result,);
                    document.getElementsByName('installlib')[0].innerHTML = '<svg t=\"1614321011390\" class=\"icon\" viewBox=\"0 0 1024 1024\" version=\"1.1\"\
        xmlns = \"http://www.w3.org/2000/svg\" p - id=\"8057\" width = \"25\" height = \"25\" >\
                    <path\
                      d=\"M888.3 757.4h-53.8c-4.2 0-7.7 3.5-7.7 7.7v61.8H197.1V197.1h629.8v61.8c0 4.2 3.5 7.7 7.7 7.7h53.8c4.2 0 7.7-3.4 7.7-7.7V158.7c0-17-13.7-30.7-30.7-30.7H158.7c-17 0-30.7 13.7-30.7 30.7v706.6c0 17 13.7 30.7 30.7 30.7h706.6c17 0 30.7-13.7 30.7-30.7V765.1c0-4.3-3.5-7.7-7.7-7.7z\"\
                      p-id=\"8058\" fill=\"#ffffff\"></path>\
                    <path\
                      d=\"M902 476H588v-76c0-6.7-7.8-10.5-13-6.3l-141.9 112c-4.1 3.2-4.1 9.4 0 12.6l141.9 112c5.3 4.2 13 0.4 13-6.3v-76h314c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8z\"\
                      p-id=\"8059\" fill=\"#ffffff\"></path>\
                  </svg >安装库';

                }
                if (result.returnCode == 'false') {
                    alert("发生错误请稍后重试===>" + result.returnCode + "(" + result.returnContent + ")")
                }
            }
        })
    }
});
// 库安装-end


// 弹窗-取消-start
$("[name='code_window_cancel_Button']").click(function () {
    document.getElementsByName('code_window_input')[0].value = '';//清空内容
    document.getElementById('windowLight').style.display = 'none';
    document.getElementById('windowFade').style.display = 'none';

});
// 弹窗-取消-end

//-----------------------------------------------------------
//-----------------------------------------------------------
// 库安装-end
//-----------------------------------------------------------
//-----------------------------------------------------------


//-----------------------------------------------------------
//-----------------------------------------------------------
// 运行-start
//-----------------------------------------------------------
//-----------------------------------------------------------


//运行代码-start
function runcode() {
    $.ajax({
        url: "/run_code_port/",
        type: "post",
        dataType: "json",
        data: {
            codeFile_id: document.getElementsByName("codeFile_id")[0].innerHTML,
            csrfmiddlewaretoken: '{{ csrf_token }}',
        },
        success: function (result) {
            if (result.returnCode == 'true') {
                // console.log(result.result)
                ace.require("ace/ext/language_tools");
                var result_code = ace.edit("code-result"); //实例化
                result_code.getSession().setValue(result.result) //初始化内容
            }
            if (result.returnCode == 'false') {
                alert("发生错误请稍后重试===>" + result.returnCode + "(" + result.returnContent + ")")
            }
        }
    })
}
//运行代码-end

//-----------------------------------------------------------
//-----------------------------------------------------------
// 运行-end
//-----------------------------------------------------------
//-----------------------------------------------------------

//-----------------------------------------------------------
//-----------------------------------------------------------
// 快捷键-start
//-----------------------------------------------------------
//-----------------------------------------------------------


//快捷键-start
function shortcutKey() {
    document.getElementById('windowLight_key').style.display = 'block';
    document.getElementById('windowFade_key').style.display = 'block'
}
$("[name='key_window_cancel_Button']").click(function () {
    // document.getElementsByName('code_window_input')[0].value = '';//清空内容
    document.getElementById('windowLight_key').style.display = 'none';
    document.getElementById('windowFade_key').style.display = 'none';

});
//ctrl+q清空-start
$(document).bind("keydown", function (e) {
    if (e.ctrlKey && (e.which == 81)) {
        e.preventDefault();
        ace.require("ace/ext/language_tools");
        var result_code = ace.edit("code-result"); //实例化
        result_code.getSession().setValue("运行结果") //初始化内容
        return false;
    }
});
//ctrl+c清空-end
//ctrl+s保存-start
// $(document).bind("keydown", function (e) {
//     if (e.ctrlKey && (e.which == 83)) {
//         e.preventDefault();
//         save_code()
//         return false;
//     }
// });
//ctrl+s保存-end
//快捷键-end

//-----------------------------------------------------------
//-----------------------------------------------------------
// 快捷键-end
//-----------------------------------------------------------
//-----------------------------------------------------------



//-----------------------------------------------------------
//-----------------------------------------------------------
// 邀请-start
//-----------------------------------------------------------
//-----------------------------------------------------------

//弹窗-打开-start
function shortcutInv() {
    document.getElementById('windowLight_invite').style.display = 'block';
    document.getElementById('windowFade_invite').style.display = 'block'
}
//弹窗-打开-end

//弹窗-关闭-start

$("[name='invite_window_cancel_Button']").click(function () {
    document.getElementById('windowLight_invite').style.display = 'none';
    document.getElementById('windowFade_invite').style.display = 'none';

});

//弹窗-关闭-start

//滑动开关按钮-start
document.getElementById("inner1").onclick = function () {
    if (this.className == "inner-off") {
        //剪贴板分享-start
        var content = $("[name='share_url']").html();
        var clipboard = new Clipboard("[name='share_btn']", {
            text: function () {
                return content;
            }
        });
        clipboard.on('success', function (e) {
            $.confirm({
                title: '警告',
                content: '打开公开分享后，任何用户便可通过链接访问本代码<br/>分享链接已经复制到您的剪贴板，快去分享吧',
                buttons: {
                    ok: {
                        text: '确认',
                        btnClass: 'btn-primary',
                    },
                }
            });
        });

        clipboard.on('error', function (e) {
            console.log(e);
        });
        //剪贴板分享-end
        this.style.left = -51 + "px";
        this.childNodes[1].checked = false;
        this.className = "inner-on";
    } else {
        this.style.left = 0;
        this.childNodes[1].checked = true;
        this.className = "inner-off";
    }
}
document.getElementById("inner2").onclick = function () {
    if (this.className == "inner-off") {
        $.confirm({
            title: '警告',
            content: '打开公开分享后，任何用户便可通过链接修改本代码',
            buttons: {
                ok: {
                    text: '确认',
                    btnClass: 'btn-primary',
                },
            }
        });
        this.style.left = -51 + "px";
        this.childNodes[1].checked = false;
        this.className = "inner-on";
    } else {
        this.style.left = 0;
        this.childNodes[1].checked = true;
        this.className = "inner-off";
    }
}
//滑动开关按钮-end

//-----------------------------------------------------------
//-----------------------------------------------------------
// 邀请-start
//-----------------------------------------------------------
//-----------------------------------------------------------


// ace.require("ace/ext/language_tools");
// var editor_code = ace.edit("code-editor"); //实例化
// editor_code.getSession().selection.on('changeCursor', function (e) {
//     // console.log(editor_code.selection.getCursor())
//     editor_code.selection.moveCursorTo(1, 3, true);

// });
// 实时请求代码 - start
// let count = 20;
// const countDown = setInterval(() => {
//     if (userSettings['visited'] == "1" || userSettings['edited'] == "1") {//无权编辑，只读
//         // SAVE = false;//保存关
//         // console.log("getcode")
//         // save_code()
//         // ace.require("ace/ext/language_tools");
//         // var editor_code = ace.edit("code-editor"); //实例化
//         // r = editor_code.selection.getCursor().row
//         // c = editor_code.selection.getCursor().column
//         // console.log(r, c)
//         if (!SAVE) {
//             getCodeContent()
//         }
//         // let RAndC = new Object()
//         // RAndC.row = 2
//         // RAndC.column = 3
//         // editor_code.getSession().insert(RAndC, "1")
//         // editor_code.selection.moveCursorTo(r, c)
//         // console.log(editor_code.selection.getCursor())
//         // ace.require("ace/ext/language_tools");
//         // var editor_code = ace.edit("code-editor"); //实例化

//         // SAVE = true;//保存开
//         // console.log(SAVE)
//     }
// }, 1000);//时间间隔3s


// function posConversion(strTarget1, codeContent) {
//     strTarget = strTarget1
//     let RowAndColumn = new Object()
//     RowAndColumn.row = 0
//     RowAndColumn.column = 0
//     strLine = codeContent.split("\n")
//     for (var i = 0; i < strLine.length; i++) {
//         if (strTarget < strLine[i].length) {
//             RowAndColumn.row = i
//             RowAndColumn.column = strTarget - 1
//             break
//         }
//         else {
//             strTarget -= strLine[i].length + 1
//         }
//     }
//     return RowAndColumn
//     // console.log(RowAndColumn)
// }

// function mergeCode(mergeList, codeContent, insertContent) {
//     console.log(mergeList)
//     // let RowAndColumn = new Object()
//     // RowAndColumn.row = 0
//     // RowAndColumn.column = 0
//     // let a = new Object()
//     // a.start = RowAndColumn
//     // RowAndColumn.row = 1
//     // RowAndColumn.column = 3
//     // a.end = RowAndColumn
//     // console.log(a)
//     ace.require("ace/ext/language_tools");
//     var editor_code = ace.edit("code-editor"); //实例化
//     // posConversion(40, codeContent)
//     var flag_len = 0 //调整位
//     for (var i = 0; i < mergeList.length; i++) {
//         var tag = mergeList[i]["tag"]
//         var i1 = mergeList[i]["i1"]
//         var i2 = mergeList[i]["i2"]
//         var j1 = mergeList[i]["j1"]
//         var j2 = mergeList[i]["j2"]
//         if (tag == "replace") {

//         }
//         if (tag == "delete") {
//             let ranges = new Object()
//             ranges.start = posConversion(i1 + flag_len, codeContent)
//             ranges.end = posConversion(i2 + flag_len, codeContent)
//             console.log(ranges)
//             editor_code.getSession().remove(ranges)
//             flag_len -= i2 - i1
//         }
//         if (tag == "insert") {
//             editor.getSession().insert(posConversion(i1 + flag_len, codeContent), insertContent.substring(j1, j2))
//             flag_len += j2 - j1
//         }
//     }
// }


// function getCodeContent() {
//     ace.require("ace/ext/language_tools");
//     var editor_code = ace.edit("code-editor"); //实例化
//     $.ajax({
//         url: "/get_code_content_port/",
//         type: "post",
//         dataType: "json",
//         data: {
//             codeFile_id: document.getElementsByName("codeFile_id")[0].innerHTML,
//             codeContent: editor.getSession().getValue(),//返回文件内容，用于比对文件
//             csrfmiddlewaretoken: '{{ csrf_token }}',
//         },
//         success: function (result) {
//             if (result.returnCode == 'true') {
//                 userSettings['fileContent'] = result.fileContent
//                 // console.log(result.mergeList)
//                 mergeCode(result.mergeList, editor_code.getSession().getValue(), result.insertContent)
//                 // editor_code.getSession().setValue(result.fileContent) //初始化内容
//             }
//             if (result.returnCode == 'false') {
//                 alert("发生错误请稍后重试===>" + result.returnCode + "(" + result.returnContent + ")")
//             }
//         }
//     })
// }

//实时请求代码-end
